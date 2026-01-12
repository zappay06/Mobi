# =========================================================
# ZapPay Mobile – AP Summary Dashboard (Cloud-Deployable)
# Auto-refresh + Color-Coded Invoices
# =========================================================

import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ZapPay Mobile",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp { background-color: #f9fbfd; color: #1f2937; }
h1, h2, h3 { color: #0d47a1; text-align: center; }
.metric-box {
    background: white;
    padding: 16px;
    border-radius: 10px;
    border-left: 6px solid #0d47a1;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 📱 ZapPay – Mobile AP Dashboard")

# ---------------- AUTO REFRESH ----------------
# Refresh every 60 seconds
st_autorefresh = st.experimental_data_editor if hasattr(st, "experimental_data_editor") else st
st_autorefresh(interval=60000, key="refresh")

# ---------------- DATABASE CONNECTION ----------------
DB_PATH = "zap_pay.db"  # Desktop app writes here

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM incoming_queue", conn)
conn.close()

if not df.empty:
    df["Received"] = pd.to_datetime(df["Received"])

# ---------------- SUMMARY CARDS ----------------
today = datetime.now().date()
df_today = df[df["Received"].dt.date == today] if not df.empty else pd.DataFrame(columns=df.columns)

awaiting_review = df_today[df_today["Status"]=="Needs Review"]
flagged = df_today[df_today["Confidence"]<0.85]
approved = df_today[df_today["Status"]=="Auto Approved"]

clients_needing_review = awaiting_review["Client"].nunique() if not awaiting_review.empty else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Clients Needing Review", clients_needing_review)
col2.metric("Bills Awaiting", len(awaiting_review))
col3.metric("Flagged Issues", len(flagged))
col4.metric("Approved", len(approved))

st.markdown("---")

# ---------------- DRILL-DOWN FILTER ----------------
st.subheader("Invoice Drill-Down")

# Filter by client
clients = df_today["Client"].unique().tolist() if not df_today.empty else []
selected_client = st.selectbox("Filter by Client", ["All"] + clients)

# Filter by status
statuses = ["All", "Auto Approved", "Needs Review"]
selected_status = st.selectbox("Filter by Status", statuses)

filtered_df = df_today.copy()
if selected_client != "All":
    filtered_df = filtered_df[filtered_df["Client"]==selected_client]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df["Status"]==selected_status]

# ---------------- COLOR-CODED TABLE ----------------
def color_code(row):
    if row["Confidence"] < 0.85:
        return ["background-color: #ffcccc"]*len(row)  # Red
    elif row["Status"] == "Needs Review":
        return ["background-color: #fff2cc"]*len(row)  # Yellow
    elif row["Status"] == "Auto Approved":
        return ["background-color: #d9f2d9"]*len(row)  # Green
    else:
        return [""]*len(row)

st.dataframe(
    filtered_df[["Received","Client","Supplier","Amount","Category","Confidence","Status"]]
        .style.apply(color_code, axis=1),
    use_container_width=True
)

st.caption("© 2026 ZapPay – Mobile AP Dashboard | Auto-Refresh Every 60s")
