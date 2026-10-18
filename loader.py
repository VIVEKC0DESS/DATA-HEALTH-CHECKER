import pandas as pd

MAX_ROWS = 60000


def _read_csv(file):
    # Try common encodings until one works
    for encoding in ["utf-8-sig", "latin-1"]:
        try:
            file.seek(0)  # go back to the start of the file
            return pd.read_csv(file, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("Could not read the text in this CSV file.")


def load_file(file):
    """Read an uploaded CSV/Excel file and return a clean DataFrame.
    Raises ValueError with a friendly message if something is wrong."""
    name = file.name.lower()

    try:
        if name.endswith(".csv"):
            df = _read_csv(file)
        elif name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            raise ValueError("Please upload a CSV or Excel (.xlsx) file.")
    except ValueError:
        raise  # keep our own friendly messages
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty.")
    except pd.errors.ParserError:
        raise ValueError("The file is badly formatted and could not be read.")
    except Exception:
        raise ValueError("This file could not be read. Is it a valid CSV or Excel file?")

    if df.empty:
        raise ValueError("The file has no data rows.")

    if len(df) > MAX_ROWS:
        raise ValueError(
            f"The file has {len(df):,} rows. The limit is {MAX_ROWS:,} rows."
        )

    # Clean column names (remove extra spaces)
    df.columns = df.columns.astype(str).str.strip()

    return df