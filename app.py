import streamlit as st
import pandas as pd
from fpdf import FPDF
import zipfile
import io

st.set_page_config(page_title="Quick Invoice Generator", layout="centered")
st.title("Quick Invoice Generator")

sample_data = """client_name,amount,invoice_no,date
John Doe,50000,INV-001,5/16/2026
Jane Smith,75000,INV-002,5/11/2026
Test Client,30000,INV-003,11/1/2026"""

st.download_button("📄 Download Sample CSV Format", sample_data, "sample_invoices.csv", "text/csv")
st.info("Your CSV needs: client_name, amount, invoice_no, date")

def create_invoice_pdf(client, amount, inv_no, date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "INVOICE", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Invoice No: {inv_no}", ln=True)
    pdf.cell(0, 10, f"Date: {date}", ln=True)
    pdf.cell(0, 10, f"Client: {client}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Amount Due: NGN {amount}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, "Thank you for your business!", ln=True, align="C")
    return pdf.output(dest='S').encode('latin1')

uploaded = st.file_uploader("Upload CSV file")

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        st.success(f"✅ Loaded {len(df)} clients!")
        st.dataframe(df)

        if st.button("🔥 Generate & Download Invoices"):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for idx, row in df.iterrows():
                    pdf_bytes = create_invoice_pdf(
                        str(row.get('client_name', 'Client')),
                        str(row.get('amount', 0)),
                        str(row.get('invoice_no', f'INV-{idx}')),
                        str(row.get('date', ''))
                    )
                    zip_file.writestr(f"{row.get('client_name','Client')}_{row.get('invoice_no','')}.pdf", pdf_bytes)
            
            st.balloons()
            st.success("🎉 Invoices Ready! Download below
