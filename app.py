import streamlit as st
import pandas as pd
from fpdf import FPDF
import zipfile, io

st.set_page_config(page_title="Zikora X")
st.title("Zikora X")
st.write("Professional Invoice Generator")
st.divider()

sample = "client_name,amount,invoice_no,date\nJohn Doe,50000,INV-001,2026-10-27"
st.download_button("Download Sample CSV", sample, "sample.csv", "text/csv")

file = st.file_uploader("Upload Clients CSV", type=["csv"])

def make_pdf(client, amount, inv_no, date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"ZIKORA X - INVOICE",ln=True,align="C")
    pdf.ln(5)
    pdf.set_font("Arial","",11)
    pdf.cell(0,8,f"Invoice No: {inv_no}",ln=True)
    pdf.cell(0,8,f"Date: {date}",ln=True)
    pdf.cell(0,8,f"Client: {client}",ln=True)
    pdf.cell(0,8,f"Amount: NGN {amount}",ln=True)
    pdf.ln(10)
    pdf.set_font("Arial","",9)
    pdf.cell(0,6,"Zikora X | WhatsApp: +234 7025091100 | Email: emereolegodswill132@gmail.com | Global - Remote",ln=True)
    out = pdf.output(dest='S')
    return out.encode('latin1') if isinstance(out,str) else bytes(out)

if file is not None:
    df = pd.read_csv(file)
    st.success(f"{len(df)} clients")
    st.dataframe(df)
    if st.button("Generate Invoices"):
        z = io.BytesIO()
        with zipfile.ZipFile(z,"w") as zipf:
            for _, r in df.iterrows():
                d = make_pdf(r['client_name'], r['amount'], r['invoice_no'], r['date'])
                zipf.writestr(f"{r['client_name']}.pdf", d)
        st.download_button("Download ALL Invoices as ZIP", z.getvalue(), "invoices.zip", "application/zip")

st.divider()
st.write("Zikora X | WhatsApp: +234 7025091100 | Email: emereolegodswill132@gmail.com | Global - Remote")
