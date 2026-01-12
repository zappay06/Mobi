# =========================================================
# ZapPay Mobile Dashboard
# Reads from main SQLite DB
# =========================================================

import streamlit as st
import sqlite3
import pandas as pd

DB_FILE = "zapay.db"

st.set_page_config(
    page_title="ZapPay Mobile Dashboard",
    page_icon="📱",
    layout="centered"
)

st.markdown("""
<style>
body { background-color: #f4f6f9; color: #1f2937; }
.metric-box { padding: 12px; border-radius: 10px; background: white; margin-bottom: 12px; border-left: 6px solid #0d47a1; }
h1, h2, h3 { color: #0d47a1; }
</style>
""", unsafe_allow_html=True)

# ---------------- DATABASE ----------------
def get_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM invoices", conn)
    conn.close()
    return df

df = get_data()

# ---------------- DASHBOARD ----------------
st.markdown("## 📱 ZapPay – Mobile AP Dashboard")

clients = df["client"].unique().tolist() if not df.empty else []

summary = []

for c in clients:
    client_df = df[df["client"]==c]
    awaiting = len(client_df[client_df["status"]=="Needs Review"])
    flagged = len(client_df[client_df["confidence"]<0.85])
    approved = len(client_df[client_df["status"]=="Auto Approved"])
    summary.append({
        "Client": c,
        "Awaiting Review": awaiting,
        "Flagged": flagged,
        "Approved": approved,
        "Total Bills": len(client_df)
    })

summary_df = pd.DataFrame(summary)

if summary_df.empty:
    st.info("No clients or invoices yet. Add clients and invoices in the main ZapPay app.")
else:
    for idx, row in summary_df.iterrows():
        st.markdown(f"### {row['Client']}")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Awaiting Review", row["Awaiting Review"])
        c2.metric("Flagged", row["Flagged"])
        c3.metric("Approved", row["Approved"])
        c4.metric("Total Bills", row["Total Bills"])
        st.progress(row["Approved"]/max(1,row["Total Bills"]))

# ---------------- CLIENT SELECT ----------------
st.subheader("Client Invoices")
selected_client = st.selectbox("Select Client", clients) if clients else None

if selected_client:
    client_df = df[df["client"]==selected_client]
    st.dataframe(client_df[["Invoice ID","Supplier","Amount","Category","Confidence","Status","Received"]], use_container_width=True)

st.caption("© 2026 ZapPay Mobile Dashboard")







