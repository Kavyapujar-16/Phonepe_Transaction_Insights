# phonepe_dashboard_app.py
import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import requests
import json

# --- DB Connection ---
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kavya2010@",
        database="phonepe_db"
    )

def execute_query(query, params=None):
    try:
        with get_db_connection() as mydb:
            cursor = mydb.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
        return pd.DataFrame(result)
    except mysql.connector.Error as err:
        st.error(f"Error executing query: {err}")
        return pd.DataFrame()

# --- Global Config ---
st.set_page_config(page_title="PhonePe Dashboard", layout="wide")
GEO_URL = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
geo = json.loads(requests.get(GEO_URL).content)
quarter_map = {
    "Q1 (Jan-Mar)": 1,
    "Q2 (Apr-Jun)": 2,
    "Q3 (Jul-Sep)": 3,
    "Q4 (Oct-Dec)": 4
}

# Query wrapper
def run_query(query, params=None):
    conn = get_db_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

# --- Navigation ---
st.sidebar.title("📊 Navigation")
section = st.sidebar.radio("Go to", ["Home", "Business Case Study", "Case Study Insights"])

# --- Home ---
if section == "Home":
    st.markdown("""
        <style>
        .home-title {
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            color: #6C63FF;
        }
        .home-subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #333;
            margin-bottom: 2rem;
        }
        .info-box {
            background-color: #F0F4FF;
            border-left: 6px solid #6C63FF;
            padding: 1rem 1.5rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            font-size: 1rem;
            color: #222;
        }
        .highlight {
            color: #6C63FF;
            font-weight: bold;
        }
        </style>

        <div class="home-title">📱 PhonePe Transaction Insights</div>
        <div class="home-subtitle">Explore India's Digital Economy with Real-time PhonePe Data</div>
        <hr style='border: 1px solid #6C63FF;'>
    """, unsafe_allow_html=True)

    st.markdown("### 🔍 What Can You Discover?")

    st.markdown("""
        <div class="info-box">💳 <span class='highlight'>Aggregated Transactions:</span> View transaction volumes by type, region, and trends over time.</div>
        <div class="info-box">👥 <span class='highlight'>User Engagement:</span> Explore how users interact with the app across brands, states, and districts.</div>
        <div class="info-box">🛡 <span class='highlight'>Insurance Analytics:</span> Analyze state-wise and district-level adoption of insurance services.</div>
        <div class="info-box">🌐 <span class='highlight'>Interactive Visuals:</span> Choropleths, bar charts, line graphs, and pie charts to bring data to life.</div>
        <div class="info-box">📊 <span class='highlight'>Custom Filters:</span> Filter insights by year and quarter across the country.</div>
    """, unsafe_allow_html=True)

    st.success("Use the sidebar to explore the full Business Case Study ➡")



# --- Business Case Study ---
elif section == "Business Case Study":
    st.title("🏢 Business Case Study")
    sub_tab = st.radio("Choose Analysis", ["Transaction", "User", "Insurance"])

    # Year & Quarter Dropdown (once only)
    years = ["All"] + [str(y) for y in range(2018, 2025)]
    quarters = ["All"] + list(quarter_map.keys())

    col1, col2 = st.columns(2)
    selected_year = col1.selectbox("Select Year", years)
    selected_quarter = col2.selectbox("Select Quarter", quarters)

    year = int(selected_year) if selected_year != "All" else None
    quarter = quarter_map[selected_quarter] if selected_quarter != "All" else None

    conditions = []
    params = []

    if year is not None:
        conditions.append("Years = %s")
        params.append(year)
    if quarter is not None:
        conditions.append("Quarter = %s")
        params.append(quarter)

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    if sub_tab == "Transaction":
        st.subheader("💳 Transaction Overview")

        df = execute_query(f"""
            SELECT SUM(Transaction_count) AS TotalTransactions,
                   AVG(Transaction_count) AS AvgTransactions,
                   SUM(Transaction_amount) AS TotalRevenue,
                   AVG(Transaction_amount) AS AvgRevenue
            FROM aggregate_transaction
            {where_clause}
        """, tuple(params))

        col1, col2 = st.columns(2)
        col1.metric("Total Transactions", f"{df['TotalTransactions'][0]:,.0f}")
        col1.metric("Average Transactions", f"{df['AvgTransactions'][0]:,.2f}")
        col2.metric("Total Revenue (₹)", f"{df['TotalRevenue'][0]:,.2f}")
        col2.metric("Avg Revenue (₹)", f"{df['AvgRevenue'][0]:,.2f}")

        df_map = execute_query(f"""
            SELECT States, SUM(Transaction_count) AS TotalTransactions
            FROM map_transaction
            {where_clause}
            GROUP BY States
        """, tuple(params))

        fig = px.choropleth(df_map, geojson=geo, locations="States",
                            featureidkey="properties.ST_NM", color="TotalTransactions",
                            color_continuous_scale="Reds", title="State-wise Total Transactions")
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📌 Top 10 States by Transaction Volume")
        df_top = df_map.sort_values(by="TotalTransactions", ascending=False).head(10)
        st.dataframe(df_top, use_container_width=True)

    elif sub_tab == "User":
        st.subheader("📱 User Engagement and Growth Strategy")

        df_total = execute_query(f"""
            SELECT SUM(RegisteredUser) as TotalUsers, SUM(AppOpens) as TotalOpens 
            FROM map_user {where_clause}
        """, tuple(params))

        if not df_total.empty:
            st.metric("Total Registered Users", f"{int(df_total.iloc[0]['TotalUsers']):,}")
            st.metric("Total App Opens", f"{int(df_total.iloc[0]['TotalOpens']):,}")

        tab1, tab2, tab3 = st.tabs(["States", "Districts", "Pincodes"])

        with tab1:
            df_states = execute_query(f"""
                SELECT States, SUM(RegisteredUser) as TotalUsers 
                FROM map_user {where_clause} 
                GROUP BY States ORDER BY TotalUsers DESC LIMIT 10
            """, tuple(params))
            if not df_states.empty:
                st.markdown("#### 🏆 Top 10 States by Registered Users")
                st.dataframe(df_states, use_container_width=True)

        with tab2:
            df_districts = execute_query(f"""
                SELECT Districts, SUM(RegisteredUser) as TotalUsers 
                FROM map_user {where_clause} 
                GROUP BY Districts ORDER BY TotalUsers DESC LIMIT 10
            """, tuple(params))
            if not df_districts.empty:
                st.markdown("#### 🏆 Top 10 Districts by Registered Users")
                st.dataframe(df_districts, use_container_width=True)

        with tab3:
            df_pincodes = execute_query(f"""
                SELECT Pincodes, SUM(RegisteredUser) as TotalUsers 
                FROM top_user {where_clause} 
                GROUP BY Pincodes ORDER BY TotalUsers DESC LIMIT 10
            """, tuple(params))
            if not df_pincodes.empty:
                st.markdown("#### 🏆 Top 10 Pincodes by Registered Users")
                st.dataframe(df_pincodes, use_container_width=True)

    elif sub_tab == "Insurance":
        st.subheader("🛡 Insurance Engagement Insights")

        df_total = execute_query(f"""
            SELECT SUM(Transaction_count) as TotalTransactions, SUM(Transaction_amount) as TotalAmount
            FROM map_insurance {where_clause}
        """, tuple(params))

        if not df_total.empty:
            st.metric("Total Insurance Transactions", f"{int(df_total.iloc[0]['TotalTransactions']):,}")
            st.metric("Total Insurance Amount (₹)", f"{int(df_total.iloc[0]['TotalAmount']):,}")

        tab1, tab2, tab3 = st.tabs(["States", "Districts", "Pincodes"])

        with tab1:
            df_states = execute_query(f"""
                SELECT States, SUM(Transaction_count) as TotalTransactions
                FROM map_insurance {where_clause}
                GROUP BY States ORDER BY TotalTransactions DESC LIMIT 10
            """, tuple(params))
            if not df_states.empty:
                st.markdown("#### 🏆 Top 10 States by Insurance Transactions")
                st.dataframe(df_states, use_container_width=True)

        with tab2:
            df_districts = execute_query(f"""
                SELECT Districts, SUM(Transaction_count) as TotalTransactions
                FROM map_insurance {where_clause}
                GROUP BY Districts ORDER BY TotalTransactions DESC LIMIT 10
            """, tuple(params))
            if not df_districts.empty:
                st.markdown("#### 🏆 Top 10 Districts by Insurance Transactions")
                st.dataframe(df_districts, use_container_width=True)

        with tab3:
            df_pincodes = execute_query(f"""
                SELECT Pincodes, SUM(Transaction_count) as TotalTransactions
                FROM top_insurance {where_clause}
                GROUP BY Pincodes ORDER BY TotalTransactions DESC LIMIT 10
            """, tuple(params))
            if not df_pincodes.empty:
                st.markdown("#### 🏆 Top 10 Pincodes by Insurance Transactions")
                st.dataframe(df_pincodes, use_container_width=True)

st.markdown("<hr><p style='text-align:center; font-size: 14px;'>Created by Kavya • Streamlit + MySQL + Plotly</p>", unsafe_allow_html=True)


# Case Study Insights
if section == "Case Study Insights":
    st.title("📈 Case Study Insights Dashboard")

    # Year and Quarter Filters
    years = ["All"] + [str(y) for y in range(2018, 2025)]
    quarters = ["All"] + list(quarter_map.keys())

    col1, col2 = st.columns(2)
    selected_year = col1.selectbox("Select Year", years)
    selected_quarter = col2.selectbox("Select Quarter", quarters)

    year = int(selected_year) if selected_year != "All" else None
    quarter = quarter_map[selected_quarter] if selected_quarter != "All" else None

    conditions = []
    params = []

    if year is not None:
        conditions.append("Years = %s")
        params.append(year)
    if quarter is not None:
        conditions.append("Quarter = %s")
        params.append(quarter)

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    case_option = st.selectbox("Select Case Study", [
        "Decoding Transaction Dynamics",
        "Device Dominance and User Engagement",
        "Insurance Penetration and Growth Potential",
        "Transaction Analysis for Market Expansion",
        "User Engagement and Growth Strategy",
        "Insurance Engagement Analysis"
    ])

    if case_option == "Decoding Transaction Dynamics":
        df_type = execute_query(f"SELECT Transaction_type, SUM(Transaction_count) AS TotalCount FROM aggregate_transaction {where_clause} GROUP BY Transaction_type", tuple(params))
        st.plotly_chart(px.bar(df_type, x="Transaction_type", y="TotalCount", title="Transactions by Type", color="Transaction_type", color_discrete_sequence=px.colors.sequential.RdBu))

        df_map = execute_query(f"SELECT States, SUM(Transaction_count) AS TotalTransactions FROM map_transaction {where_clause} GROUP BY States", tuple(params))
        fig_map = px.choropleth(df_map, geojson=geo, locations="States", featureidkey="properties.ST_NM", color="TotalTransactions", title="State-wise Transaction Volume", color_continuous_scale="Sunset")
        fig_map.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_map)

        df_trend = execute_query(f"SELECT Years, SUM(Transaction_amount) AS Amount FROM aggregate_transaction {where_clause} GROUP BY Years", tuple(params))
        st.plotly_chart(px.line(df_trend, x="Years", y="Amount", markers=True, title="Transaction Trend Over Years", color_discrete_sequence=["orange"]))

        df_top = execute_query(f"SELECT States, SUM(Transaction_count) AS TotalCount FROM map_transaction {where_clause} GROUP BY States ORDER BY TotalCount DESC LIMIT 10", tuple(params))
        st.plotly_chart(px.bar(df_top, x="States", y="TotalCount", title="Top 10 States by Transactions", color="States", color_discrete_sequence=px.colors.sequential.Agsunset))

    elif case_option == "Device Dominance and User Engagement":
        df_users = execute_query(f"SELECT Brands, SUM(Transaction_count) AS Users FROM aggregate_user {where_clause} GROUP BY Brands", tuple(params))
        st.plotly_chart(px.bar(df_users, x="Brands", y="Users", title="Users by Device Brand", color="Brands", color_discrete_sequence=px.colors.qualitative.Set1))

        df_opens = execute_query(f"""
            SELECT au.Brands, SUM(mu.AppOpens) AS AppOpens
            FROM aggregate_user au
            JOIN map_user mu ON au.States = mu.States AND au.Years = mu.Years AND au.Quarter = mu.Quarter
            {where_clause.replace('Years', 'au.Years').replace('Quarter', 'au.Quarter')}
            GROUP BY au.Brands
        """, tuple(params))
        st.plotly_chart(px.bar(df_opens, x="Brands", y="AppOpens", title="App Opens by Device Brand", color="Brands", color_discrete_sequence=px.colors.qualitative.Dark2))

    elif case_option == "Insurance Penetration and Growth Potential":
        df_state = execute_query(f"SELECT States, SUM(Total_count) AS TotalCount FROM aggregated_insurance {where_clause} GROUP BY States", tuple(params))
        st.plotly_chart(px.bar(df_state.sort_values(by="TotalCount", ascending=False), x="States", y="TotalCount", title="Top States by Insurance Transactions", color_discrete_sequence=px.colors.sequential.Tealgrn))

        st.plotly_chart(px.pie(df_state.sort_values(by="TotalCount", ascending=True).head(10), names="States", values="TotalCount", title="Least Penetrated States (Pie View)"))

        df_line = execute_query(f"SELECT Years, SUM(Total_count) AS Count FROM aggregated_insurance {where_clause} GROUP BY Years", tuple(params))
        st.plotly_chart(px.line(df_line, x="Years", y="Count", markers=True, title="Insurance Growth Over Time", color_discrete_sequence=["#EF476F"]))

    elif case_option == "Transaction Analysis for Market Expansion":
        df_amount = execute_query(f"SELECT States, SUM(Transaction_amount) AS Amount FROM aggregate_transaction {where_clause} GROUP BY States", tuple(params))
        st.plotly_chart(px.bar(df_amount.sort_values(by="Amount", ascending=False), x="States", y="Amount", title="States by Transaction Value", color_discrete_sequence=px.colors.sequential.Plasma))

        df_yearwise = execute_query(f"SELECT Years, SUM(Transaction_amount) AS Total FROM aggregate_transaction {where_clause} GROUP BY Years", tuple(params))
        st.plotly_chart(px.area(df_yearwise, x="Years", y="Total", title="Transaction Value Over Years", color_discrete_sequence=["#06D6A0"]))

        df_map_amt = execute_query(f"SELECT States, SUM(Transaction_amount) AS TotalAmount FROM map_transaction {where_clause} GROUP BY States", tuple(params))
        fig = px.choropleth(df_map_amt, geojson=geo, locations="States", featureidkey="properties.ST_NM", color="TotalAmount", color_continuous_scale="Purples", title="State-wise Market Value Map")
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)

    elif case_option == "User Engagement and Growth Strategy":
        df_app = execute_query(f"SELECT States, SUM(AppOpens) AS Opens FROM map_user {where_clause} GROUP BY States", tuple(params))
        st.plotly_chart(px.bar(df_app.sort_values(by="Opens", ascending=False).head(10), x="States", y="Opens", title="Top States by App Opens", color="States", color_discrete_sequence=px.colors.sequential.Mint))

        df_reg = execute_query(f"SELECT Years, SUM(RegisteredUser) AS Users FROM map_user {where_clause} GROUP BY Years", tuple(params))
        st.plotly_chart(px.line(df_reg, x="Years", y="Users", markers=True, title="User Registrations Over Time", color_discrete_sequence=["#FF6B6B"]))

        df_districts = execute_query(f"SELECT Districts, SUM(RegisteredUser) AS Users FROM map_user {where_clause} GROUP BY Districts ORDER BY Users DESC LIMIT 10", tuple(params))
        st.plotly_chart(px.pie(df_districts, names="Districts", values="Users", title="Top Districts by Registrations Share"))

    elif case_option == "Insurance Engagement Analysis":
        df_districts = execute_query(f"SELECT Districts, SUM(Transaction_count) AS Count, SUM(Transaction_amount) AS Amount FROM map_insurance {where_clause} GROUP BY Districts ORDER BY Count DESC LIMIT 10", tuple(params))
        st.plotly_chart(px.bar(df_districts, x="Districts", y="Count", title="Insurance Transactions by District", color="Districts", color_discrete_sequence=px.colors.sequential.Greens))
        st.plotly_chart(px.pie(df_districts, names="Districts", values="Amount", title="Insurance Value Distribution by District"))

    st.markdown("<hr><p style='text-align:center; font-size: 14px;'>Created by Kavya • Streamlit + MySQL + Plotly</p>", unsafe_allow_html=True)