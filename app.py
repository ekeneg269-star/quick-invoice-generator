import streamlit as st
import pandas as pd
from fpdf import FPDF
import zipfile
import io

st.set_page_config(page_title="Zikora X - Invoice Generator", layout="centered")

st.title("Zikora X")
st.subheader("Professional Invoice Generator")
st.markdown("**WhatsApp:** +234 7025091100  |  **Email:** emereolegodswill132@gmail.com")
st.caption("Global - Remote | Serving clients worldwide")
st.divider()

sample_data = """client_name,amount,invoice_no,date
John Doe,50000,INV-001,10/27/2026
Jane Smith,75000,INV-002,10/27/2026"""

st.download_button("📄 Download Sample CSV Format", sample_data, "sample_invoices.csv", "text/csv")
st.info("CSV needs: client_name, amount, invoice_no, date")

def create_invoice_pdf(client, amount, inv_no, date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)
    pdf.set_text_color(0, 82, 204)
    pdf.cell(0, 12, "ZIKORA X", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(100,100,100)
    pdf.cell(0, 6, "Global Digital Services - Remote Team", ln=True, align="C")
    pdf.ln(5)
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
    pdf.ln(12)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "Contact & Payment:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"WhatsApp: +234 7025091100", ln=True)
    pdf.cell(0, 6, f"Email: emereolegodswill132@gmail.com", ln=True)
    pdf.cell(0, 6, f"Location: Global - Remote", ln=True)
    pdf.ln(3)
    pdf.multi_cell(0, 6, "Payment: Please contact us for account details.")
    pdf.ln(8)
    pdf.set_font("Arial", "B", 11)
    pdf.set_text_color(0, 82, 204)
    pdf.cell(0, 8, "Thank you for choosing Zikora X!", ln=True, align="C")
    out = pdf.output(dest='S')
    if isinstance(out, str):
        return out.encode('latin1')
    elif isinstance(out, bytearray):
        return bytes(out)
    else:
        return out

uploaded = st.file_uploader("Upload CSV (After selecting, click DONE at bottom)", type=['csv'])

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        st.success(f"Loaded {len(df)} clients!")
        st.dataframe(df, use_container_width=True)
        if st.button("⚡ Generate Zikora X Invoices", type="primary"):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for idx, row in df.iterrows():
                    pdf_bytes = create_invoice_pdf(str(row.get('client_name','Client')), str(row.get('amount','0')), str(row.get('invoice_no', f'INV-{idx}')), str(row.get('date','')))
                    zip_file.writestr(f"ZikoraX_{row.get('client_name','Client')}_{row.get('invoice_no','')}.pdf", pdf_bytes)
            st.balloons()
            st.success("Zikora X Invoices Ready!")
            st.download_button("📦 Download ALL as ZIP", zip_buffer.getvalue(), "ZikoraX_invoices.zip", "application/zip", type="primary")
            for idx, row in df.iterrows():
                pdf_bytes = create_invoice_pdf(str(row.get('client_name','Client')), str(row.get('amount','0')), str(row.get('invoice_no', f'INV-{idx}')), str(row.get('date','')))
                st.download_button(f"Download {row.get('client_name')} - {row.get('invoice_no')}", pdf_bytes, f"ZikoraX_{row.get('client_name')}.pdf", "application/pdf", key=f"dl_{idx}")
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()
st.caption("Zikora X | WhatsApp: +234 7025091100 | Email: emereolegodswill132@gmail.com | Global - Remote")
