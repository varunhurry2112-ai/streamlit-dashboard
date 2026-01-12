import streamlit as st
import pandas as pd

st.title("My First Streamlit Dashboard")

st.write("Upload an Excel file")

file = st.file_uploader("Choose file", type=["xlsx"])

if file:
    df = pd.read_excel(file)
    st.dataframe(df)
