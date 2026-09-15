# UPI Fraud Ring and Merchant Analytics
A Streamlit-based fraud analytics dashboard for studying UPI transactions, chargebacks, merchant risk, user risk, and suspicious transaction networks.
About the Project
We built this project to answer a simple question:
How can we quickly identify transactions and entities that need further investigation?
We worked with transaction, KYC, merchant, and chargeback data. After cleaning and validating the data, we created risk indicators and an explainable risk score. These results are shown through an interactive dashboard.
The system is meant to support investigation. A high risk score does not mean that fraud is confirmed.
Main Features
Executive Overview
Shows the main transaction, chargeback, and risk KPIs.
Fraud Investigation
Helps filter and review high-priority transactions and their risk signals.
Merchant Intelligence
Shows merchant activity, chargeback ratios, fraud evidence, and merchant categories.
User Risk Intelligence
Shows user-level risk, KYC issues, and identity-related risk signals.
Fraud Network Analysis
Looks at connected user–merchant activity and highlights suspicious network clusters for investigation.
Trends & Analytics
Shows how transactions, chargebacks, and risk indicators change over time.
Methodology
Explains the data preparation and risk-scoring approach used in the project.
Key Results
Metric	Value
Total transactions	20,000
Total transaction value	₹214.06M
Average transaction value	₹11,893
Successful transactions	17,053
Failed transactions	1,955
Pending transactions	992
Chargeback transactions	2,451
Fraud/unauthorized chargeback evidence	873
High-value transactions	879
High-risk users	686
HIGH-risk transactions	788
CRITICAL-risk transactions	94
HIGH + CRITICAL transactions	882
Risk Scoring
We used a weighted scoring method based on observable risk signals.
Some of the main signals are:
Signal	Weight
Fraud/Unauthorized chargeback	+30
Chargeback	+15
Strong identity anomaly	+15
Repeated chargeback user	+10
High-chargeback merchant	+10
High-risk user	+5
KYC rejected/failed transaction	+5
Velocity anomaly	+5
High-value transaction	+3
Merchant status risk	+2
Risk Bands
LOW: 0–19
MEDIUM: 20–39
HIGH: 40–59
CRITICAL: 60+
The score is used to prioritize investigations. It is not a fraud probability.
Data Validation
We kept unmatched records instead of removing them so that data-coverage problems remained visible.
Join	Match Rate
Transaction → KYC	31.18%
Transaction → Merchant	46.38%
Chargeback → Transaction	93.11%
Chargeback → KYC	28.82%
Chargeback → Merchant	42.82%
These match rates should not be treated as fraud indicators.
FraudIQ Copilot
The dashboard also includes FraudIQ Copilot, a small project assistant that works with the project's local data and definitions.
It can answer questions such as:
```text
How many HIGH and CRITICAL transactions are there?
What is the risk scoring methodology?
Which merchants are highest risk?
How does the Merchant Risk Quadrant work?
How were suspicious networks identified?
Explain this project for my viva.
```
Technology
Python
Pandas
NumPy
Streamlit
Plotly
Jupyter Notebook
Git & GitHub
Project Structure
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
└── README.md
```
Run the Project
Clone the repository:
```bash
git clone https://github.com/vikashkatiki/UPI-Fraud-Ring-Merchant-Analytics.git
cd UPI-Fraud-Ring-Merchant-Analytics
```
Install the dependencies:
```bash
pip install -r requirements.txt
```
Run the dashboard:
```bash
python -m streamlit run app/app.py
```
Open:
```text
http://localhost:8501
```
Limitations
This is a project-level fraud analytics solution, not a production fraud detection system.
The main limitations are:
Some KYC and merchant joins are incomplete.
The risk weights are designed for this project.
HIGH and CRITICAL do not mean confirmed fraud.
Suspicious network clusters need human investigation.
The scoring framework would need further validation with labelled real-world fraud data.
Future Improvements
With more time, we would like to:
Validate the risk weights with labelled data
Add more behavioural features
Improve network-based analysis
Add stronger model validation
Add better monitoring and audit features
Links
GitHub:  
https://github.com/vikashkatiki/UPI-Fraud-Ring-Merchant-Analytics
Live Dashboard:  
https://upi-fraud-ring-merchant-analytics--datasena.streamlit.app
Team
This project was developed as a team submission for the FinTech & BFSI — UPI Fraud Ring & Merchant Analytics track.
Disclaimer
This project provides investigation-prioritisation signals. It does not prove that a transaction, user, merchant, or network is fraudulent.
