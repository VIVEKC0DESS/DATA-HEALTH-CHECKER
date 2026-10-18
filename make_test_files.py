import pandas as pd

# 60,000 rows: should be rejected
pd.DataFrame({"a": range(60000)}).to_csv("big.csv", index=False)

# Special characters saved in latin-1: old code would crash
pd.DataFrame({"name": ["José", "Zoë"], " age ": [25, 30]}).to_csv(
    "latin.csv", index=False, encoding="latin-1"
)

# Empty file
open("empty.csv", "w").close()