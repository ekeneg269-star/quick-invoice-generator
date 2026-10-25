import streamlit as st
import pandas as pd
from fpdf import FPDF
import zipfile
import io

st.set_page_config(page_title="Quick Invoice Generator")
st.title("Quick Invoice Generator")

sample_csv = """client_name,amount,invoice_no,date
John Doe,50000,INV-001,2026-05-16
Jane Smith,75000,INV-002,2026-05-11
Test Client,30000,INV-003,2026-11-01
"""

st.download_button("📥 Download Sample CSV Format", sample_csv, "sample_invoices.csv", "text/csv")
st.info("Your CSV needs columns: client_name, amount, invoice_no, date")

uploaded = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    st.success(f"Loaded {len(df)} clients!")
    st.dataframe(df)
    if st.button("Generate Invoices"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for _, row in df.iterrows():
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, f"INVOICE {row['invoice_no']}", ln=True)
                pdf.set_font("Arial", "", 12)
                pdf.cell(0, 10, f"Client: {row['client_name']}", ln=True)
                pdf.cell(0, 10, f"Amount: {row['amount']}", ln=True)
                pdf.cell(0, 10, f"Date: {row['date']}", ln=True)
                pdf_bytes = pdf.output(dest='S').encode('latin1')
                zip_file.writestr(f"{row['invoice_no']}.pdf", pdf_bytes)
        st.download_button("📦 DOWNLOAD ALL INVOICES (ZIP)", zip_buffer.getvalue(), "invoices.zip", "application/zip")
