import streamlit as st
import plotly.express as px
from loader import load_file
from checks import check_missing, check_duplicates, check_constant_columns

st.set_page_config(page_title="Data Health Checker", layout="wide")
st.title("Data Health Checker")

SEVERITY_COLORS = {"High": "#e74c3c", "Medium": "#f39c12", "Low": "#2ecc71"}
SEVERITY_ICONS = {"High": "🔴", "Medium": "🟠", "Low": "🟢", "None": "🟢"}

file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if file is not None:
    try:
        df = load_file(file)
    except ValueError as error:
        st.error(str(error))
        st.stop()

    # Run all checks once
    missing = check_missing(df)
    dup = check_duplicates(df)
    constant = check_constant_columns(df)

    # ---------- Summary cards ----------
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Rows", f"{df.shape[0]:,}")
    c2.metric("Columns", df.shape[1])
    c3.metric("Columns with missing values", len(missing))
    c4.metric("Duplicate rows", f"{dup['count']:,}")
    c5.metric("Constant / empty columns", len(constant))

    # ---------- Tabs ----------
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Overview", "Missing values", "Duplicates", "Constant columns"]
    )

    # ----- Overview -----
    with tab1:
        st.subheader("Data preview")
        st.dataframe(df.head(10))

        st.subheader("Quick status")
        st.write("✅ No missing values" if missing.empty
                 else f"⚠️ {len(missing)} column(s) have missing values")
        st.write("✅ No duplicate rows" if dup["count"] == 0
                 else f"⚠️ {dup['count']:,} duplicate rows")
        st.write("✅ No constant or empty columns" if constant.empty
                 else f"⚠️ {len(constant)} constant or empty column(s)")

    # ----- Missing values -----
    with tab2:
        if missing.empty:
            st.success("No missing values found.")
        else:
            fig = px.bar(
                missing,
                x="missing_percent",
                y="column",
                orientation="h",
                color="severity",
                color_discrete_map=SEVERITY_COLORS,
                text="missing_percent",
                labels={"missing_percent": "Missing (%)", "column": ""},
                title="Missing values by column",
            )
            fig.update_layout(
                yaxis={"categoryorder": "total ascending"},
                xaxis_range=[0, 100],
            )
            st.plotly_chart(fig)

            st.write("Click a column for the explanation:")
            for _, row in missing.iterrows():
                icon = SEVERITY_ICONS[row["severity"]]
                title = f"{icon} {row['column']}: {row['missing_percent']}% missing"
                with st.expander(title):
                    st.write(row["explanation"])

    # ----- Duplicates -----
    with tab3:
        if dup["count"] == 0:
            st.success(dup["explanation"])
        else:
            unique_rows = len(df) - dup["count"]
            fig = px.pie(
                names=["Unique rows", "Duplicate rows"],
                values=[unique_rows, dup["count"]],
                hole=0.5,
                color=["Unique rows", "Duplicate rows"],
                color_discrete_map={
                    "Unique rows": "#2ecc71",
                    "Duplicate rows": "#e74c3c",
                },
                title="Unique vs duplicate rows",
            )
            st.plotly_chart(fig)

            icon = SEVERITY_ICONS[dup["severity"]]
            with st.expander(f"{icon} {dup['count']:,} duplicate rows: explanation"):
                st.write(dup["explanation"])
            with st.expander("Show some duplicated rows"):
                st.dataframe(dup["sample"])

    # ----- Constant columns -----
    with tab4:
        if constant.empty:
            st.success("No constant or empty columns found.")
        else:
            for _, row in constant.iterrows():
                with st.expander(f"⚠️ {row['column']}: {row['problem']}"):
                    st.write(row["explanation"])