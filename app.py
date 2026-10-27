import streamlit as st
import pandas as pd
from fpdf import FPDF
import zipfile, io, os

st.set_page_config(page_title="Zikora X")
if os.path.exists("logo.png"):
    st.image("logo.png", width=200)
st.title("Zikora X")
st.write("Professional Invoice Generator")
st.divider()
file = st.file_uploader("Upload Clients CSV", type=["csv"])
def make_pdf(client, amount, inv_no, date):
    pdf = FPDF()
    pdf.add_page()
    if os.path.exists("logo.png"):
        try:
            pdf.image("logo.png", x=10, y=8, w=40)
            pdf.ln(10)
        except: pass
    pdf.set_font("Arial","B",18)
    pdf.set_text_color(0,82,204)
    pdf.cell(0,10,"ZIKORA X",ln=True,align="C")
    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"INVOICE",ln=True,align="C")
    pdf.ln(5)
    pdf.set_font("Arial","",11)
    pdf.cell(0,8,f"Invoice No: {inv_no}",ln=True)
    pdf.cell(0,8,f"Date: {date}",ln=True)
    pdf.cell(0,8,f"Client: {client}",ln=True)
    pdf.ln(4)
    pdf.set_fill_color(240,244,255)
    pdf.set_font("Arial","B",12)
    pdf.cell(0,10,f" Amount Due: NGN {amount}",ln=True,fill=True)
    pdf.ln(10)
    pdf.set_font("Arial","",10)
    pdf.cell(0,6,"WhatsApp: +234 7025091100",ln=True)
    pdf.cell(0,6,"Email: emereolegodswill132@gmail.com",ln=True)
    pdf.cell(0,6,"Location: Global - Remote",ln=True)
    out = pdf.output(dest='S')
    return out.encode('latin1') if isinstance(out,str) else bytes(out)
if file:
    df = pd.read_csv(file)
    st.success(f"{len(df)} clients loaded")
    st.dataframe(df)
    if st.button("Generate Invoices", type="primary"):
        z = io.BytesIO()
        with zipfile.ZipFile(z,"w") as zipf:
            for _, r in df.iterrows():
                pdf_data = make_pdf(r['client_name'], r['amount'], r['invoice_no'], r['date'])
                zipf.writestr(f"ZikoraX_{r['client_name']}.pdf", pdf_data)
        st.balloons()
        st.success("Done! Download below")
        st.download_button("Download ALL Invoices as ZIP", z.getvalue(), "ZikoraX_invoices.zip", "application/zip", type="primary")
st.divider()
if os.path.exists("logo.png"):
    st.image("logo.png", width=100)
st.markdown("**Zikora X**")
st.markdown("WhatsApp: +234 7025091100")
st.markdown("Email: emereolegodswill132@gmail.com")
st.markdown("Location: Global - Remote")
