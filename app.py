import streamlit as st
import pandas as pd
from fpdf import FPDF
import zipfile
import os
from io import BytesIO

st.set_page_config(page_title="Quick Invoice Generator", page_icon="🧾")

st.title("🧾 Quick Invoice Generator")
st.write("Upload your CSV and generate invoice PDFs in seconds!")

# Sample format guide
with st.expander("📋 See CSV Format Example"):
    st.write("Your CSV should have columns like:")
    st.code("client_name, amount, invoice_no, date\nJohn Doe, 50000, INV-001, 2026-05-10\nJane Smith, 75000, INV-002, 2026-05-11")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"Loaded {len(df)} invoices!")
    st.dataframe(df.head())

    if st.button("🚀 Generate All Invoices as PDF"):
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for index, row in df.iterrows():
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 20)
                pdf.cell(0, 20, "INVOICE", ln=True, align="C")
                pdf.ln(10)
                pdf.set_font("Arial", "", 12)
                
                # Get data safely
                client = str(row.iloc[0] if len(row) > 0 else "Client")
                amount = str(row.iloc[1] if len(row) > 1 else "0")
                inv_no = str(row.iloc[2] if len(row) > 2 else f"INV-{index}")
                
                pdf.cell(0, 10, f"Invoice No: {inv_no}", ln=True)
                pdf.cell(0, 10, f"Client: {client}", ln=True)
                pdf.cell(0, 10, f"Amount: {amount}", ln=True)
                pdf.cell(0, 10, f"Description: Service Payment", ln=True)
                pdf.ln(20)
                pdf.cell(0, 10, "Thank you for your business!", ln=True, align="C")
                
                pdf_bytes = pdf.output(dest='S').encode('latin-1')
                zip_file.writestr(f"{inv_no}_{client}.pdf", pdf_bytes)
        
        st.success("✅ Invoices Generated!")
        st.download_button(
            label="📥 Download All Invoices (ZIP)",
            data=zip_buffer.getvalue(),
            file_name="quick_invoices.zip",
            mime="application/zip"
        )

st.markdown("---")
st.caption("Built with Quick Invoice Generator | github.com/ekeneg269-star/quick-invoice-generator")
