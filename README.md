# Data Health Checker

A conversational data quality assistant. Upload any CSV or Excel
dataset (up to 50,000 rows) and the app checks its quality, explains
every issue, creates visualizations, and lets you chat with it about
your data in plain English.

## Features

1. Domain-independent analysis: works on any dataset (hospital,
   sales, education, etc.) by reading the data's structure, not
   its subject.
2. Data quality checks: missing values, duplicates, outliers,
   invalid and inconsistent values.
3. Justified explanations: every issue explains what it is,
   why it matters, and how to fix it.
4. Quality score: an overall rating from 0 to 100.
5. Automatic visualizations: histograms, bar charts, and a
   correlation heatmap.
6. AI chat about your data (planned): ask in plain English and get
   answers based only on the uploaded dataset.
   - Chart requests: "create a boxplot of salary" or
     "show sales by month" and the app draws the chart.
   - Data questions: "which column has the most missing values?"
   - Fix discussions: if the app suggests removing a column and you
     disagree, you can discuss it and decide together.
7. Safe corrections (planned): approved fixes are applied with an
   undo option. The original file is never modified.

## How the AI chat works

- The app's own code calculates all statistics and draws all charts,
  so the numbers are accurate.
- The language model only receives the dataset's column names, data
  types, quality report, and a few sample rows. It does not receive
  the full dataset.
- It replies with an explanation and, for chart or fix requests,
  a structured instruction. The app then runs that instruction from
  a fixed list of allowed operations.
- The chat is limited to the uploaded dataset and does not answer
  unrelated questions.

## Workflow

Upload -> Detect column types -> Quality checks -> Explanations and
score -> Visualizations -> Chat -> Apply fixes -> Export

## Tech stack

Python, Pandas, Scikit-learn, Plotly, Streamlit, LLM API

## Status

Phase 1 in progress: file upload and basic report.

## Run locally

pip install -r requirements.txt
streamlit run app.py