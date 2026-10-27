import streamlit as st
import pandas as pd
st.title("Zikora X")
file = st.file_uploader("Upload Clients CSV", type=["csv"])
if file:
    df = pd.read_csv(file)
    st.success("UPLOAD WORKS!")
    st.dataframe(df)
st.write("Zikora X | WhatsApp: +234 7025091100 | Email: emereolegodswill132@gmail.com | Global - Remote")
