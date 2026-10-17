import streamlit as st
import pandas as pd

st.title("Data Health Checker")

file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if file is not None:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.write("Rows:", df.shape[0], "| Columns:", df.shape[1])
    st.dataframe(df.head())
