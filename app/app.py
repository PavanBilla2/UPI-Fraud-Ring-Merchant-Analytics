import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="UPI Fraud Ring & Merchant Analytics",
    page_icon="💳",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    executive_kpis = pd.read_csv(
        DATA_DIR / "powerbi_executive_kpis.csv"
    )

    daily_trend = pd.read_csv(
        DATA_DIR / "powerbi_daily_trend.csv"
    )

    merchant_intelligence = pd.read_csv(
        DATA_DIR / "powerbi_merchant_intelligence.csv"
    )

    category_intelligence = pd.read_csv(
        DATA_DIR / "powerbi_category_intelligence.csv"
    )

    user_risk_intelligence = pd.read_csv(
        DATA_DIR / "powerbi_user_risk_intelligence.csv"
    )

    chargeback_analytics = pd.read_csv(
        DATA_DIR / "powerbi_chargeback_analytics.csv"
    )

    investigation_evidence = pd.read_csv(
        DATA_DIR / "powerbi_investigation_evidence.csv"
    )

    suspicious_networks = pd.read_csv(
        DATA_DIR / "powerbi_suspicious_networks_top50.csv"
    )

    return (
        executive_kpis,
        daily_trend,
        merchant_intelligence,
        category_intelligence,
        user_risk_intelligence,
        chargeback_analytics,
        investigation_evidence,
        suspicious_networks
    )


(
    executive_kpis,
    daily_trend,
    merchant_intelligence,
    category_intelligence,
    user_risk_intelligence,
    chargeback_analytics,
    investigation_evidence,
    suspicious_networks
) = load_data()


# ============================================================
# HELPER
# ============================================================

def get_kpi(name):

    value = executive_kpis.loc[
        executive_kpis["metric"] == name,
        "value"
    ]

    if len(value) == 0:
        return 0

    return value.iloc[0]


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("💳 Fraud Intelligence")

st.sidebar.markdown(
    "### Navigation"
)

page = st.sidebar.radio(
    "Select Dashboard",
    [
        "📊 Executive Overview",
        "🔎 Fraud Investigation"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "UPI Fraud Ring & Merchant Analytics"
)

st.sidebar.caption(
    "FinTech & BFSI — Datathon Project"
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "📊 Executive Overview":

    st.title("💳 UPI Fraud Ring & Merchant Analytics")

    st.markdown(
        "### FinTech & BFSI — Fraud Intelligence Dashboard"
    )

    st.caption(
        "Transaction monitoring • Fraud-risk scoring • "
        "Merchant intelligence • Chargeback analytics • "
        "Suspicious network analysis"
    )

    st.divider()

    # --------------------------------------------------------
    # KPI VALUES
    # --------------------------------------------------------

    total_transactions = int(
        get_kpi("Total Transactions")
    )

    transaction_value = float(
        get_kpi("Total Transaction Value")
    )

    avg_transaction = float(
        get_kpi("Average Transaction Value")
    )

    chargebacks = int(
        get_kpi("Chargeback Transactions")
    )

    fraud_chargebacks = int(
        get_kpi(
            "Fraud/Unauthorized Chargeback Transactions"
        )
    )

    high_risk = int(
        get_kpi("HIGH Risk Transactions")
    )

    critical_risk = int(
        get_kpi("CRITICAL Risk Transactions")
    )

    high_critical = int(
        get_kpi("HIGH + CRITICAL Risk Transactions")
    )

    # --------------------------------------------------------
    # EXECUTIVE KPIs
    # --------------------------------------------------------

    st.subheader("📊 Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Transactions",
            f"{total_transactions:,}"
        )

    with col2:
        st.metric(
            "Transaction Value",
            f"₹{transaction_value / 1_000_000:.2f}M"
        )

    with col3:
        st.metric(
            "Chargeback Transactions",
            f"{chargebacks:,}"
        )

    with col4:
        st.metric(
            "Fraud/Unauthorized CB",
            f"{fraud_chargebacks:,}"
        )

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric(
            "Average Transaction",
            f"₹{avg_transaction:,.0f}"
        )

    with col6:
        st.metric(
            "HIGH Risk",
            f"{high_risk:,}"
        )

    with col7:
        st.metric(
            "CRITICAL Risk",
            f"{critical_risk:,}"
        )

    with col8:
        st.metric(
            "HIGH + CRITICAL",
            f"{high_critical:,}",
            f"{high_critical / total_transactions * 100:.2f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # DAILY TREND
    # --------------------------------------------------------

    st.subheader("📈 Transaction & Fraud-Risk Trend")

    daily_trend["transaction_date"] = pd.to_datetime(
        daily_trend["transaction_date"]
    )

    fig_trend = px.line(
        daily_trend,
        x="transaction_date",
        y=[
            "transaction_count",
            "chargeback_transactions",
            "high_risk_transactions"
        ],
        markers=True,
        labels={
            "transaction_date": "Date",
            "value": "Transaction Count",
            "variable": "Metric"
        },
        title="Daily Transaction Activity"
    )

    fig_trend.update_layout(
        hovermode="x unified",
        legend_title_text=""
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )

    # --------------------------------------------------------
    # RISK + CATEGORY
    # --------------------------------------------------------

    col_left, col_right = st.columns(2)

    with col_left:

        st.subheader("🚨 Risk Band Distribution")

        risk_data = pd.DataFrame({
            "Risk Band": [
                "LOW",
                "MEDIUM",
                "HIGH",
                "CRITICAL"
            ],
            "Transactions": [
                18553,
                565,
                788,
                94
            ]
        })

        fig_risk = px.pie(
            risk_data,
            names="Risk Band",
            values="Transactions",
            hole=0.55,
            title="Fraud Risk Band Distribution"
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )

    with col_right:

        st.subheader(
            "🏪 Highest-Risk Merchant Categories"
        )

        category_plot = category_intelligence[
            category_intelligence[
                "merchant_category_final"
            ].notna()
            &
            (
                category_intelligence[
                    "merchant_category_final"
                ] != "NA"
            )
        ].copy()

        category_plot = category_plot.sort_values(
            "chargeback_ratio",
            ascending=False
        ).head(10)

        fig_category = px.bar(
            category_plot,
            x="chargeback_ratio",
            y="merchant_category_final",
            orientation="h",
            text="chargeback_ratio",
            title="Top Categories by Chargeback Ratio"
        )

        fig_category.update_traces(
            texttemplate="%{text:.1%}",
            textposition="outside"
        )

        fig_category.update_layout(
            xaxis_tickformat=".0%",
            yaxis_title="Merchant Category",
            xaxis_title="Chargeback / Transaction Ratio"
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    # --------------------------------------------------------
    # BUSINESS SIGNALS
    # --------------------------------------------------------

    st.divider()

    st.subheader("💡 Key Business Signals")

    insight1, insight2, insight3 = st.columns(3)

    with insight1:
        st.info(
            f"**{high_critical:,} transactions** are classified "
            "as **HIGH or CRITICAL risk** by the explainable "
            "risk framework."
        )

    with insight2:
        st.warning(
            f"**{fraud_chargebacks:,} transactions** have "
            "fraud/unauthorized chargeback evidence in the "
            "enriched transaction analytics."
        )

    with insight3:

        top_category = category_plot.iloc[0][
            "merchant_category_final"
        ]

        top_ratio = category_plot.iloc[0][
            "chargeback_ratio"
        ]

        st.error(
            f"**{top_category}** has the highest observed "
            f"chargeback ratio among the displayed categories: "
            f"**{top_ratio:.1%}**."
        )

    st.divider()

    st.caption(
        "Risk scores are analytical ranking signals based on "
        "observable evidence and should not be interpreted as "
        "probabilities of fraud."
    )


# ============================================================
# FRAUD INVESTIGATION
# ============================================================

elif page == "🔎 Fraud Investigation":

    st.title("🔎 Fraud Investigation Workspace")

    st.markdown(
        "### Evidence-driven transaction investigation"
    )

    st.caption(
        "Use the filters below to prioritize suspicious "
        "transactions for analyst review."
    )

    st.divider()

    # --------------------------------------------------------
    # COPY DATA
    # --------------------------------------------------------

    investigation = investigation_evidence.copy()

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    st.subheader("🎯 Investigation Filters")

    col1, col2, col3 = st.columns(3)

    with col1:

        risk_options = [
            "ALL",
            "CRITICAL",
            "HIGH"
        ]

        selected_risk = st.selectbox(
            "Risk Band",
            risk_options
        )

    with col2:

        priority_options = [
            "ALL"
        ] + sorted(
            investigation[
                "investigation_priority"
            ].dropna().unique().tolist()
        )

        selected_priority = st.selectbox(
            "Investigation Priority",
            priority_options
        )

    with col3:

        category_options = [
            "ALL"
        ] + sorted(
            investigation[
                "merchant_category_final"
            ]
            .dropna()
            .unique()
            .tolist()
        )

        selected_category = st.selectbox(
            "Merchant Category",
            category_options
        )

    search_text = st.text_input(
        "🔍 Search Transaction ID, User ID or Merchant ID",
        placeholder="Example: TXN00011255"
    )

    # --------------------------------------------------------
    # APPLY FILTERS
    # --------------------------------------------------------

    filtered = investigation.copy()

    if selected_risk != "ALL":

        filtered = filtered[
            filtered["fraud_risk_band"]
            == selected_risk
        ]

    if selected_priority != "ALL":

        filtered = filtered[
            filtered["investigation_priority"]
            == selected_priority
        ]

    if selected_category != "ALL":

        filtered = filtered[
            filtered["merchant_category_final"]
            == selected_category
        ]

    if search_text.strip():

        search_text = search_text.strip()

        mask = (
            filtered["txn_id"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
            |
            filtered["user_id"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
            |
            filtered["merchant_id"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        )

        filtered = filtered[mask]

    # --------------------------------------------------------
    # INVESTIGATION KPIs
    # --------------------------------------------------------

    st.divider()

    st.subheader("🚨 Investigation Summary")

    total_cases = len(filtered)

    critical_cases = len(
        filtered[
            filtered["fraud_risk_band"]
            == "CRITICAL"
        ]
    )

    high_cases = len(
        filtered[
            filtered["fraud_risk_band"]
            == "HIGH"
        ]
    )

    fraud_cases = int(
        filtered["fraud_chargeback_flag"]
        .fillna(0)
        .sum()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Cases",
            f"{total_cases:,}"
        )

    with col2:
        st.metric(
            "CRITICAL",
            f"{critical_cases:,}"
        )

    with col3:
        st.metric(
            "HIGH",
            f"{high_cases:,}"
        )

    with col4:
        st.metric(
            "Fraud CB Evidence",
            f"{fraud_cases:,}"
        )

    # --------------------------------------------------------
    # PRIORITY BREAKDOWN
    # --------------------------------------------------------

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        priority_counts = (
            filtered[
                "investigation_priority"
            ]
            .value_counts()
            .reset_index()
        )

        priority_counts.columns = [
            "Priority",
            "Cases"
        ]

        fig_priority = px.bar(
            priority_counts,
            x="Priority",
            y="Cases",
            text="Cases",
            title="Investigation Priority Distribution"
        )

        fig_priority.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig_priority,
            use_container_width=True
        )

    with col2:

        score_data = filtered.copy()

        fig_score = px.histogram(
            score_data,
            x="fraud_risk_score",
            nbins=20,
            title="Risk Score Distribution",
            labels={
                "fraud_risk_score": "Risk Score"
            }
        )

        st.plotly_chart(
            fig_score,
            use_container_width=True
        )

    # --------------------------------------------------------
    # INVESTIGATION TABLE
    # --------------------------------------------------------

    st.divider()

    st.subheader("📋 Investigation Cases")

    display_columns = [
        "txn_id",
        "user_id",
        "merchant_id",
        "merchant_name",
        "merchant_category_final",
        "amount_numeric",
        "fraud_risk_score",
        "fraud_risk_band",
        "investigation_priority",
        "risk_reasons",
        "recommended_action"
    ]

    display_data = filtered[
        display_columns
    ].copy()

    display_data = display_data.sort_values(
        ["fraud_risk_score", "investigation_priority"],
        ascending=[False, True]
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "amount_numeric": st.column_config.NumberColumn(
                "Amount",
                format="₹%.2f"
            ),
            "fraud_risk_score": st.column_config.NumberColumn(
                "Risk Score",
                format="%d"
            )
        }
    )

    st.caption(
        f"Showing {len(display_data):,} investigation cases."
    )

    st.divider()

    st.info(
        "⚠️ Investigation cases are prioritized using observable "
        "risk signals such as chargebacks, identity anomalies, "
        "repeat chargebacks, velocity anomalies and merchant "
        "risk indicators. They are not confirmed fraud cases."
    )