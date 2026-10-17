# SWYNEX Technologies — Task 3: Interactive Dashboard

An interactive Titanic passenger analytics dashboard built with Python, Pandas, Streamlit, and Plotly.

## Features
- KPI cards: passenger count, survivors, survival rate, average fare
- Filters: sex, passenger class, embarkation port, and age range
- Interactive charts: survival counts, survival rate by class and sex, age/fare distributions, and passengers by embarkation port
- Filtered data table and CSV download

## Run on Windows
1. Extract this project ZIP.
2. Open the `SWYNEX-Interactive-Dashboard` folder.
3. Click the File Explorer address bar, type `cmd`, and press Enter.
4. Install dependencies:
   `python -m pip install -r requirements.txt`
5. Start the dashboard:
   `python -m streamlit run app.py`
6. Open the local URL shown in Command Prompt (usually `http://localhost:8501`) if the browser does not open automatically.

## Project structure
- `app.py` — dashboard code
- `data/titanic_cleaned.csv` — cleaned dataset from Task 1
- `requirements.txt` — required packages

## Submission
Upload the contents of this folder to a public GitHub repository named `SWYNEX-Interactive-Dashboard`. Run the dashboard, verify the filters and charts, take a screenshot of the actual running dashboard, and include the GitHub link and a LinkedIn post link in the SWYNEX submission.

This dashboard is descriptive and does not claim that observed associations prove causation.
