import streamlit as st
import pandas as pd
from fpdf import FPDF
import zipfile, io

st.set_page_config(page_title="Zikora X", page_icon="📄", layout="centered")

st.title("Zikora X")
st.write("### Professional Invoice Generator - Live Demo")
st.write("See how it works in 10 seconds. No signup needed.")
st.divider()

# AUTO DEMO DATA - Client sees this immediately
demo_csv = """client_name,amount,invoice_no,date
John Doe,50000,INV-001,2026-10-27
Jane Smith,75000,INV-002,2026-10-27
Acme Corp,120000,INV-003,2026-10-27"""

df = pd.read_csv(io.StringIO(demo_csv))

# Optional: If client wants to test with their own file
with st.expander("Want to test with your own clients? Upload CSV here"):
    file = st.file_uploader("Upload Clients CSV", type=["csv"], label_visibility="collapsed")
    if file is not None:
        df = pd.read_csv(file)
    pasted = st.text_area("Or paste CSV", placeholder="client_name,amount,invoice_no,date", height=80)
    if pasted.strip() != "":
        try:
            df = pd.read_csv(io.StringIO(pasted))
        except:
            st.error("Format: client_name,amount,invoice_no,date")

st.success(f"✅ {len(df)} clients loaded - Ready to generate")
st.dataframe(df, use_container_width=True)

def make_pdf(client, amount, inv_no, date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"ZIKORA X - INVOICE",ln=True,align="C")
    pdf.line(10,25,200,25)
    pdf.ln(15)
    pdf.set_font("Arial","",12)
    pdf.cell(0,9,f"Invoice No: {inv_no}",ln=True)
    pdf.cell(0,9,f"Date: {date}",ln=True)
    pdf.cell(0,9,f"Bill To: {client}",ln=True)
    pdf.ln(3)
    pdf.set_font("Arial","B",13)
    pdf.cell(0,10,f"Amount Due: NGN {amount}",ln=True)
    pdf.ln(15)
    pdf.set_font("Arial","",8)
    pdf.set_text_color(100,100,100)
    pdf.cell(0,5,"Zikora X | WhatsApp: +234 7025091100 | Email: emereolegodswill132@gmail.com | Global - Remote",ln=True,align="C")
    out = pdf.output(dest='S')
    return out.encode('latin1') if isinstance(out,str) else bytes(out)

st.write("")
if st.button("🚀 Generate Invoices - Try It Now", type="primary", use_container_width=True):
    z = io.BytesIO()
    with zipfile.ZipFile(z,"w") as zipf:
        for _, r in df.iterrows():
            d = make_pdf(r['client_name'], r['amount'], r['invoice_no'], r['date'])
            zipf.writestr(f"{r['client_name'].replace(' ','_')}_{r['invoice_no']}.pdf", d)
    st.balloons()
    st.download_button("📥 Download ALL Invoices (ZIP)", z.getvalue(), "Zikora_X_Demo_Invoices.zip", "application/zip", use_container_width=True, type="primary")

st.divider()
st.caption("Zikora X | WhatsApp: +234 7025091100 | Email: emereolegodswill132@gmail.com | Global - Remote | Built for businesses that bill fast")
