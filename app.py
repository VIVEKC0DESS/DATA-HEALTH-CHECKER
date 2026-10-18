import streamlit as st
from loader import load_file
from checks import check_missing, check_duplicates, check_constant_columns

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

    # --- Missing values ---
    st.subheader("Missing values")
    missing = check_missing(df)
    if missing.empty:
        st.success("No missing values found.")
    else:
        st.dataframe(
            missing[["column", "missing_count", "missing_percent", "severity"]]
        )
        for _, row in missing.iterrows():
            st.write("- " + row["explanation"])

    # --- Duplicate rows ---
    st.subheader("Duplicate rows")
    dup = check_duplicates(df)
    if dup["count"] == 0:
        st.success(dup["explanation"])
    else:
        st.warning(f"Severity: {dup['severity']}")
        st.write(dup["explanation"])
        st.write("Some of the duplicated rows:")
        st.dataframe(dup["sample"])

    # --- Constant / empty columns ---
    st.subheader("Constant or empty columns")
    constant = check_constant_columns(df)
    if constant.empty:
        st.success("No constant or empty columns found.")
    else:
        for _, row in constant.iterrows():
            st.write("- " + row["explanation"])
