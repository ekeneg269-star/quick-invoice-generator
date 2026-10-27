import streamlit as st
import pandas as pd
from fpdf import FPDF
import zipfile
import io

st.set_page_config(page_title="Zikora X", layout="centered")

st.title("Zikora X")
st.subheader("Professional Invoice Generator")
st.caption("Generate branded invoices in seconds")
st.divider()

sample_data = """client_name,amount,invoice_no,date
John Doe,50000,INV-001,10/27/2026
Jane Smith,75000,INV-002,10/27/2026"""

st.download_button("📄 Download Sample CSV", sample_data, "sample_invoices.csv", "text/csv")

def create_invoice_pdf(client, amount, inv_no, date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(0, 82, 204)
    pdf.cell(0, 12, "ZIKORA X", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(100,100,100)
    pdf.cell(0, 6, "Global Digital Services", ln=True, align="C")
    pdf.ln(8)
    pdf.set_draw_color(0,82,204)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "INVOICE", ln=True, align="C")
    pdf.ln(8)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Invoice No: {inv_no}", ln=True)
    pdf.cell(0, 8, f"Date: {date}", ln=True)
    pdf.cell(0, 8, f"Billed To: {client}", ln=True)
    pdf.ln(5)
    pdf.set_fill_color(240, 244, 255)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 12, f"  Amount Due: NGN {amount}", ln=True, fill=True)
    pdf.ln(15)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, "WhatsApp: +234 7025091100", ln=True)
    pdf.cell(0, 6, "Email: emereolegodswill132@gmail.com", ln=True)
    pdf.cell(0, 6, "Location: Global - Remote", ln=True)
    pdf.ln(8)
    pdf.set_font("Arial", "B", 11)
    pdf.set_text_color(0, 82, 204)
    pdf.cell(0, 8, "Thank you for choosing Zikora X!", ln=True, align="C")
    out = pdf.output(dest='S')
    return out.encode('latin1') if isinstance(out, str) else bytes(out) if isinstance(out, bytearray) else out

# UPLOAD - DO NOT USE RECENTS, USE DOWNLOADS
uploaded = st.file_uploader("Upload CSV from Downloads folder", type=['csv'])

if uploaded is not None:
    df = pd.read_csv(uploaded)
    st.success(f"Loaded {len(df)} clients!")
    st.dataframe(df)
    if st.button("Generate Invoices", type="primary"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as z:
            for _, row in df.iterrows():
                pdf_bytes = create_invoice_pdf(str(row['client_name']), str(row['amount']), str(row['invoice_no']), str(row['date']))
                z.writestr(f"{row['client_name']}.pdf", pdf_bytes)
        st.balloons()
        st.download_button("Download ZIP", zip_buffer.getvalue(), "ZikoraX_invoices.zip", "application/zip")

st.divider()
st.caption("Zikora X | Global - Remote")
