# Revenue Recovery & Decision Intelligence Platform

An AI-powered SaaS customer risk and revenue recovery platform that transforms customer usage, subscription, and support data into actionable retention decisions.

---

## 🚀 Overview

SaaS companies often know which customers are at risk of churning, but identifying **which customers require immediate attention** and **what action should be taken** is a harder business problem.

This project combines:

- Customer churn prediction
- Revenue-at-risk estimation
- Rule-based decision intelligence
- Customer-level risk investigation
- AI-powered business analysis
- Interactive Streamlit dashboards

The platform converts raw SaaS customer data into a prioritized list of customers and recommended retention actions.

---

## 🎯 Problem Statement

Customer churn can directly affect recurring SaaS revenue.

A traditional churn model answers:

> "Which customers are likely to churn?"

This platform goes further and answers:

> "Which customers should the business prioritize, how much revenue is exposed, and what action should be taken?"

The system therefore combines **machine learning + business rules + generative AI** into a single decision-support platform.

---

## 💡 Solution

The platform follows this workflow:

```text
RavenStack SaaS Data
        │
        ▼
Data Preparation & Temporal Filtering
        │
        ▼
Customer Feature Engineering
        │
        ▼
Churn Risk Model
        │
        ▼
Churn Probability
        │
        ▼
Revenue at Risk
        │
        ▼
Recovery / Retention Decision Engine
        │
        ├── Priority
        │
        └── Recommended Action
        │
        ▼
AI Assistant + Dashboard
```

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │   RavenStack Data    │
                    │ Accounts / Usage /   │
                    │ Support / Billing    │
                    └──────────┬───────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Data Preparation        │
                  │ & Temporal Filtering    │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Feature Engineering     │
                  │ Customer-level signals  │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Logistic Regression     │
                  │ Churn Risk Model        │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Churn Probability       │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Revenue at Risk         │
                  │ Probability × MRR       │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Decision Engine         │
                  │ Priority + Action       │
                  └────────────┬────────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ Streamlit        │        │ AI Assistant     │
       │ Dashboard        │        │ Business +       │
       │                  │        │ Customer Analysis│
       └──────────────────┘        └──────────────────┘
```

---

## 📊 Dataset

The project uses the **RavenStack SaaS Subscription & Churn Analytics Dataset**.

The dataset contains:

- Account information
- Subscription information
- Feature usage
- Customer support tickets
- Churn events

### Raw files

```text
data/raw/
├── ravenstack_accounts.csv
├── ravenstack_churn_events.csv
├── ravenstack_feature_usage.csv
├── ravenstack_subscriptions.csv
└── ravenstack_support_tickets.csv
```

The original dataset does not contain actual payment-failure or recovery-outcome information.

Therefore, the project's **revenue-at-risk metric is a model-based estimate**, not a guaranteed prediction of lost revenue.

---

## 🔐 Temporal Leakage Prevention

A major focus of the project is preventing future information from leaking into the churn model.

### Prediction setup

```text
Cutoff Date:
2024-09-30

Prediction Window:
2024-10-01 → 2024-12-29
```

Only information available on or before the cutoff date is used to construct customer features.

Future churn events are used only to construct the target.

### Target

A customer receives:

```text
churn_target = 1
```

if the customer churned during the future prediction window.

Otherwise:

```text
churn_target = 0
```

This produces:

```text
Eligible accounts: 420

Target distribution:
No churn: 296
Churn:    124
```

---

## 🧠 Machine Learning

The project evaluates customer churn risk using a **Logistic Regression** model.

### Features

Customer-level features include:

- Industry
- Country
- Referral source
- Plan tier
- Seats
- Trial status
- Tenure
- Current MRR
- Current ARR
- Usage count
- Support ticket count
- Average satisfaction
- Escalation rate
- Upgrade history
- Downgrade history

Categorical, numerical, and boolean features are processed using appropriate preprocessing pipelines.

Missing values are handled through imputation.

---

## 📈 Model Results

The trained model was evaluated using a held-out test set.

| Metric | Score |
|---|---:|
| Accuracy | 71.43% |
| Precision | 60.00% |
| Recall | 12.00% |
| F1 Score | 20.00% |
| ROC-AUC | 65.76% |

The model's predicted probabilities are used primarily for **customer risk ranking and decision prioritization**.

---

## 💰 Revenue at Risk

Revenue at risk is calculated as:

```text
Revenue at Risk
=
Churn Probability × Current MRR
```

For example:

```text
Churn Probability = 40%
Current MRR       = $10,000

Revenue at Risk
= 0.40 × $10,000
= $4,000
```

### Portfolio result

The current scored portfolio contains:

```text
Eligible customers:        420
Estimated revenue at risk: $248,505.84
Average churn probability: 29.44%
```

> Revenue at risk is a model-based estimate and should not be interpreted as guaranteed lost revenue.

---

## 🎯 Decision Intelligence Engine

The decision engine converts model predictions into business priorities.

### Priority rules

#### High Priority

A customer is High priority when:

```text
Churn Probability >= 50%
OR
Revenue at Risk >= $7,500
```

#### Medium Priority

```text
0.30 <= Churn Probability < 0.50
AND
Revenue at Risk < $7,500
```

#### Low Priority

All remaining customers.

### Current distribution

```text
High     : 40
Medium   : 140
Low      : 240
```

---

## 🛠️ Recommended Retention Actions

The decision engine recommends an action based on observed customer signals.

| Condition | Recommended Action |
|---|---|
| Escalation rate >= 30% | Priority support intervention |
| Average satisfaction <= 3 | Customer satisfaction outreach |
| Customer downgraded | Account retention review |
| Usage count < 200 | Product adoption outreach |
| Otherwise | Proactive retention outreach |

This separates the **prediction layer** from the **business decision layer**.

---

## 🤖 AI Assistant

The platform includes a grounded AI assistant with two modes.

### 👤 Customer Analysis

The assistant can explain:

- Why a customer is considered risky
- Their predicted churn probability
- Revenue at risk
- Risk signals
- Recommended retention action
- Why the customer received its priority

### 🏢 Business Analysis

The assistant can answer portfolio-level questions such as:

```text
How many customers are eligible?

What is the total revenue at risk?

How many customers are high priority?

What are the most common recommended actions?

What is the average predicted churn probability?

Which customers have the highest revenue at risk?
```

The AI assistant is designed as a **business intelligence layer**, not a second prediction model.

It uses the supplied project data and distinguishes between:

- Observed customer information
- Model predictions
- Business-rule decisions

---

## 🖥️ Dashboard

The application is built using Streamlit.

### 🏠 Overview

Provides:

- Portfolio KPIs
- Revenue-at-risk summary
- Priority distribution
- Revenue exposure
- Business insights
- Top customers by revenue at risk

### 👥 Customer Risk Explorer

Provides:

- Customer search
- Priority filtering
- Recommended action filtering
- Customer risk signals
- Customer-level AI analysis

### 🎯 Decision Center

Provides:

- Prioritized customer list
- Recommended retention actions
- Customer investigation
- Decision explanations

### 📈 Analytics

Provides:

- Risk distribution
- Revenue concentration
- Industry-level revenue exposure
- Churn probability distribution
- Recommended action analysis

### 🤖 AI Assistant

Provides:

- Customer Analysis
- Business Analysis
- Natural-language questions about the risk portfolio

---

## 📁 Project Structure

```text
revenue-recovery-decision-intelligence/
│
├── app/
│   ├── app.py
│   ├── data_loader.py
│   │
│   ├── components/
│   │   ├── cards.py
│   │   └── styles.py
│   │
│   └── pages/
│       ├── overview.py
│       ├── customers.py
│       ├── decisions.py
│       ├── analytics.py
│       └── ai_assistant.py
│
├── data/
│   ├── raw/
│   │   ├── ravenstack_accounts.csv
│   │   ├── ravenstack_churn_events.csv
│   │   ├── ravenstack_feature_usage.csv
│   │   ├── ravenstack_subscriptions.csv
│   │   └── ravenstack_support_tickets.csv
│   │
│   └── processed/
│       ├── account_features.csv
│       ├── temporal_account_features.csv
│       ├── customer_risk_scores.csv
│       └── customer_risk_decisions.csv
│
├── models/
│   └── churn_risk_model.joblib
│
├── notebooks/
│   ├── build_features.py
│   ├── check_features.py
│   ├── train_model.py
│   ├── score_customers.py
│   └── decision_engine.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Tech Stack

| Category | Technology |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Model | Logistic Regression |
| Dashboard | Streamlit |
| Visualization | Streamlit Charts / Matplotlib / Plotly |
| Generative AI | OpenAI API |
| Environment Management | python-dotenv |
| Version Control | Git, GitHub |

---

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/Pooja-Priyanka/revenue-recovery-decision-intelligence.git
```

Move into the project:

```bash
cd revenue-recovery-decision-intelligence
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_api_key_here
```

The `.env` file is intentionally excluded from Git using `.gitignore`.

**Never commit your API key to GitHub.**

---

## ▶️ Run the Application

From the project root:

```bash
streamlit run app/app.py
```

The application will open in your browser.

---

## 🔄 Reproducing the Pipeline

### 1. Feature Engineering

```bash
python notebooks/build_features.py
```

### 2. Model Training

```bash
python notebooks/train_model.py
```

### 3. Customer Scoring

```bash
python notebooks/score_customers.py
```

### 4. Decision Engine

```bash
python notebooks/decision_engine.py
```

### 5. Launch Dashboard

```bash
streamlit run app/app.py
```

---

## 📌 Key Results

The current implementation produces:

```text
420
Eligible customers

29.44%
Average predicted churn probability

$248,505.84
Estimated portfolio revenue at risk

40
High-priority customers

140
Medium-priority customers

240
Low-priority customers
```

---

## ⚠️ Limitations

This project is a decision-support prototype.

Important limitations include:

1. The dataset does not contain actual payment-failure data.
2. Revenue at risk is therefore an estimate based on churn probability and current MRR.
3. The model's recall at the default classification threshold is relatively low.
4. The dataset is synthetic and should not be interpreted as production customer data.
5. Recommended actions are business rules rather than experimentally validated interventions.
6. AI-generated explanations are grounded in supplied customer and portfolio data and should be treated as decision support.

---

## 🔮 Future Improvements

Potential production extensions include:

- Real payment-failure signals
- Payment retry and recovery tracking
- Recovery outcome labels
- Customer lifetime value prediction
- Cost-sensitive churn modeling
- Threshold optimization
- Model monitoring
- Automated retention campaigns
- A/B testing of recovery actions
- Real-time CRM integration
- Payment gateway integration
- Explainable ML using SHAP
- Model drift detection

---

## 👩‍💻 Project

**Revenue Recovery & Decision Intelligence Platform**

Built as a SaaS analytics and AI decision-support project combining machine learning, business rules, and generative AI.

---

## 📄 License

This project is intended for educational, portfolio, and buildathon purposes.