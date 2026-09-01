
# Employee Attrition Analytics — Deployed-Ready Streamlit Project

## Project
Interactive HR analytics dashboard based on `Employee_Attrition_Analysis.xlsx`.

### Features
- Overall employee and attrition KPIs
- Department, job-role and overtime filters
- Attrition distribution
- Attrition by age band, department and overtime
- Attrition by job role, business travel, job satisfaction and work-life balance
- Attrition by income band
- Filtered employee table
- Key findings and retention recommendations

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The included Excel file is used automatically. Users can also upload another `.xlsx` file from the sidebar.

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload:
   - `app.py`
   - `requirements.txt`
   - `Employee_Attrition_Analysis.xlsx`
3. Open Streamlit Community Cloud and connect the repository.
4. Select `app.py` as the main file.
5. Deploy.

## Research-paper sections
The dashboard supports the accompanying paper sections:
Abstract, Introduction, Problem Statement, Objectives, Dataset Description,
Data Preprocessing, Exploratory Data Analysis, Employee Attrition Analysis,
Key Findings, Recommendations, Conclusion, and References.

## Dataset
1,470 employee records and 35 attributes from the supplied workbook.
