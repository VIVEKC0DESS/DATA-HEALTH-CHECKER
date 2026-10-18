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