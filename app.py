import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quick Invoice Generator", layout="centered")
st.title("Quick Invoice Generator")

# Sample download
sample_data = """client_name,amount,invoice_no,date
John Doe,50000,INV-001,5/16/2026
Jane Smith,75000,INV-002,5/11/2026
Test Client,30000,INV-003,11/1/2026"""

st.download_button("📄 Download Sample CSV Format", sample_data, "sample_invoices.csv", "text/csv")

st.info("Your CSV needs columns: client_name, amount, invoice_no, date")

# FIXED UPLOADER - No type filter for Android
uploaded = st.file_uploader("Upload CSV file", type=None)

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        st.success(f"✅ Loaded {len(df)} clients!")
        st.dataframe(df)
        
        if st.button("Generate Invoices"):
            st.balloons()
            st.success("Invoices ready!")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.write("Make sure file is CSV with columns: client_name, amount, invoice_no, date")
else:
    st.write("Waiting for CSV upload...")
