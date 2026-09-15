# UPI Fraud Ring & Merchant Analytics

An explainable fraud-intelligence platform for analysing UPI transaction activity, chargebacks, merchant risk, user behaviour, and suspicious transaction networks.

Built for the **FinTech & BFSI** track, this project brings together data engineering, risk analytics, network analysis, and an interactive Streamlit dashboard into one workflow designed for practical fraud investigation.

---

## Why this project?

Fraud teams rarely have the time to investigate every transaction manually. The challenge is to identify the transactions, users, merchants, and connected activity that deserve attention first — and to explain why they were prioritised.

This project addresses that problem by combining multiple observable signals such as:

- chargebacks and unauthorized-transaction evidence
- repeated chargeback behaviour
- identity anomalies
- KYC failures
- transaction velocity
- high-value activity
- merchant risk indicators
- user and merchant relationships

Instead of treating a single signal as proof of fraud, the platform combines them into an **explainable risk score** that helps investigators focus on the strongest leads.

> **Important:** The risk score is an investigation-prioritisation mechanism, not a probability of fraud. HIGH and CRITICAL records are investigation leads, not automatically confirmed fraud.

---

## What the dashboard provides

The application is organised as a fraud-intelligence workspace rather than a collection of isolated charts.

### Executive Overview
A high-level command centre for monitoring transaction volume, transaction value, chargebacks, fraud evidence, and overall risk exposure.

### Fraud Investigation
A focused workspace for reviewing high-priority cases, understanding the signals behind their risk scores, and filtering investigation evidence.

### Merchant Intelligence
A deeper look at merchant behaviour, transaction concentration, chargeback exposure, fraud evidence, and category-level risk.

### User Risk Intelligence
User and KYC-focused analysis covering high-risk users, identity anomalies, repeated chargeback behaviour, and related risk indicators.

### Fraud Network Analysis
A relationship view of users and merchants designed to surface suspicious connected activity and rank network components for further investigation.

### Trends & Analytics
Time-based analysis of transaction activity, chargebacks, and risk signals to help identify changing patterns.

### Methodology
A transparent explanation of the data preparation process, risk framework, assumptions, and interpretation guidelines.

---

## Key results

The current analytical layer contains:

| Metric | Result |
|---|---:|
| Transactions | **20,000** |
| Total transaction value | **₹214.06M** |
| Average transaction value | **₹11,893** |
| Successful transactions | **17,053** |
| Failed transactions | **1,955** |
| Pending transactions | **992** |
| Chargeback transactions | **2,451** |
| Fraud/unauthorized chargeback evidence | **873** |
| High-value transactions | **879** |
| High-risk users | **686** |
| KYC rejected/failed transaction records | **491** |
| Risky merchant-status transaction records | **738** |
| HIGH-risk transactions | **788** |
| CRITICAL-risk transactions | **94** |
| HIGH + CRITICAL transactions | **882** |
| HIGH + CRITICAL share | **4.41%** |

These figures are based on the project's processed analytical datasets.

---

## Explainable risk scoring

A key design decision in this project was to make the risk score understandable rather than treating it as a black box.

Each transaction receives points for observable risk signals:

| Risk signal | Weight |
|---|---:|
| Fraud/Unauthorized chargeback | +30 |
| Chargeback | +15 |
| Strong identity anomaly | +15 |
| Repeated chargeback user | +10 |
| High-chargeback merchant | +10 |
| High-risk user | +5 |
| KYC rejected/failed transaction | +5 |
| Velocity anomaly | +5 |
| High-value transaction | +3 |
| Merchant status risk | +2 |

### Risk bands

| Score | Risk band |
|---:|---|
| 0–19 | LOW |
| 20–39 | MEDIUM |
| 40–59 | HIGH |
| 60+ | CRITICAL |

This scoring framework is intended to answer two questions:

1. **Which records should investigators look at first?**
2. **What observable signals contributed to that priority?**

It is deliberately not presented as a fraud-probability model.

---

## Data preparation and validation

The project follows a structured analytical workflow:

```text
Raw Data
   ↓
Data Understanding
   ↓
Cleaning & Standardisation
   ↓
Join Validation
   ↓
Feature / Risk Signal Engineering
   ↓
Explainable Risk Scoring
   ↓
Merchant / User / Chargeback / Network Intelligence
   ↓
Interactive Dashboard
```

The main source tables are transactions, KYC, merchants, and chargebacks.

### Join validation

Unmatched records are preserved so that data-quality limitations remain visible instead of being silently discarded.

| Join | Match rate |
|---|---:|
| Transaction → KYC | **31.18%** |
| Transaction → Merchant | **46.38%** |
| Chargeback → Transaction | **93.11%** |
| Chargeback → KYC | **28.82%** |
| Chargeback → Merchant | **42.82%** |

These match rates represent **data coverage**, not evidence of fraud.

---

## Suspicious network analysis

The project also examines shared user–merchant activity as a graph.

The network layer is used to identify connected components with combinations of signals such as:

- transaction concentration
- chargebacks
- fraud/unauthorized chargeback evidence
- risk scores
- user and merchant participation

The goal is to surface **network-level investigation leads** that may not be obvious from transaction-level analysis alone.

> A suspicious network component is not automatically a fraud ring. It requires analyst validation and additional evidence.

---

## FraudIQ Copilot

The dashboard includes **FraudIQ Copilot**, a floating project assistant designed specifically for this application.

The current implementation uses a **local project-intelligence engine**, so it does not depend on a paid external AI API.

It can answer questions such as:

```text
How many HIGH and CRITICAL transactions are there?

Explain the risk scoring methodology.

Which merchants are highest risk?

How does the Merchant Risk Quadrant work?

How were suspicious networks identified?

What are the key project metrics?

Explain this project for my viva.
```

The assistant is grounded in the project's analytical data and definitions and is designed to avoid presenting unsupported values as facts.

---

## Technology stack

**Data & analytics**
- Python
- Pandas
- NumPy
- Jupyter Notebook

**Dashboard & visualization**
- Streamlit
- Plotly

**Development & version control**
- VS Code / Antigravity IDE
- Git
- GitHub

---

## Repository structure

```text
UPI-Fraud-Ring-Merchant-Analytics/
│
├── app/
│   ├── app.py
│   └── copilot.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── Data_Cleaning.ipynb
│   ├── Data_understanding.ipynb
│   └── fraud_analytics.ipynb
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/vikashkatiki/UPI-Fraud-Ring-Merchant-Analytics.git
cd UPI-Fraud-Ring-Merchant-Analytics
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts ctivate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the dashboard

```bash
python -m streamlit run app/app.py
```

Open:

```text
http://localhost:8501
```

---

## Deployment

The application is deployed with **Streamlit Community Cloud**.

Current deployment configuration:

```text
Repository: vikashkatiki/UPI-Fraud-Ring-Merchant-Analytics
Branch: main
Entry point: app/app.py
```

The processed datasets are part of the repository because the dashboard loads them when the application starts.

---

## Project limitations

This solution is intended as an **analytics and investigation-support platform**, not as a production fraud-decision engine.

Some important limitations are:

- KYC and merchant join coverage is incomplete.
- The risk framework is rule-based and project-specific.
- Risk scores should not be interpreted as fraud probabilities.
- Suspicious network structures require human validation.
- Thresholds and weights would need calibration against labelled outcomes in a production setting.
- A production system would require stronger monitoring, model governance, access control, audit logging, and security controls.

---

## Business value

The project is designed to help fraud and risk teams move from broad monitoring to focused investigation.

It can help answer questions such as:

- Which transactions deserve attention first?
- Which merchants have disproportionate chargeback exposure?
- Which users show multiple risk signals?
- Where are identity or velocity anomalies concentrated?
- Which connected user–merchant groups deserve investigation?
- Why was a transaction prioritised?

The underlying idea is simple:

```text
Observe → Measure → Prioritise → Investigate → Explain
```

---

## Project objective

The final goal is to build an investigation workflow where fraud analysts can move from **raw transaction data to explainable risk signals and actionable investigation leads** through a single, interactive interface.

---

## Links

**GitHub Repository**  
https://github.com/vikashkatiki/UPI-Fraud-Ring-Merchant-Analytics

**Live Dashboard**  
_Add your Streamlit deployment URL here._

---

## Team

Developed as a team project for the **FinTech & BFSI — UPI Fraud Ring & Merchant Analytics** datathon track.

---

## Disclaimer

This project provides analytical insights and investigation-prioritisation signals. It does **not** establish that a transaction, user, merchant, or network is fraudulent.
