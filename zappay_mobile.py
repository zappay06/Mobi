import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
from datetime import datetime
import random

# -------------------------
# Auto-refresh every 60 sec
# -------------------------
st_autorefresh(interval=60000, key="refresh")

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="📱 ZapPay Mobile AP",
    page_icon="💸",
    layout="wide"
)

# -------------------------
# Mock Data (replace with real integration)
# -------------------------
# Simulate invoice data
def generate_mock_invoices():
    clients = ["Client A", "Client B", "Client C"]
    statuses = ["awaiting_review", "flagged", "approved"]
    data = []
    for i in range(25):
        client = random.choice(clients)
        status = random.choices(
            statuses, weights=[0.4, 0.2, 0.4], k=1
        )[0]
        amount = round(random.uniform(100, 2000), 2)
        data.append({
            "Invoice ID": f"{i+1:03d}",
            "Client": client,
            "Supplier": f"Supplier {random.randint(1,5)}",
            "Amount": amount,
            "Status": status,
            "Received": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
    return pd.DataFrame(data)

df = generate_mock_invoices()

# -------------------------
# Client Grouping
# -------------------------
st.title("📱 ZapPay – Mobile AP Dashboard")
clients = df["Client"].unique()

for client in clients:
    client_df = df[df["Client"] == client]
    st.subheader(f"Client: {client}")

    # Status counts
    awaiting = len(client_df[client_df["Status"]=="awaiting_review"])
    flagged = len(client_df[client_df["Status"]=="flagged"])
    approved = len(client_df[client_df["Status"]=="approved"])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Awaiting Review", awaiting)
    col2.metric("Flagged", flagged)
    col3.metric("Approved", approved)
    col4.metric("Total Bills", len(client_df))
    
    # Color-coded table
    def color_status(row):
        if row.Status == "awaiting_review":
            return ["#FFF3CD"]*len(row)
        elif row.Status == "flagged":
            return ["#F8D7DA"]*len(row)
        elif row.Status == "approved":
            return ["#D4EDDA"]*len(row)
        else:
            return ["white"]*len(row)
    
    st.dataframe(client_df.style.apply(color_status, axis=1), use_container_width=True)

# -------------------------
# Quick Actions
# -------------------------
st.sidebar.title("⚡ Quick Actions")
if st.sidebar.button("Auto-approve all high-confidence"):
    st.sidebar.success("Auto-approve action simulated!")
if st.sidebar.button("View flagged only"):
    flagged_df = df[df["Status"]=="flagged"]
    st.sidebar.dataframe(flagged_df, use_container_width=True)

# -------------------------
# Summary
# -------------------------
st.markdown("---")
st.subheader("📊 Today's Summary (All Clients)")

today_df = df  # In real app, filter by today
total_bills = len(today_df)
total_flagged = len(today_df[today_df["Status"]=="flagged"])
total_review = len(today_df[today_df["Status"]=="awaiting_review"])
total_approved = len(today_df[today_df["Status"]=="approved"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Bills", total_bills)
col2.metric("Awaiting Review", total_review)
col3.metric("Flagged Issues", total_flagged)
col4.metric("Approved", total_approved)


