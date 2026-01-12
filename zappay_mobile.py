import streamlit as st
import sqlite3
import pandas as pd

# Page config
st.set_page_config(page_title="📱 ZapPay Mobile", layout="wide")
st.header("📱 ZapPay – Mobile AP Dashboard")

# Connect to main database
conn = sqlite3.connect("zappay.db", check_same_thread=False)

# Fetch real invoices
invoices_df = pd.read_sql("""
    SELECT invoices.*, clients.name as client_name
    FROM invoices
    LEFT JOIN clients ON invoices.client_id = clients.id
""", conn)

# Compute metrics safely
awaiting = len(invoices_df[invoices_df["status"]=="Needs Review"]) if not invoices_df.empty else 0
flagged = len(invoices_df[invoices_df["status"]=="Flagged"]) if not invoices_df.empty else 0
approved = len(invoices_df[invoices_df["status"]=="Auto Approved"]) if not invoices_df.empty else 0
total = len(invoices_df) if not invoices_df.empty else 0

# Display summary
col1, col2, col3, col4 = st.columns(4)
col1.metric("Awaiting Review", awaiting)
col2.metric("Flagged", flagged)
col3.metric("Approved", approved)
col4.metric("Total Bills", total)

# Show grouped client data if invoices exist
if not invoices_df.empty:
    grouped = invoices_df.groupby("client_name").agg(
        awaiting_review=("status", lambda x: sum(x=="Needs Review")),
        flagged=("status", lambda x: sum(x=="Flagged")),
        approved=("status", lambda x: sum(x=="Auto Approved")),
        total=("id", "count")
    ).reset_index()
    st.subheader("Invoices by Client")
    st.dataframe(grouped, use_container_width=True)
else:
    st.info("No invoices yet. Add clients and upload invoices in the main system.")





