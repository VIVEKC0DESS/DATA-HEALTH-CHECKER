import streamlit as st
from loader import load_file

st.title("Data Health Checker")

file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if file is not None:
    try:
        df = load_file(file)
    except ValueError as error:
        st.error(str(error))
        st.stop()

    st.success("File loaded successfully")
    st.write("Rows:", df.shape[0], "| Columns:", df.shape[1])
    st.dataframe(df.head())
