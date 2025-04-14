# 📊 PhonePe Pulse Data Visualization Dashboard

Welcome to the **PhonePe Pulse Data Visualization Dashboard**! This project utilizes data from the [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse) and presents it in an interactive Streamlit dashboard, showcasing trends in digital payments across India from 2018 to 2023.

---

## 🔍 Overview

The dashboard provides:

- 🗺️ **Geo visualizations** of transaction amounts and counts by state and year.
- 📈 **Trends over time** for different payment types.
- 📍 District and state-level **user registrations and app opens**.
- 📊 Comparative **bar and pie charts** for high-performing regions and categories.
- ⏳ Dynamic filters based on **year, quarter, and state selection**.

---

## 🛠 Tech Stack

- **Python 3.11+**
- **Streamlit** – for dashboard UI
- **Plotly** – for interactive charts
- **MySQL** – for structured backend storage
- **Pandas, JSON, Requests, PIL**

---

## 📁 Folder Structure

📦 phonepe-project/ ├── 📂 data/ # JSON data extracted from PhonePe Pulse GitHub ├── 📜 phonepay.py # Main Streamlit dashboard code ├── 📜 data_ingestion_scripts.py # Script to parse and insert JSON into MySQL ├── 📜 requirements.txt # Python dependencies └── 📄 README.md # You're here!

yaml
Copy
Edit

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally:

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/your-username/phonepe-project.git
cd phonepe-project
✅ 2. Set Up Virtual Environment (Optional)

python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
✅ 3. Install Dependencies

pip install -r requirements.txt
✅ 4. Setup MySQL Database
Ensure MySQL is installed and running.

Create a database:


CREATE DATABASE phonepe_db;
Use the provided data ingestion script or your own logic to insert data into the following tables:

Table Name	Purpose

aggregate_transaction
Aggregated transaction data by state, year, quarter, and transaction type.

aggregate_user
Aggregated user data by state, year, quarter, and phone brand.

map_transaction
Transaction data aggregated at the district level.

map_user
User activity data (app opens and registrations) aggregated at the district level.

top_transaction
Transaction data for the top pincodes in each state, year and quarter.

top_user
User registration data for the top pincodes in each state, year and quarter.

aggregated_insurance
Aggregated insurance transaction data by state, year, quarter, and insurance type.

map_insurance
Insurance transaction data aggregated at the district level.

top_insurance
Insurance transaction data for the top pincodes.

Sample data from PhonePe Pulse is in JSON format and must be parsed correctly into SQL.

💡 How to Run the Dashboard
Once your MySQL database is ready and data is inserted:

streamlit run phonepay.py
You will see a local URL like:

http://localhost:8501
Open this in your browser.

🧩 Features in the Dashboard
✅ Home Tab
Overview of PhonePe

Features of the app

Download link

✅ Explore Data Tab
Animated Geo Maps (choropleths) for:

Total Transaction Amounts

Transaction Counts

Year-wise visualizations:

Payment types vs Count & Amount

Transaction distribution by state

State-wise filtering:

District-level registered users

District-level transaction analysis

✅ Top Charts Tab
Top states by app opens

Transaction types across years

User growth trends

Districts with highest registration

📸 Sample Screenshots
Add screenshots or GIFs of your dashboard UI here!

![Screenshot (178)](https://github.com/user-attachments/assets/7e57da06-32f4-439f-aa01-22ee09d47309)
![Screenshot (179)](https://github.com/user-attachments/assets/b3014e15-a231-4099-b077-bafe7edd48fd)
![Screenshot (180)](https://github.com/user-attachments/assets/ef6e0868-ad12-4d4c-98e2-9f31c7d76093)
![Screenshot (181)](https://github.com/user-attachments/assets/2b73dcbf-1bae-4845-b436-18b543c62ac6)
![Screenshot (182)](https://github.com/user-attachments/assets/8882741f-3900-4277-8190-ca43ee44f874)
![Screenshot (183)](https://github.com/user-attachments/assets/bb087798-f76d-45bb-af26-70022946071e)


🔐 Credentials and Notes
Update your MySQL DB config inside phonepay.py:

host = "localhost"
user = "root"
password = "your_mysql_password"
database = "phonepe_db"

📌 Requirements

streamlit
mysql-connector-python
pandas
plotly
Pillow
requests
Install using:

pip install -r requirements.txt

🤝 Contributing
Feel free to fork this repo, enhance the visuals, fix bugs, or add new features! PRs are welcome.

📬 Contact
Created by [Kavya]



