import pandas as pd


def check_missing(df):
    """Return a table of columns that have missing values,
    with count, percentage, severity and an explanation."""
    total_rows = len(df)
    counts = df.isna().sum()

    rows = []
    for column in df.columns:
        missing = int(counts[column])
        if missing == 0:
            continue  # skip columns with no missing values

        percent = round(missing / total_rows * 100, 1)

        if percent >= 50:
            severity = "High"
            advice = "More than half of this column is empty. It may be too incomplete to be useful. Consider dropping it unless you really need it."
        elif percent >= 10:
            severity = "Medium"
            advice = "A noticeable part of this column is empty. Averages and charts may be biased. Consider filling the blanks (median for numbers, most common value for categories)."
        else:
            severity = "Low"
            advice = "Only a small part is empty. Filling the blanks or removing those rows is usually safe."

        explanation = (
            f"Column '{column}' has {missing} missing values "
            f"({percent}% of {total_rows} rows). {advice}"
        )

        rows.append({
            "column": column,
            "missing_count": missing,
            "missing_percent": percent,
            "severity": severity,
            "explanation": explanation,
        })

    result = pd.DataFrame(
        rows,
        columns=["column", "missing_count", "missing_percent", "severity", "explanation"],
    )
    return result.sort_values("missing_percent", ascending=False).reset_index(drop=True)
def check_duplicates(df):
    """Find fully duplicated rows."""
    total_rows = len(df)
    count = int(df.duplicated().sum())
    percent = round(count / total_rows * 100, 1) if total_rows else 0.0

    if count == 0:
        return {
            "count": 0,
            "percent": 0.0,
            "severity": "None",
            "explanation": "No duplicate rows found.",
            "sample": df.iloc[0:0],
        }

    if percent >= 10:
        severity = "High"
    elif percent >= 1:
        severity = "Medium"
    else:
        severity = "Low"

    explanation = (
        f"Found {count} duplicate rows ({percent}% of {total_rows} rows). "
        "Duplicates can inflate totals and counts and bias statistics. "
        "They may be accidental copies, or genuine repeats such as two "
        "identical purchases. If the data has a unique ID column, check "
        "whether the IDs repeat before removing them."
    )

    sample = df[df.duplicated(keep=False)].head(10)

    return {
        "count": count,
        "percent": percent,
        "severity": severity,
        "explanation": explanation,
        "sample": sample,
    }


def check_constant_columns(df):
    """Find columns with one value only, or no values at all."""
    rows = []
    for column in df.columns:
        unique_values = df[column].nunique()  # ignores missing values

        if unique_values == 0:
            problem = "Empty column"
            explanation = (
                f"Column '{column}' is completely empty. "
                "It has no information and can be dropped."
            )
        elif unique_values == 1:
            value = df[column].dropna().iloc[0]
            problem = "Constant column"
            explanation = (
                f"Column '{column}' has the same value ('{value}') in every "
                "row that has data. It cannot help distinguish rows, so it is "
                "usually useless for analysis and charts."
            )
        else:
            continue

        rows.append({
            "column": column,
            "problem": problem,
            "explanation": explanation,
        })

    return pd.DataFrame(rows, columns=["column", "problem", "explanation"])