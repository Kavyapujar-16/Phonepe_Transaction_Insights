# 📊 PhonePe Transaction Insights Dashboard

This project presents a fully interactive data dashboard that visualizes PhonePe Pulse transaction data across India using **Streamlit**, **Plotly**, and **MySQL**. It also includes a professional Power BI report for high-level business insights.

---

## 🧠 Project Overview

PhonePe is one of India's most popular digital payment platforms. This dashboard helps visualize key patterns and behaviors across different states, districts, quarters, and years.

- 📈 Track transaction volume and value trends
- 👤 Analyze user registrations and engagement across devices
- 🛡 Evaluate insurance penetration across regions
- 📍 Explore district-wise and pincode-level insights

---

## 📦 Features

- ✅ Real-time visualizations using Plotly and GeoJSON maps
- ✅ Year and Quarter filters for dynamic exploration
- ✅ Business Case Studies across 6 dimensions:
  - Decoding Transaction Dynamics
  - Device Dominance & User Engagement
  - Insurance Growth Analysis
  - Market Expansion via Transactions
  - User Engagement Trends
  - Insurance Engagement by District
- ✅ Power BI Dashboard Report (`/PowerBI` folder)
- ✅ Clean and branded UI with Streamlit

---

## 🛠 Technologies Used

| Tool            | Purpose                        |
|-----------------|--------------------------------|
| Python          | Backend Data Processing        |
| MySQL           | Database for structured data   |
| Streamlit       | Interactive Web App            |
| Plotly          | Visualizations and Charts      |
| Power BI        | Professional Report Insights   |
| GitHub          | Version Control & Deployment   |

---

## 📁 Project Structure

```
├── phonepay.py                     # Streamlit App Source Code
├── datafetch_notebook.ipynb       # Jupyter Notebook for Data Extraction
├── /PowerBI                       # Reports and Power BI visuals
│   ├── PhonePe_Insights_Report.docx
│   └── Dashboard_Visuals.pbix
├── /data                          # Raw JSON Files from PhonePe Pulse
└── README.md                      # This file
```

---

## 🚀 How to Run Locally

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/Phonepe_Transaction_Insights.git
cd Phonepe_Transaction_Insights
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit App:
```bash
streamlit run phonepe.py
```

---


