import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from copilot import render_copilot

# ============================================================
# PLOTLY UI/UX THEME
# ============================================================

RISK_COLORS = {
    "LOW": "#10B981",
    "MEDIUM": "#F59E0B",
    "HIGH": "#F97316",
    "CRITICAL": "#EF4444"
}

CHART_COLORS = {
    "primary": "#38BDF8",
    "secondary": "#818CF8",
    "accent": "#22D3EE",
    "warning": "#F59E0B",
    "danger": "#F43F5E",
    "success": "#10B981"
}


def style_plotly(fig, height=430):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(8,14,26,0.28)",
        font=dict(
            family="Inter, Segoe UI, sans-serif",
            size=13,
            color="#E8EEF7"
        ),
        title=dict(
            font=dict(size=17, color="#F8FAFC"),
            x=0,
            xanchor="left"
        ),
        margin=dict(l=55, r=35, t=65, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)"
        ),
        hoverlabel=dict(
            bgcolor="#121A2B",
            bordercolor="#334155",
            font=dict(
                family="Inter, Segoe UI, sans-serif",
                size=13,
                color="#F8FAFC"
            )
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(148,163,184,0.11)",
        zeroline=False,
        linecolor="rgba(148,163,184,0.18)",
        tickfont=dict(color="#AEB9C9")
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(148,163,184,0.11)",
        zeroline=False,
        linecolor="rgba(148,163,184,0.18)",
        tickfont=dict(color="#AEB9C9")
    )

    return fig


def show_plotly(fig, height=430):
    fig = style_plotly(fig, height=height)
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "responsive": True,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"]
        }
    )

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
# LOAD DATA  (unchanged datasets / paths from the original app)
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
# HELPERS
# ============================================================

def get_kpi(name, default=0):
    """Look up a validated metric from powerbi_executive_kpis.csv."""

    value = executive_kpis.loc[
        executive_kpis["metric"] == name,
        "value"
    ]

    if len(value) == 0:
        return default

    return value.iloc[0]


def find_col(df, candidates):
    """Return the first column from `candidates` that exists in `df`."""

    for c in candidates:
        if c in df.columns:
            return c

    return None


def safe_numeric(df, cols):
    """Coerce a list of columns to numeric in-place, filling NaN with 0."""

    df = df.copy()

    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def clean_text_col(series, fallback):
    """Replace NaN / empty / literal 'NA' strings with a readable fallback."""

    cleaned = series.astype(str).replace(
        {"nan": None, "None": None, "": None, "NA": None}
    )

    return cleaned.fillna(fallback)


def fmt_inr(value):
    try:
        return f"₹{float(value):,.2f}"
    except (TypeError, ValueError):
        return "N/A"


def fmt_inr_compact(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "N/A"

    if abs(value) >= 1_000_000:
        return f"₹{value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"₹{value / 1_000:.2f}K"
    return f"₹{value:,.2f}"


def none_if_empty(df, col_list):
    """Return only the columns from col_list that actually exist in df."""
    return [c for c in col_list if c in df.columns]


# ============================================================
# PAGE HERO HELPER
# ============================================================

def page_hero(kicker, title, description):
    st.html(f"""
    <div class="upi-page-hero">
        <div class="upi-page-kicker">{kicker}</div>
        <div class="upi-page-title">{title}</div>
        <div class="upi-page-copy">{description}</div>
    </div>
    """)


# ============================================================
# PREMIUM UI / UX
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp {
        background:
            radial-gradient(circle at 10% 5%, rgba(14,165,233,0.10), transparent 24%),
            radial-gradient(circle at 90% 8%, rgba(99,102,241,0.12), transparent 24%),
            linear-gradient(180deg, #060A13 0%, #0A1020 100%);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    [data-testid="stHeader"] {
        background: rgba(6,10,19,0.78);
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    /* Premium top navigation */
    div[role="radiogroup"] {
        position: relative;
        display: grid !important;
        grid-template-columns: repeat(7, minmax(0, 1fr));
        gap: 6px;
        width: 100%;
        padding: 8px;
        margin: 10px 0 30px;
        border: 1px solid rgba(96,165,250,0.20);
        border-radius: 20px;
        background:
            linear-gradient(135deg, rgba(12,18,31,0.94), rgba(15,23,42,0.90)),
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='90' viewBox='0 0 180 90'%3E%3Cg fill='none' stroke='%2338BDF8' stroke-opacity='.10'%3E%3Cpath d='M10 72L54 30L108 58L166 16'/%3E%3Cpath d='M-10 20L42 64L94 18L150 70L190 38'/%3E%3C/g%3E%3Cg fill='%23818CF8' fill-opacity='.20'%3E%3Ccircle cx='54' cy='30' r='2'/%3E%3Ccircle cx='108' cy='58' r='2'/%3E%3Ccircle cx='166' cy='16' r='2'/%3E%3Ccircle cx='94' cy='18' r='2'/%3E%3C/g%3E%3C/svg%3E");
        background-size: auto, 180px 90px;
        box-shadow:
            0 18px 55px rgba(0,0,0,0.30),
            inset 0 1px 0 rgba(255,255,255,0.04);
        backdrop-filter: blur(18px);
    }

    div[role="radiogroup"]::before {
        content: "";
        position: absolute;
        left: 14px;
        right: 14px;
        top: 0;
        height: 2px;
        border-radius: 999px;
        background: linear-gradient(90deg, #22D3EE, #38BDF8, #818CF8, #A78BFA);
        opacity: .85;
    }

    div[role="radiogroup"] label {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 48px;
        padding: 8px 10px;
        border-radius: 13px;
        border: 1px solid transparent;
        transition: all 0.18s ease;
        color: #AEB9C9;
        font-size: 12px;
        font-weight: 650;
        text-align: center;
        line-height: 1.18;
        white-space: normal;
        cursor: pointer;
    }

    div[role="radiogroup"] label:hover {
        color: #F8FAFC;
        background: linear-gradient(135deg, rgba(56,189,248,0.10), rgba(129,140,248,0.08));
        border-color: rgba(56,189,248,0.20);
        transform: translateY(-1px);
    }

    div[role="radiogroup"] div[role="radio"][aria-checked="true"] {
        color: #FFFFFF;
        background:
            linear-gradient(135deg, rgba(14,165,233,0.96), rgba(99,102,241,0.96)),
            linear-gradient(135deg, rgba(56,189,248,0.16), rgba(129,140,248,0.16));
        border-radius: 13px;
        border-color: rgba(255,255,255,0.13);
        box-shadow:
            0 10px 26px rgba(14,165,233,0.22),
            inset 0 1px 0 rgba(255,255,255,0.16);
    }

    /* Hide the small "Fraud Intelligence Modules" helper label */
    .nav-kicker {
        display: none;
    }

    /* KPI cards — fixed geometry so cards with deltas never become taller */
    [data-testid="stMetric"] {
        height: 128px !important;
        min-height: 128px !important;
        box-sizing: border-box !important;
        padding: 18px 18px 14px !important;
        border-radius: 18px;
        border: 1px solid rgba(148,163,184,0.15);
        background:
            linear-gradient(145deg, rgba(20,30,48,0.92), rgba(11,17,30,0.90));
        box-shadow: 0 12px 32px rgba(0,0,0,0.18);
        transition: transform .18s ease, border-color .18s ease;
        overflow: hidden;
    }

    /* Keep metric contents vertically consistent across cards */
    [data-testid="stMetric"] [data-testid="stMetricLabel"] {
        min-height: 18px;
        display: flex;
        align-items: center;
    }

    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        margin-top: 3px;
        line-height: 1.05;
    }

    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        margin-top: 7px;
        line-height: 1.05;
        min-height: 18px;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(56,189,248,0.30);
    }

    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-weight: 800;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-testid="stTextInput"] input {
        background: rgba(15,23,42,0.90) !important;
        border-color: rgba(148,163,184,0.18) !important;
        border-radius: 12px !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
        border: 1px solid rgba(148,163,184,0.12);
    }

    [data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(148,163,184,0.15);
    }

    hr {
        border-color: rgba(148,163,184,0.12);
        margin: 2rem 0;
    }

    .upi-footer {
        margin-top: 64px;
        padding: 30px 24px 22px;
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 22px;
        background:
            radial-gradient(circle at 18% 0%, rgba(14,165,233,0.10), transparent 34%),
            radial-gradient(circle at 82% 0%, rgba(99,102,241,0.10), transparent 34%),
            rgba(9,15,27,0.90);
        text-align: center;
        box-shadow: 0 18px 55px rgba(0,0,0,0.20);
    }

    .upi-footer-title {
        font-size: 18px;
        font-weight: 800;
        color: #F8FAFC;
    }

    .upi-footer-subtitle {
        margin-top: 8px;
        color: #94A3B8;
        font-size: 12px;
    }

    .upi-footer-line {
        width: 86px;
        height: 2px;
        margin: 16px auto;
        border-radius: 999px;
        background: linear-gradient(90deg, #38BDF8, #818CF8);
    }

    .upi-footer-tech {
        color: #CBD5E1;
        font-size: 12px;
        font-weight: 600;
    }

    .upi-footer-note {
        margin-top: 10px;
        color: #64748B;
        font-size: 10px;
    }

    .upi-footer-copy {
        margin-top: 16px;
        color: #475569;
        font-size: 10px;
    }

    @media (max-width: 1200px) {
        div[role="radiogroup"] {
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }
    }

    @media (max-width: 760px) {
        div[role="radiogroup"] {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# APPLICATION HEADER
# ============================================================

st.html("""
<div style="
    position:relative;
    overflow:hidden;
    padding:30px 34px 22px;
    margin-bottom:8px;
    border:1px solid rgba(148,163,184,0.16);
    border-radius:24px;
    background:
        radial-gradient(circle at 92% 15%, rgba(56,189,248,0.20), transparent 24%),
        radial-gradient(circle at 76% 100%, rgba(129,140,248,0.17), transparent 28%),
        linear-gradient(135deg, rgba(12,20,36,0.98), rgba(17,26,48,0.90));
    box-shadow:0 24px 75px rgba(0,0,0,0.24);
">
    <div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap;">
        <div style="
            width:66px;height:66px;display:flex;align-items:center;justify-content:center;
            border-radius:19px;font-size:33px;
            background:linear-gradient(135deg,#0EA5E9,#6366F1);
            box-shadow:0 14px 34px rgba(14,165,233,0.25);
        ">💳</div>

        <div>
            <div style="font-size:31px;line-height:1.08;font-weight:800;letter-spacing:-0.035em;color:#F8FAFC;">
                UPI Fraud Intelligence
            </div>
            <div style="margin-top:8px;font-size:13px;color:#A8B5C7;">
                Transaction Risk &nbsp;•&nbsp; Merchant Analytics &nbsp;•&nbsp; Fraud Investigation
            </div>
        </div>

        <div style="margin-left:auto;">
            <span style="
                display:inline-block;padding:9px 14px;border-radius:999px;
                color:#6EE7B7;background:rgba(16,185,129,0.10);
                border:1px solid rgba(16,185,129,0.25);
                font-size:11px;font-weight:700;letter-spacing:0.04em;
            ">● ANALYTICS READY</span>
        </div>
    </div>

    <div style="margin-top:23px;padding-top:15px;border-top:1px solid rgba(148,163,184,0.12);color:#71809A;font-size:11px;letter-spacing:0.025em;">
        FinTech & BFSI &nbsp;|&nbsp; Explainable Risk Scoring
        &nbsp;|&nbsp; Chargeback Intelligence &nbsp;|&nbsp; Network Analysis
    </div>
</div>
""")

# ============================================================
# NAVIGATION  (top navbar, no sidebar)
# ============================================================

PAGES = [
    "📊 Executive Overview",
    "🔎 Fraud Investigation",
    "🏪 Merchant Intelligence",
    "👤 User Risk Intelligence",
    "🕸️ Fraud Network Analysis",
    "📈 Trends & Analytics",
    "ℹ️ Methodology"
]

# Navigation is presented as a premium segmented web-app bar.
page = st.radio(
    "Navigation",
    PAGES,
    horizontal=True,
    label_visibility="collapsed"
)

# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "📊 Executive Overview":

    page_hero(
        "EXECUTIVE COMMAND CENTER",
        "UPI Fraud & Merchant Analytics",
        "Monitor transaction activity, chargeback exposure, merchant risk and explainable fraud-prioritization signals."
    )

    # --------------------------------------------------------
    # KPI VALUES
    # --------------------------------------------------------

    total_transactions = int(get_kpi("Total Transactions"))
    transaction_value = float(get_kpi("Total Transaction Value"))
    avg_transaction = float(get_kpi("Average Transaction Value"))
    chargebacks = int(get_kpi("Chargeback Transactions"))
    fraud_chargebacks = int(get_kpi("Fraud/Unauthorized Chargeback Transactions"))
    high_risk = int(get_kpi("HIGH Risk Transactions"))
    critical_risk = int(get_kpi("CRITICAL Risk Transactions"))
    high_critical = int(get_kpi("HIGH + CRITICAL Risk Transactions"))

    # --------------------------------------------------------
    # EXECUTIVE KPIs
    # --------------------------------------------------------

    st.subheader("📊 Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Transactions", f"{total_transactions:,}")

    with col2:
        st.metric("Transaction Value", fmt_inr_compact(transaction_value))

    with col3:
        st.metric("Chargeback Transactions", f"{chargebacks:,}")

    with col4:
        st.metric("Fraud/Unauthorized CB", f"{fraud_chargebacks:,}")

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric("Average Transaction", f"₹{avg_transaction:,.0f}")

    with col6:
        st.metric("HIGH Risk", f"{high_risk:,}")

    with col7:
        st.metric("CRITICAL Risk", f"{critical_risk:,}")

    with col8:
        share = (high_critical / total_transactions * 100) if total_transactions else 0
        st.metric(
            "HIGH + CRITICAL",
            f"{high_critical:,}",
            f"{share:.2f}%"
        )

    st.markdown(f"""
    <div style="
        margin:4px 0 18px;
        padding:12px 16px;
        border-radius:14px;
        border:1px solid rgba(56,189,248,0.12);
        background:linear-gradient(90deg, rgba(14,165,233,0.08), rgba(99,102,241,0.05));
        color:#A8B5C7;
        font-size:12px;
    ">
        <b style="color:#F8FAFC;">Risk focus:</b>
        {high_critical:,} transactions ({share:.2f}%) are HIGH or CRITICAL and should receive investigation attention according to the scoring framework.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --------------------------------------------------------
    # DAILY TREND
    # --------------------------------------------------------

    st.markdown("""
    <div style="margin-bottom:10px;color:#64748B;font-size:11px;letter-spacing:0.04em;text-transform:uppercase;">
        Monitoring window • transaction volume • chargeback exposure • high/critical risk activity
    </div>
    """, unsafe_allow_html=True)
    st.subheader("📈 Transaction & Fraud-Risk Trend")

    trend = daily_trend.copy()
    trend["transaction_date"] = pd.to_datetime(
        trend["transaction_date"], errors="coerce"
    )

    trend = safe_numeric(
        trend,
        ["transaction_count", "chargeback_transactions", "high_risk_transactions"]
    )

    trend = (
        trend.dropna(subset=["transaction_date"])
        .sort_values("transaction_date")
        .copy()
    )

    fig_trend = go.Figure()

    fig_trend.add_trace(
        go.Scatter(
            x=trend["transaction_date"],
            y=trend["transaction_count"],
            mode="lines+markers",
            name="Transactions",
            line=dict(width=3),
            marker=dict(size=5),
            hovertemplate="<b>%{x|%d %b %Y}</b><br>Transactions: %{y:,}<extra></extra>"
        )
    )

    fig_trend.add_trace(
        go.Scatter(
            x=trend["transaction_date"],
            y=trend["chargeback_transactions"],
            mode="lines+markers",
            name="Chargebacks",
            line=dict(width=2),
            marker=dict(size=4),
            hovertemplate="<b>%{x|%d %b %Y}</b><br>Chargebacks: %{y:,}<extra></extra>"
        )
    )

    fig_trend.add_trace(
        go.Scatter(
            x=trend["transaction_date"],
            y=trend["high_risk_transactions"],
            mode="lines+markers",
            name="HIGH/CRITICAL Risk",
            line=dict(width=2),
            marker=dict(size=4),
            hovertemplate="<b>%{x|%d %b %Y}</b><br>High/Critical: %{y:,}<extra></extra>"
        )
    )

    fig_trend.update_layout(
        title="Daily Transaction Activity",
        xaxis_title="Date",
        yaxis_title="Transaction Count",
        hovermode="x unified"
    )

    fig_trend.update_xaxes(
        tickformat="%d %b",
        nticks=10,
        rangeslider=dict(
            visible=True,
            thickness=0.055,
            bgcolor="rgba(30,41,59,0.40)",
            bordercolor="rgba(148,163,184,0.15)"
        )
    )

    show_plotly(fig_trend, height=460)

    # --------------------------------------------------------
    # RISK BAND + CATEGORY RISK
    # --------------------------------------------------------

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🚨 Risk Band Distribution")

        risk_counts = (
            investigation_evidence.get("fraud_risk_band", pd.Series(dtype=str))
            .fillna("UNCLASSIFIED")
            .value_counts()
        )
        risk_data = pd.DataFrame({
            "Risk Band": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            "Transactions": [
                int(risk_counts.get("LOW", 0)),
                int(risk_counts.get("MEDIUM", 0)),
                int(risk_counts.get("HIGH", 0)),
                int(risk_counts.get("CRITICAL", 0))
            ]
        })

        fig_risk = px.pie(
            risk_data,
            names="Risk Band",
            values="Transactions",
            hole=0.58,
            title="Fraud Risk Band Distribution",
            color="Risk Band",
            color_discrete_map={
                "LOW": "#34D399",
                "MEDIUM": "#F59E0B",
                "HIGH": "#F97316",
                "CRITICAL": "#F43F5E"
            }
        )

        fig_risk.update_traces(
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>Transactions: %{value:,}<br>"
                "Share: %{percent}<extra></extra>"
            )
        )

        fig_risk.update_layout(
            margin=dict(l=20, r=20, t=60, b=20),
            legend_title_text="Risk Level"
        )

        show_plotly(fig_risk)

    with col_right:
        st.subheader("🏪 Highest-Risk Merchant Categories")

        category_plot = category_intelligence[
            category_intelligence["merchant_category_final"].notna()
            & (category_intelligence["merchant_category_final"] != "NA")
        ].copy()

        category_plot = category_plot.sort_values(
            "chargeback_ratio", ascending=False
        ).head(10)

        fig_category = px.bar(
            category_plot.sort_values("chargeback_ratio"),
            color="chargeback_ratio",
            color_continuous_scale=["#38BDF8", "#6366F1", "#EF4444"],
            x="chargeback_ratio",
            y="merchant_category_final",
            orientation="h",
            text="chargeback_ratio",
            title="Top Categories by Chargeback Ratio",
            hover_data={
                "chargeback_ratio": ":.1%",
                "transaction_count": ":,",
                "chargeback_transactions": ":,",
                "fraud_chargeback_transactions": ":,"
            }
        )

        fig_category.update_traces(
            texttemplate="%{x:.1%}",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Chargeback Ratio: %{x:.1%}<extra></extra>"
        )

        fig_category.update_layout(
            xaxis_tickformat=".0%",
            xaxis_title="Chargeback / Transaction Ratio",
            yaxis_title="Merchant Category",
            margin=dict(l=20, r=40, t=60, b=40)
        )

        fig_category.update_xaxes(showgrid=True, rangemode="tozero")

        show_plotly(fig_category)

    # --------------------------------------------------------
    # CATEGORY RISK MATRIX (volume vs chargeback ratio vs value)
    # --------------------------------------------------------

    st.divider()
    st.subheader("🧭 Category Risk Matrix")

    matrix_data = category_intelligence[
        category_intelligence["merchant_category_final"].notna()
        & (category_intelligence["merchant_category_final"] != "NA")
    ].copy()

    value_col = find_col(
        matrix_data, ["transaction_value", "total_transaction_value"]
    )

    if value_col and "transaction_count" in matrix_data.columns:

        fig_matrix = px.scatter(
            matrix_data,
            color_continuous_scale=["#38BDF8", "#F59E0B", "#EF4444"],
            x="transaction_count",
            y="chargeback_ratio",
            size=value_col,
            color="chargeback_ratio",
            hover_name="merchant_category_final",
            hover_data={
                "transaction_count": ":,",
                "chargeback_ratio": ":.1%",
                value_col: ":,.0f",
                "fraud_chargeback_transactions": ":,"
            },
            title="Category Risk Matrix — Volume vs Chargeback Ratio"
        )

        fig_matrix.update_layout(
            xaxis_title="Transaction Volume",
            yaxis_title="Chargeback Ratio",
            yaxis_tickformat=".0%"
        )

        show_plotly(fig_matrix)

    else:
        st.info(
            "Category-level transaction value is not available in the "
            "current dataset, so the risk matrix bubble size is omitted."
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
        top_category = category_plot.iloc[0]["merchant_category_final"]
        top_ratio = category_plot.iloc[0]["chargeback_ratio"]

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

    page_hero(
        "FRAUD OPERATIONS",
        "Fraud Investigation Workspace",
        "Prioritize suspicious transactions using observable chargeback, identity, velocity and merchant-risk signals."
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
        risk_options = ["ALL", "CRITICAL", "HIGH"]
        selected_risk = st.selectbox("Risk Band", risk_options)

    with col2:
        priority_options = ["ALL"] + sorted(
            investigation["investigation_priority"].dropna().unique().tolist()
        )
        selected_priority = st.selectbox("Investigation Priority", priority_options)

    with col3:
        category_options = ["ALL"] + sorted(
            investigation["merchant_category_final"].dropna().unique().tolist()
        )
        selected_category = st.selectbox("Merchant Category", category_options)

    col4, col5, col6 = st.columns(3)

    with col4:
        min_score = int(
            pd.to_numeric(
                investigation.get("fraud_risk_score", pd.Series([0])),
                errors="coerce"
            ).fillna(0).min()
        )
        max_score = int(
            pd.to_numeric(
                investigation.get("fraud_risk_score", pd.Series([100])),
                errors="coerce"
            ).fillna(0).max()
        )
        if max_score <= min_score:
            max_score = min_score + 1

        min_risk_score = st.slider(
            "Minimum Risk Score",
            min_value=min_score,
            max_value=max_score,
            value=min_score
        )

    with col5:
        search_txn = st.text_input(
            "Search Transaction ID", placeholder="e.g. TXN00011255"
        )

    with col6:
        search_user_merchant = st.text_input(
            "Search User ID / Merchant ID", placeholder="e.g. USR12345 or MCH1234"
        )

    # --------------------------------------------------------
    # APPLY FILTERS
    # --------------------------------------------------------

    filtered = investigation.copy()

    if selected_risk != "ALL":
        filtered = filtered[filtered["fraud_risk_band"] == selected_risk]

    if selected_priority != "ALL":
        filtered = filtered[filtered["investigation_priority"] == selected_priority]

    if selected_category != "ALL":
        filtered = filtered[filtered["merchant_category_final"] == selected_category]

    if "fraud_risk_score" in filtered.columns:
        filtered = filtered[
            pd.to_numeric(filtered["fraud_risk_score"], errors="coerce").fillna(0)
            >= min_risk_score
        ]

    if search_txn.strip():
        s = search_txn.strip()
        filtered = filtered[
            filtered["txn_id"].astype(str).str.contains(s, case=False, na=False)
        ]

    if search_user_merchant.strip():
        s = search_user_merchant.strip()
        mask = (
            filtered["user_id"].astype(str).str.contains(s, case=False, na=False)
            | filtered["merchant_id"].astype(str).str.contains(s, case=False, na=False)
        )
        filtered = filtered[mask]

    # --------------------------------------------------------
    # INVESTIGATION KPIs
    # --------------------------------------------------------

    st.divider()
    st.subheader("🚨 Investigation Summary")

    total_cases = len(filtered)
    critical_cases = len(filtered[filtered["fraud_risk_band"] == "CRITICAL"])
    high_cases = len(filtered[filtered["fraud_risk_band"] == "HIGH"])
    fraud_cases = int(filtered.get("fraud_chargeback_flag", pd.Series(dtype=float)).fillna(0).sum())

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Cases", f"{total_cases:,}")

    with col2:
        st.metric("CRITICAL", f"{critical_cases:,}")

    with col3:
        st.metric("HIGH", f"{high_cases:,}")

    with col4:
        st.metric("Fraud CB Evidence", f"{fraud_cases:,}")

    # --------------------------------------------------------
    # PRIORITY / SCORE BREAKDOWN
    # --------------------------------------------------------

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        priority_counts = (
            filtered["investigation_priority"].value_counts().reset_index()
        )
        priority_counts.columns = ["Priority", "Cases"]

        fig_priority = px.bar(
            priority_counts,
            color="Priority",
            color_discrete_sequence=[CHART_COLORS["primary"], CHART_COLORS["warning"], CHART_COLORS["danger"]],
            x="Priority",
            y="Cases",
            text="Cases",
            title="Investigation Priority Distribution"
        )

        fig_priority.update_traces(textposition="outside")

        show_plotly(fig_priority)

    with col2:
        fig_score = px.histogram(
            filtered,
            x="fraud_risk_score",
            nbins=20,
            title="Risk Score Distribution",
            labels={"fraud_risk_score": "Risk Score"}
        )

        show_plotly(fig_score)

    # --------------------------------------------------------
    # INVESTIGATION TABLE
    # --------------------------------------------------------

    st.divider()
    st.subheader("📋 Investigation Cases")

    display_columns = none_if_empty(filtered, [
        "txn_id", "user_id", "merchant_id", "merchant_name",
        "merchant_category_final", "amount_numeric", "fraud_risk_score",
        "fraud_risk_band", "investigation_priority", "risk_reasons",
        "recommended_action"
    ])

    display_data = filtered[display_columns].copy()

    if "merchant_name" in display_data.columns:
        display_data["merchant_name"] = clean_text_col(
            display_data["merchant_name"], "Unknown Merchant"
        )

    if "merchant_category_final" in display_data.columns:
        display_data["merchant_category_final"] = clean_text_col(
            display_data["merchant_category_final"], "Unclassified"
        )

    if "user_id" in display_data.columns:
        display_data["user_id"] = clean_text_col(
            display_data["user_id"], "Unknown User"
        )

    sort_cols = none_if_empty(display_data, ["fraud_risk_score", "investigation_priority"])
    if sort_cols:
        display_data = display_data.sort_values(
            sort_cols,
            ascending=[False, True][:len(sort_cols)]
        )

    column_config = {}
    if "amount_numeric" in display_data.columns:
        column_config["amount_numeric"] = st.column_config.NumberColumn(
            "Amount", format="₹%.2f"
        )
    if "fraud_risk_score" in display_data.columns:
        column_config["fraud_risk_score"] = st.column_config.NumberColumn(
            "Risk Score", format="%d"
        )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True,
        column_config=column_config
    )

    st.caption(f"Showing {len(display_data):,} investigation cases.")

    csv_bytes = display_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered Cases (CSV)",
        data=csv_bytes,
        file_name="fraud_investigation_cases.csv",
        mime="text/csv"
    )

    st.divider()

    st.info(
        "⚠️ These cases are prioritized using observable risk signals "
        "such as chargebacks, identity anomalies, repeat chargebacks, "
        "velocity anomalies and merchant risk indicators. They should "
        "be treated as investigation leads, not confirmed fraud."
    )


# ============================================================
# MERCHANT INTELLIGENCE
# ============================================================

elif page == "🏪 Merchant Intelligence":

    page_hero(
        "MERCHANT RISK",
        "Merchant Intelligence",
        "Compare merchant exposure, chargeback behavior and fraud-evidence signals while avoiding low-volume distortion."
    )
    st.divider()

    # --------------------------------------------------------
    # MERCHANT FILTERS
    # --------------------------------------------------------

    st.subheader("🎯 Merchant Analysis Filters")

    col1, col2 = st.columns(2)

    with col1:
        min_transactions = st.slider(
            "Minimum Transactions", min_value=1, max_value=10, value=5
        )

    with col2:
        merchant_category_options = ["ALL"] + sorted(
            merchant_intelligence["merchant_category_final"].dropna().unique().tolist()
        )
        selected_merchant_category = st.selectbox(
            "Merchant Category", merchant_category_options
        )

    # --------------------------------------------------------
    # FILTER MERCHANT DATA
    # --------------------------------------------------------

    merchant_data = merchant_intelligence.copy()
    merchant_data = merchant_data[
        merchant_data["transaction_count"] >= min_transactions
    ]

    if selected_merchant_category != "ALL":
        merchant_data = merchant_data[
            merchant_data["merchant_category_final"] == selected_merchant_category
        ]

    # --------------------------------------------------------
    # MERCHANT KPIs
    # --------------------------------------------------------

    merchant_count = len(merchant_data)
    total_merchant_transactions = int(merchant_data["transaction_count"].sum())
    total_merchant_chargebacks = int(merchant_data["chargeback_transactions"].sum())
    total_merchant_fraud = int(merchant_data["fraud_chargeback_transactions"].sum())

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Merchants", f"{merchant_count:,}")

    with col2:
        st.metric("Transactions", f"{total_merchant_transactions:,}")

    with col3:
        st.metric("Chargebacks", f"{total_merchant_chargebacks:,}")

    with col4:
        st.metric("Fraud CB Evidence", f"{total_merchant_fraud:,}")

    st.divider()

    # --------------------------------------------------------
    # TOP MERCHANTS BY CHARGEBACK RATIO
    # --------------------------------------------------------

    st.subheader("🚨 Highest-Risk Merchants")

    top_merchants = merchant_data[
        merchant_data["chargeback_transactions"] >= 2
    ].copy()

    top_merchants = top_merchants.sort_values(
        ["chargeback_ratio", "fraud_chargeback_transactions", "transaction_count"],
        ascending=[False, False, False]
    ).head(15)

    if len(top_merchants) > 0:

        fig_merchants = px.bar(
            top_merchants.sort_values("chargeback_ratio"),
            color="chargeback_ratio",
            color_continuous_scale=["#38BDF8", "#6366F1", "#F97316", "#EF4444"],
            x="chargeback_ratio",
            y="merchant_id",
            orientation="h",
            text="chargeback_ratio",
            hover_data=[
                "merchant_name", "merchant_category_final", "transaction_count",
                "chargeback_transactions", "fraud_chargeback_transactions"
            ],
            title="Top Merchants by Chargeback Ratio"
        )

        fig_merchants.update_traces(texttemplate="%{text:.1%}", textposition="outside")

        fig_merchants.update_layout(
            xaxis_tickformat=".0%",
            xaxis_title="Chargeback / Transaction Ratio",
            yaxis_title="Merchant ID"
        )

        show_plotly(fig_merchants)

    else:
        st.info("No merchants match the selected filters.")

    # --------------------------------------------------------
    # CATEGORY ANALYSIS
    # --------------------------------------------------------

    st.divider()
    st.subheader("📊 Merchant Category Risk")

    category_data = category_intelligence[
        category_intelligence["merchant_category_final"].notna()
        & (category_intelligence["merchant_category_final"] != "NA")
    ].copy()

    category_data = category_data.sort_values("chargeback_ratio", ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        fig_category_ratio = px.bar(
            category_data.head(10).sort_values("chargeback_ratio"),
            color="chargeback_ratio",
            color_continuous_scale=["#38BDF8", "#6366F1", "#EF4444"],
            x="chargeback_ratio",
            y="merchant_category_final",
            orientation="h",
            text="chargeback_ratio",
            title="Top Categories by Chargeback Ratio"
        )

        fig_category_ratio.update_traces(texttemplate="%{text:.1%}", textposition="outside")
        fig_category_ratio.update_layout(
            xaxis_tickformat=".0%", xaxis_title="Chargeback Ratio", yaxis_title="Category"
        )

        show_plotly(fig_category_ratio)

    with col2:
        category_fraud = category_data.sort_values(
            "fraud_chargeback_transactions", ascending=False
        ).head(10)

        fig_category_fraud = px.bar(
            category_fraud.sort_values("fraud_chargeback_transactions"),
            color="fraud_chargeback_transactions",
            color_continuous_scale=["#22D3EE", "#F97316", "#EF4444"],
            x="fraud_chargeback_transactions",
            y="merchant_category_final",
            orientation="h",
            text="fraud_chargeback_transactions",
            title="Categories by Fraud Chargeback Evidence"
        )

        fig_category_fraud.update_traces(textposition="outside")
        fig_category_fraud.update_layout(
            xaxis_title="Fraud/Unauthorized Chargeback Transactions",
            yaxis_title="Category"
        )

        show_plotly(fig_category_fraud)

    # --------------------------------------------------------
    # MERCHANT RISK QUADRANT
    # --------------------------------------------------------

    st.divider()
    st.subheader("🧭 Merchant Risk Quadrant")

    quadrant_data = merchant_data.copy()

    if len(quadrant_data) > 0:

        # Plotly bubble sizes cannot be negative. Some merchant transaction values
        # can be negative (for example, refunds/reversals), so use absolute
        # transaction-value magnitude only for the visual bubble size.
        quadrant_data["transaction_value_size"] = (
            pd.to_numeric(quadrant_data["transaction_value"], errors="coerce")
            .abs()
            .fillna(0)
            .clip(lower=1)
        )

        fig_quadrant = px.scatter(
            quadrant_data,
            color_continuous_scale=["#38BDF8", "#F59E0B", "#EF4444"],
            x="transaction_count",
            y="chargeback_ratio",
            size="transaction_value_size",
            color="fraud_chargeback_transactions",
            hover_data={
                "merchant_id": True,
                "merchant_name": True,
                "merchant_category_final": True,
                "transaction_count": ":,",
                "chargeback_transactions": ":,",
                "fraud_chargeback_transactions": ":,",
                "transaction_value": ":,.0f",
                "chargeback_ratio": ":.1%"
            },
            title="Merchant Risk Quadrant — Volume vs Chargeback Ratio"
        )

        fig_quadrant.update_layout(
            xaxis_title="Transaction Count",
            yaxis_title="Chargeback Ratio",
            yaxis_tickformat=".0%"
        )

        show_plotly(fig_quadrant)

    else:
        st.info("No merchants available to plot with the current filters.")

    st.caption(
        "Bubble size reflects total transaction value. Color reflects "
        "fraud/unauthorized chargeback evidence."
    )

    # --------------------------------------------------------
    # MERCHANT TABLE
    # --------------------------------------------------------

    st.divider()
    st.subheader("📋 Merchant Risk Table")

    merchant_table_columns = [
        "merchant_id", "merchant_name", "merchant_category_final",
        "transaction_count", "transaction_value", "chargeback_transactions",
        "fraud_chargeback_transactions", "high_risk_transactions",
        "chargeback_ratio", "fraud_chargeback_ratio"
    ]

    merchant_table_columns = none_if_empty(merchant_data, merchant_table_columns)

    merchant_table = merchant_data[merchant_table_columns].copy()

    if "merchant_name" in merchant_table.columns:
        merchant_table["merchant_name"] = clean_text_col(
            merchant_table["merchant_name"], "Unknown Merchant"
        )

    if "merchant_category_final" in merchant_table.columns:
        merchant_table["merchant_category_final"] = clean_text_col(
            merchant_table["merchant_category_final"], "Unclassified"
        )

    # Convert ratio columns to a proper percentage scale for display
    for ratio_col in ["chargeback_ratio", "fraud_chargeback_ratio"]:
        if ratio_col in merchant_table.columns:
            merchant_table[ratio_col] = pd.to_numeric(
                merchant_table[ratio_col], errors="coerce"
            ).fillna(0) * 100

    sort_cols = none_if_empty(merchant_table, ["chargeback_ratio", "fraud_chargeback_transactions"])
    if sort_cols:
        merchant_table = merchant_table.sort_values(
            sort_cols, ascending=False
        ).head(100)

    column_config = {}
    if "transaction_value" in merchant_table.columns:
        column_config["transaction_value"] = st.column_config.NumberColumn(
            "Transaction Value", format="₹%.2f"
        )
    if "chargeback_ratio" in merchant_table.columns:
        column_config["chargeback_ratio"] = st.column_config.NumberColumn(
            "Chargeback Ratio (%)", format="%.1f%%"
        )
    if "fraud_chargeback_ratio" in merchant_table.columns:
        column_config["fraud_chargeback_ratio"] = st.column_config.NumberColumn(
            "Fraud CB Ratio (%)", format="%.1f%%"
        )

    st.dataframe(
        merchant_table,
        use_container_width=True,
        hide_index=True,
        column_config=column_config
    )

    st.divider()

    st.info(
        "💡 Merchant rankings use a minimum transaction threshold "
        "to avoid over-interpreting merchants with only one or two "
        "transactions. A high chargeback ratio is a risk signal, "
        "not proof of merchant fraud."
    )


# ============================================================
# USER RISK INTELLIGENCE  (new page — uses previously unused dataset)
# ============================================================

elif page == "👤 User Risk Intelligence":

    page_hero(
        "USER RISK",
        "User Risk Intelligence",
        "Investigate user-level chargeback concentration, identity anomalies and elevated risk signals."
    )
    st.divider()

    users = user_risk_intelligence.copy()

    if len(users) == 0:
        st.info("No user risk data is available in the current dataset.")

    else:

        # ----------------------------------------------------
        # DETECT RELEVANT COLUMNS DEFENSIVELY
        # ----------------------------------------------------

        user_id_col = find_col(users, ["user_id", "customer_id"])
        risk_segment_col = find_col(
            users, ["risk_segment", "user_risk_band", "user_risk_segment", "user_risk_category"]
        )
        risk_score_col = find_col(
            users, ["max_risk_score", "avg_risk_score", "user_risk_score", "total_risk_score"]
        )
        chargeback_col = find_col(users, ["chargeback_transactions", "chargeback_count"])
        fraud_cb_col = find_col(
            users, ["fraud_chargeback_transactions", "fraud_chargeback_count"]
        )
        high_risk_flag_col = find_col(users, ["high_risk_user_flag"])
        identity_conflict_col = find_col(
            users, ["identity_conflict_flag", "identity_conflict_signal"]
        )
        strong_anomaly_col = find_col(users, ["strong_identity_anomaly_flag"])
        repeated_cb_col = find_col(users, ["repeated_chargeback_user_flag"])
        kyc_rejected_col = find_col(users, ["kyc_rejected_transaction_flag", "kyc_status"])

        users = safe_numeric(
            users,
            [c for c in [
                risk_score_col, chargeback_col, fraud_cb_col, high_risk_flag_col,
                identity_conflict_col, strong_anomaly_col, repeated_cb_col
            ] if c]
        )

        # ----------------------------------------------------
        # USER RISK KPIs
        # ----------------------------------------------------

        st.subheader("🚨 User Risk Summary")

        total_users = len(users)

        # Prefer the validated executive KPI for High-Risk Users so the
        # figure matches the rest of the dashboard.
        high_risk_users = int(get_kpi("High-Risk Users", default=None) or 0)
        if not high_risk_users and high_risk_flag_col:
            high_risk_users = int(users[high_risk_flag_col].sum())

        identity_conflicts = (
            int(users[identity_conflict_col].sum()) if identity_conflict_col else None
        )
        strong_anomalies = (
            int(users[strong_anomaly_col].sum()) if strong_anomaly_col else None
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Users", f"{total_users:,}")

        with col2:
            st.metric("High-Risk Users", f"{high_risk_users:,}")

        with col3:
            st.metric(
                "Identity Conflict Signals",
                f"{identity_conflicts:,}" if identity_conflicts is not None else "N/A"
            )

        with col4:
            st.metric(
                "Strong Identity Anomaly Signals",
                f"{strong_anomalies:,}" if strong_anomalies is not None else "N/A"
            )

        st.divider()

        # ----------------------------------------------------
        # RISK SEGMENT DISTRIBUTION
        # ----------------------------------------------------

        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("📊 Risk Segment Distribution")

            if risk_segment_col:
                seg_counts = (
                    users[risk_segment_col]
                    .fillna("Unclassified")
                    .value_counts()
                    .reset_index()
                )
                seg_counts.columns = ["Segment", "Users"]

                fig_seg = px.pie(
                    seg_counts,
                    names="Segment",
                    values="Users",
                    hole=0.5,
                    title="User Risk Segment Distribution"
                )

                fig_seg.update_traces(
                    textinfo="percent",
                    hovertemplate="<b>%{label}</b><br>Users: %{value:,}<extra></extra>"
                )

                show_plotly(fig_seg)

            else:
                st.info(
                    "A risk-segment column was not found in "
                    "powerbi_user_risk_intelligence.csv."
                )

        with col_right:
            st.subheader("🏆 Highest-Risk Users")

            if user_id_col and risk_score_col:
                ranking = users.sort_values(
                    risk_score_col, ascending=False
                ).head(15)

                fig_rank = px.bar(
                    ranking.sort_values(risk_score_col),
                    x=risk_score_col,
                    y=user_id_col,
                    orientation="h",
                    text=risk_score_col,
                    title="User Risk Ranking"
                )

                fig_rank.update_traces(textposition="outside")
                fig_rank.update_layout(
                    xaxis_title="Risk Score", yaxis_title="User ID"
                )

                show_plotly(fig_rank)

            else:
                st.info(
                    "A user ID or risk-score column was not found to "
                    "build a user ranking chart."
                )

        # ----------------------------------------------------
        # CHARGEBACK CONCENTRATION
        # ----------------------------------------------------

        st.divider()
        st.subheader("💳 Chargeback Concentration")

        if user_id_col and chargeback_col:
            top_cb_users = users.sort_values(
                chargeback_col, ascending=False
            ).head(15)

            fig_cb = px.bar(
                top_cb_users.sort_values(chargeback_col),
                x=chargeback_col,
                y=user_id_col,
                orientation="h",
                text=chargeback_col,
                color=fraud_cb_col if fraud_cb_col else None,
                title="Top Users by Chargeback Volume"
            )

            fig_cb.update_traces(textposition="outside")
            fig_cb.update_layout(
                xaxis_title="Chargeback Transactions", yaxis_title="User ID"
            )

            show_plotly(fig_cb)

        else:
            st.info(
                "A user ID or chargeback-count column was not found to "
                "chart chargeback concentration by user."
            )

        # ----------------------------------------------------
        # IDENTITY ANOMALY BREAKDOWN
        # ----------------------------------------------------

        st.divider()
        st.subheader("🪪 Identity & Behavior Signal Breakdown")

        signal_cols = {
            "High-Risk User Flag": high_risk_flag_col,
            "Strong Identity Anomaly": strong_anomaly_col,
            "Repeated Chargeback User": repeated_cb_col,
            "Identity Conflict": identity_conflict_col
        }

        signal_rows = [
            {"Signal": label, "Users": int(users[col].sum())}
            for label, col in signal_cols.items()
            if col is not None
        ]

        if signal_rows:
            signal_df = pd.DataFrame(signal_rows)

            fig_signals = px.bar(
                signal_df.sort_values("Users"),
                x="Users",
                y="Signal",
                orientation="h",
                text="Users",
                title="Identity & Behavior Risk Signals"
            )

            fig_signals.update_traces(textposition="outside")
            show_plotly(fig_signals)

        else:
            st.info(
                "No identity or behavior risk-flag columns were found "
                "in the current user risk dataset."
            )

        st.divider()

        st.info(
            "⚠️ Identity conflicts and anomaly flags are risk signals "
            "derived from observable data-coverage and behavior patterns. "
            "They are not proof of fraud, and missing KYC or merchant "
            "joins reflect data-coverage gaps rather than confirmed risk."
        )


# ============================================================
# FRAUD NETWORK ANALYSIS
# ============================================================

elif page == "🕸️ Fraud Network Analysis":

    page_hero(
        "NETWORK INTELLIGENCE",
        "Suspicious User–Merchant Network Clusters",
        "Surface connected activity patterns that deserve investigation without treating clusters as confirmed fraud rings."
    )
    st.divider()

    # Network KPIs
    network_count = len(suspicious_networks)

    if network_count > 0:

        total_users = int(suspicious_networks["user_count"].sum())
        total_merchants = int(suspicious_networks["merchant_count"].sum())
        total_transactions = int(suspicious_networks["transaction_count"].sum())
        total_fraud_cb = int(suspicious_networks["fraud_chargeback_transactions"].sum())

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Suspicious Networks", f"{network_count:,}")

        with col2:
            st.metric("Users Involved", f"{total_users:,}")

        with col3:
            st.metric("Transactions", f"{total_transactions:,}")

        with col4:
            st.metric("Fraud CB Evidence", f"{total_fraud_cb:,}")

        st.divider()

        # Top suspicious networks
        st.subheader("🚨 Highest-Risk Network Clusters")

        top_networks = suspicious_networks.copy()

        top_networks = safe_numeric(
            top_networks,
            [
                "network_risk_score", "fraud_chargeback_transactions",
                "chargeback_transactions", "chargeback_ratio", "max_risk_score"
            ]
        )

        top_networks = top_networks.sort_values(
            ["network_risk_score", "fraud_chargeback_transactions", "chargeback_transactions"],
            ascending=[False, False, False]
        ).head(15)

        top_networks = top_networks.sort_values("network_risk_score", ascending=True).copy()

        # A direct Graph Objects bar keeps the network ranking reliably visible
        # even when Plotly Express encounters mixed categorical/numeric metadata.
        fig_network = go.Figure(
            go.Bar(
                x=top_networks["network_risk_score"],
                y=top_networks["component_id"].astype(str),
                orientation="h",
                text=top_networks["network_risk_score"],
                texttemplate="%{text:.1f}",
                textposition="outside",
                cliponaxis=False,
                marker=dict(
                    color=top_networks["network_risk_score"],
                    colorscale=[
                        [0.00, "#38BDF8"],
                        [0.45, "#6366F1"],
                        [0.75, "#F97316"],
                        [1.00, "#EF4444"]
                    ],
                    line=dict(
                        color="rgba(255,255,255,0.10)",
                        width=0.6
                    ),
                    showscale=True,
                    colorbar=dict(
                        title="Risk",
                        thickness=10
                    )
                ),
                customdata=top_networks[
                    [
                        "user_count",
                        "merchant_count",
                        "transaction_count",
                        "chargeback_transactions",
                        "fraud_chargeback_transactions",
                        "chargeback_ratio",
                        "max_risk_score"
                    ]
                ].to_numpy(),
                hovertemplate=(
                    "<b>Network %{y}</b><br>"
                    "Network Risk Score: %{x:.1f}<br>"
                    "Users: %{customdata[0]:,}<br>"
                    "Merchants: %{customdata[1]:,}<br>"
                    "Transactions: %{customdata[2]:,}<br>"
                    "Chargebacks: %{customdata[3]:,}<br>"
                    "Fraud CB Evidence: %{customdata[4]:,}<br>"
                    "Chargeback Ratio: %{customdata[5]:.1%}<br>"
                    "Max Transaction Risk: %{customdata[6]:.0f}"
                    "<extra></extra>"
                )
            )
        )

        fig_network.update_layout(
            title="Top Suspicious Network Clusters by Risk Score",
            xaxis_title="Network Risk Score",
            yaxis_title="Network Component",
            xaxis=dict(rangemode="tozero"),
            height=540,
            margin=dict(l=75, r=90, t=70, b=55),
            bargap=0.22
        )

        show_plotly(fig_network, height=540)

        # Network characteristics
        st.divider()
        st.subheader("📊 Network Characteristics")

        col1, col2 = st.columns(2)

        with col1:
            fig_users = px.scatter(
                suspicious_networks,
                x="user_count",
                y="merchant_count",
                size="transaction_count",
                color="chargeback_ratio",
                color_continuous_scale=["#38BDF8", "#6366F1", "#F97316", "#EF4444"],
                hover_data=[
                    "component_id", "transaction_count",
                    "fraud_chargeback_transactions", "network_risk_score"
                ],
                title="Users vs Merchants in Suspicious Networks"
            )

            fig_users.update_layout(xaxis_title="Users", yaxis_title="Merchants")

            show_plotly(fig_users)

        with col2:
            fig_chargebacks = px.scatter(
                suspicious_networks,
                x="transaction_count",
                y="chargeback_transactions",
                size="fraud_chargeback_transactions",
                color="network_risk_score",
                color_continuous_scale=["#38BDF8", "#6366F1", "#EF4444"],
                hover_data=[
                    "component_id", "user_count", "merchant_count", "chargeback_ratio"
                ],
                title="Transaction Activity vs Chargebacks"
            )

            fig_chargebacks.update_layout(
                xaxis_title="Transactions", yaxis_title="Chargeback Transactions"
            )

            show_plotly(fig_chargebacks)

        # Network Risk vs Chargeback Ratio
        st.divider()
        st.subheader("🔬 Network Risk vs Chargeback Ratio")

        fig_risk_ratio = px.scatter(
            suspicious_networks,
            x="chargeback_ratio",
            y="network_risk_score",
            size="transaction_count",
            color="fraud_chargeback_transactions",
            color_continuous_scale=["#22D3EE", "#F59E0B", "#EF4444"],
            hover_data=[
                "component_id", "user_count", "merchant_count",
                "transaction_count", "max_risk_score"
            ],
            title="Network Risk Score vs Chargeback Ratio"
        )

        fig_risk_ratio.update_layout(
            xaxis_title="Chargeback Ratio",
            xaxis_tickformat=".0%",
            yaxis_title="Network Risk Score"
        )

        show_plotly(fig_risk_ratio)

        # Network table
        st.divider()
        st.subheader("📋 Suspicious Network Details")

        network_table_columns = [
            "component_id", "user_count", "merchant_count", "transaction_count",
            "transaction_value", "chargeback_transactions",
            "fraud_chargeback_transactions", "chargeback_ratio",
            "max_risk_score", "network_risk_score"
        ]

        network_table = suspicious_networks[network_table_columns].copy()

        network_table["chargeback_ratio"] = pd.to_numeric(
            network_table["chargeback_ratio"], errors="coerce"
        ).fillna(0) * 100

        network_table = network_table.sort_values(
            "network_risk_score", ascending=False
        ).head(50)

        st.dataframe(
            network_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "transaction_value": st.column_config.NumberColumn(
                    "Transaction Value", format="₹%.2f"
                ),
                "chargeback_ratio": st.column_config.NumberColumn(
                    "Chargeback Ratio (%)", format="%.1f%%"
                ),
                "max_risk_score": st.column_config.NumberColumn(
                    "Max Risk Score", format="%.0f"
                ),
                "network_risk_score": st.column_config.NumberColumn(
                    "Network Risk Score", format="%.1f"
                )
            }
        )

        st.divider()

        st.info(
            "⚠️ These are suspicious transaction networks identified "
            "from shared user–merchant activity and risk signals. "
            "They should be treated as investigation leads, not "
            "confirmed fraud rings."
        )

    else:
        st.info("No suspicious network clusters are available.")


# ============================================================
# TRENDS & ANALYTICS  (new page — daily_trend + chargeback_analytics)
# ============================================================

elif page == "📈 Trends & Analytics":

    page_hero(
        "ANALYTICS",
        "Trends & Analytics",
        "Explore transaction, value, chargeback and risk behavior across the available time series."
    )
    st.markdown("### Time-based transaction and chargeback analytics")
    st.caption(
        "Explore how transaction activity, chargebacks and risk "
        "evolve over time. Aggregation is computed from the existing "
        "daily transaction dataset — no historical data is invented."
    )
    st.divider()

    trend = daily_trend.copy()
    trend["transaction_date"] = pd.to_datetime(trend["transaction_date"], errors="coerce")
    trend = trend.dropna(subset=["transaction_date"]).sort_values("transaction_date")

    numeric_candidates = [
        "transaction_count", "chargeback_transactions", "high_risk_transactions"
    ]

    value_col = find_col(trend, ["transaction_value", "total_transaction_value"])
    fraud_cb_trend_col = find_col(
        trend, ["fraud_chargeback_transactions", "fraud_cb_transactions"]
    )

    numeric_cols_present = none_if_empty(
        trend, numeric_candidates + ([value_col] if value_col else []) + ([fraud_cb_trend_col] if fraud_cb_trend_col else [])
    )

    trend = safe_numeric(trend, numeric_cols_present)

    # --------------------------------------------------------
    # CONTROLS
    # --------------------------------------------------------

    st.subheader("🎛️ Analysis Controls")

    col1, col2 = st.columns(2)

    with col1:
        agg_choice = st.selectbox(
            "Aggregation", ["Daily", "Weekly", "Monthly"]
        )

    with col2:
        min_date = trend["transaction_date"].min()
        max_date = trend["transaction_date"].max()

        date_range = st.slider(
            "Date Range",
            min_value=min_date.to_pydatetime(),
            max_value=max_date.to_pydatetime(),
            value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
            format="DD MMM"
        )

    filtered_trend = trend[
        (trend["transaction_date"] >= date_range[0])
        & (trend["transaction_date"] <= date_range[1])
    ].copy()

    freq_map = {"Daily": "D", "Weekly": "W", "Monthly": "M"}

    if agg_choice != "Daily":
        agg_dict = {c: "sum" for c in numeric_cols_present}
        filtered_trend = (
            filtered_trend
            .set_index("transaction_date")
            .resample(freq_map[agg_choice])
            .agg(agg_dict)
            .reset_index()
        )

    st.divider()

    # --------------------------------------------------------
    # TRANSACTION VOLUME TREND
    # --------------------------------------------------------

    st.subheader("📊 Transaction Volume Trend")

    fig_vol = go.Figure()
    fig_vol.add_trace(
        go.Scatter(
            x=filtered_trend["transaction_date"],
            y=filtered_trend["transaction_count"],
            mode="lines+markers",
            name="Transactions",
            line=dict(width=3),
            hovertemplate="<b>%{x|%d %b %Y}</b><br>Transactions: %{y:,}<extra></extra>"
        )
    )
    fig_vol.update_layout(
        title=f"{agg_choice} Transaction Volume",
        xaxis_title="Date",
        yaxis_title="Transactions",
        hovermode="x unified"
    )
    show_plotly(fig_vol)

    # --------------------------------------------------------
    # VALUE TREND (if available)
    # --------------------------------------------------------

    if value_col:
        st.subheader("💰 Transaction Value Trend")

        fig_val = go.Figure()
        fig_val.add_trace(
            go.Scatter(
                x=filtered_trend["transaction_date"],
                y=filtered_trend[value_col],
                mode="lines+markers",
                name="Transaction Value",
                line=dict(width=3, color="#38BDF8"),
                hovertemplate="<b>%{x|%d %b %Y}</b><br>Value: ₹%{y:,.0f}<extra></extra>"
            )
        )
        fig_val.update_layout(
            title=f"{agg_choice} Transaction Value",
            xaxis_title="Date",
            yaxis_title="Transaction Value (₹)"
        )
        show_plotly(fig_val)

    # --------------------------------------------------------
    # CHARGEBACK & RISK TRENDS
    # --------------------------------------------------------

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🔁 Chargeback Trend")

        fig_cb = go.Figure()
        fig_cb.add_trace(
            go.Scatter(
                x=filtered_trend["transaction_date"],
                y=filtered_trend["chargeback_transactions"],
                mode="lines+markers",
                name="Chargebacks",
                line=dict(width=2, color="#F87171")
            )
        )
        fig_cb.update_layout(
            title=f"{agg_choice} Chargeback Trend",
            xaxis_title="Date",
            yaxis_title="Chargebacks"
        )
        show_plotly(fig_cb)

    with col_right:
        st.subheader("⚠️ HIGH/CRITICAL Risk Trend")

        fig_hr = go.Figure()
        fig_hr.add_trace(
            go.Scatter(
                x=filtered_trend["transaction_date"],
                y=filtered_trend["high_risk_transactions"],
                mode="lines+markers",
                name="HIGH/CRITICAL Risk",
                line=dict(width=2, color="#A78BFA")
            )
        )
        fig_hr.update_layout(
            title=f"{agg_choice} HIGH/CRITICAL Risk Trend",
            xaxis_title="Date",
            yaxis_title="Transactions"
        )
        show_plotly(fig_hr)

    if fraud_cb_trend_col:
        st.subheader("🚩 Fraud Chargeback Evidence Trend")

        fig_fraud = go.Figure()
        fig_fraud.add_trace(
            go.Scatter(
                x=filtered_trend["transaction_date"],
                y=filtered_trend[fraud_cb_trend_col],
                mode="lines+markers",
                name="Fraud CB Evidence",
                line=dict(width=2, color="#FBBF24")
            )
        )
        fig_fraud.update_layout(
            title=f"{agg_choice} Fraud Chargeback Evidence Trend",
            xaxis_title="Date",
            yaxis_title="Transactions"
        )
        show_plotly(fig_fraud)
    else:
        st.caption(
            f"Fraud/unauthorized chargeback evidence total across the "
            f"full dataset: **{int(get_kpi('Fraud/Unauthorized Chargeback Transactions')):,}**. "
            "A day-level breakdown of this metric is not available in "
            "the current daily-trend dataset."
        )

    # --------------------------------------------------------
    # CHARGEBACK ANALYTICS (reason / severity breakdowns, if available)
    # --------------------------------------------------------

    st.divider()
    st.subheader("🧾 Chargeback Reason & Severity Analytics")

    cb = chargeback_analytics.copy()

    reason_col = find_col(cb, ["chargeback_reason", "reason_code", "dispute_reason"])
    severity_col = find_col(cb, ["severity", "dispute_severity", "severity_level"])
    resolution_col = find_col(cb, ["resolution_status", "status", "dispute_status"])

    if reason_col or severity_col or resolution_col:

        chart_cols = st.columns(sum(bool(c) for c in [reason_col, severity_col, resolution_col]))
        idx = 0

        if reason_col:
            with chart_cols[idx]:
                reason_counts = cb[reason_col].fillna("Unknown").value_counts().reset_index()
                reason_counts.columns = ["Reason", "Count"]

                fig_reason = px.bar(
                    reason_counts.sort_values("Count").tail(10),
                    x="Count", y="Reason", orientation="h",
                    title="Chargeback Reason Distribution"
                )
                show_plotly(fig_reason)
            idx += 1

        if severity_col:
            with chart_cols[idx]:
                sev_counts = cb[severity_col].fillna("Unknown").value_counts().reset_index()
                sev_counts.columns = ["Severity", "Count"]

                fig_sev = px.pie(
                    sev_counts, names="Severity", values="Count", hole=0.5,
                    title="Dispute Severity Distribution"
                )
                show_plotly(fig_sev)
            idx += 1

        if resolution_col:
            with chart_cols[idx]:
                res_counts = cb[resolution_col].fillna("Unknown").value_counts().reset_index()
                res_counts.columns = ["Resolution", "Count"]

                fig_res = px.bar(
                    res_counts.sort_values("Count"),
                    x="Count", y="Resolution", orientation="h",
                    title="Resolution Status Distribution"
                )
                show_plotly(fig_res)

    else:
        st.info(
            "Reason, severity or resolution-status columns were not "
            "found in powerbi_chargeback_analytics.csv, so this "
            "breakdown is not shown."
        )

    st.divider()

    st.caption(
        "Trend charts are computed directly from the existing processed "
        "datasets. No historical values are estimated or fabricated."
    )


# ============================================================
# METHODOLOGY
# ============================================================

elif page == "ℹ️ Methodology":

    page_hero(
        "METHOD & GOVERNANCE",
        "Methodology",
        "Understand the data pipeline, explainable risk framework and analytical limitations behind the dashboard."
    )
    st.markdown("### How this analytics platform is built")
    st.caption(
        "An explainable, auditable pipeline from raw UPI transaction "
        "logs to investigation-ready fraud intelligence."
    )
    st.divider()

    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    st.subheader("🔗 Data & Analytics Pipeline")

    pipeline_steps = [
        "RAW DATA", "DATA CLEANING", "ENTITY NORMALIZATION",
        "TRANSACTION ENRICHMENT", "IDENTITY ANALYTICS",
        "MERCHANT ANALYTICS", "RISK SCORING",
        "INVESTIGATION PRIORITIZATION", "NETWORK ANALYSIS"
    ]

    pipeline_html = "<div class='upi-pipeline'>"
    for i, step in enumerate(pipeline_steps):
        pipeline_html += f"<div class='upi-pipeline-node'>{step}</div>"
        if i < len(pipeline_steps) - 1:
            pipeline_html += "<div class='upi-pipeline-arrow'>→</div>"
    pipeline_html += "</div>"

    st.markdown(pipeline_html, unsafe_allow_html=True)

    st.divider()

    # --------------------------------------------------------
    # RISK SCORING FRAMEWORK
    # --------------------------------------------------------

    st.subheader("🧮 Explainable Risk Scoring Framework")

    st.markdown(
        "The **fraud risk score** is an explainable, "
        "investigation-prioritization score built from weighted "
        "observable evidence flags. **It is not a fraud probability.**"
    )

    weights = pd.DataFrame([
        {"Risk Flag": "Fraud Chargeback Evidence", "Weight": 30},
        {"Risk Flag": "Chargeback Flag", "Weight": 15},
        {"Risk Flag": "Strong Identity Anomaly", "Weight": 15},
        {"Risk Flag": "Repeated Chargeback User", "Weight": 10},
        {"Risk Flag": "High Chargeback Merchant", "Weight": 10},
        {"Risk Flag": "High-Risk User", "Weight": 5},
        {"Risk Flag": "KYC Rejected Transaction", "Weight": 5},
        {"Risk Flag": "Velocity Anomaly", "Weight": 5},
        {"Risk Flag": "High-Value Transaction", "Weight": 3},
        {"Risk Flag": "Merchant Status Risk", "Weight": 2},
    ])

    col_left, col_right = st.columns([3, 2])

    with col_left:
        fig_weights = px.bar(
            weights.sort_values("Weight"),
            x="Weight", y="Risk Flag", orientation="h",
            text="Weight", title="Risk Scoring Weights"
        )
        fig_weights.update_traces(textposition="outside")
        show_plotly(fig_weights, height=420)

    with col_right:
        st.markdown("**Risk Bands**")

        bands = pd.DataFrame([
            {"Score Range": "0 – 19", "Band": "LOW"},
            {"Score Range": "20 – 39", "Band": "MEDIUM"},
            {"Score Range": "40 – 59", "Band": "HIGH"},
            {"Score Range": "60+", "Band": "CRITICAL"},
        ])
        st.dataframe(bands, hide_index=True, use_container_width=True)

        st.markdown(
            "<div class='upi-method-card' style='margin-top:12px;'>"
            "<h4>Interpretation</h4>"
            "<p>Higher scores indicate more observable risk evidence "
            "accumulated on a transaction — they prioritize which "
            "cases an analyst should look at first, not a statement "
            "of certainty that fraud occurred.</p>"
            "</div>",
            unsafe_allow_html=True
        )

    st.divider()

    # --------------------------------------------------------
    # LIMITATIONS
    # --------------------------------------------------------

    st.subheader("📌 Analytical Limitations & Definitions")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "<div class='upi-method-card'>"
            "<h4>Unmatched Joins</h4>"
            "<p>Missing KYC or merchant joins reflect data-coverage "
            "gaps in the underlying datasets — they are not treated "
            "as automatic evidence of fraud.</p>"
            "</div>",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<div class='upi-method-card'>"
            "<h4>Identity Anomalies</h4>"
            "<p>Identity conflicts (e.g. inconsistent identifiers) are "
            "risk signals used for prioritization, not proof of "
            "identity fraud.</p>"
            "</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            "<div class='upi-method-card'>"
            "<h4>Chargeback Evidence</h4>"
            "<p>Chargeback and dispute records represent observable "
            "evidence of a disputed transaction, independent of the "
            "explainable risk score.</p>"
            "</div>",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<div class='upi-method-card'>"
            "<h4>Suspicious Network Clusters</h4>"
            "<p>Because the data has no direct receiver_user_id field, "
            "connected user–merchant clusters are <b>investigation "
            "leads</b>, not confirmed fraud rings or proven directed "
            "cycles.</p>"
            "</div>",
            unsafe_allow_html=True
        )

    st.divider()

    st.caption(
        "This methodology page summarizes the fixed business logic "
        "of the analytics pipeline. It does not display computed "
        "metrics — those live on the Executive Overview, Fraud "
        "Investigation, Merchant Intelligence, User Risk Intelligence "
        "and Fraud Network Analysis pages."
    )


# ============================================================
# PROFESSIONAL FOOTER  (renders on every page)
# ============================================================

st.html("""
<div class="upi-footer">
    <div class="upi-footer-title">
        💳 UPI Fraud Intelligence Platform
    </div>

    <div class="upi-footer-subtitle">
        FinTech & BFSI &nbsp;•&nbsp; Fraud Detection
        &nbsp;•&nbsp; Merchant Analytics &nbsp;•&nbsp; Network Intelligence
    </div>

    <div class="upi-footer-line"></div>

    <div class="upi-footer-tech">
        Built with Python &nbsp;•&nbsp; Pandas &nbsp;•&nbsp; Plotly &nbsp;•&nbsp; Streamlit
    </div>

    <div class="upi-footer-note">
        Risk scores are investigation-prioritization signals based on
        observable evidence, not confirmed fraud probabilities.
    </div>

    <div class="upi-footer-copy">
        © 2026 UPI Fraud Intelligence &nbsp;•&nbsp; Datathon Project
    </div>
</div>
""")


# ============================================================
# FLOATING AI CHATBOT: FRAUDIQ COPILOT
# ============================================================

render_copilot(
    executive_kpis=executive_kpis,
    daily_trend=daily_trend,
    merchant_intelligence=merchant_intelligence,
    category_intelligence=category_intelligence,
    user_risk_intelligence=user_risk_intelligence,
    chargeback_analytics=chargeback_analytics,
    investigation_evidence=investigation_evidence,
    suspicious_networks=suspicious_networks
)
