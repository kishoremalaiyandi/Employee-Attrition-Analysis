
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Employee Attrition Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        return pd.read_excel(uploaded_file, sheet_name="Raw Data")
    default_file = Path(__file__).parent / "Employee_Attrition_Analysis.xlsx"
    if default_file.exists():
        return pd.read_excel(default_file, sheet_name="Raw Data")
    return None

st.title("📊 Employee Attrition Analytics")
st.caption("Interactive HR analytics dashboard built from the Employee Attrition Analysis dataset.")

with st.sidebar:
    st.header("Data & Filters")
    uploaded = st.file_uploader("Upload Excel file (optional)", type=["xlsx"])
    df = load_data(uploaded)

if df is None:
    st.warning("Upload the Employee Attrition Analysis Excel file to start.")
    st.stop()

# Normalize useful fields
df["AttritionLabel"] = df["Attrition"].map({1: "Left", 0: "Stayed"}).fillna(df.get("AttritionLabel"))
df["AgeBand"] = df["AgeBand"].astype(str)
df["IncomeBand"] = df["IncomeBand"].astype(str)

with st.sidebar:
    departments = sorted(df["Department"].dropna().unique())
    roles = sorted(df["JobRole"].dropna().unique())
    overtime = sorted(df["OverTime"].dropna().unique())
    selected_dept = st.multiselect("Department", departments, default=departments)
    selected_role = st.multiselect("Job Role", roles, default=roles)
    selected_ot = st.multiselect("Overtime", overtime, default=overtime)

filtered = df[
    df["Department"].isin(selected_dept)
    & df["JobRole"].isin(selected_role)
    & df["OverTime"].isin(selected_ot)
].copy()

total = len(filtered)
left = int((filtered["Attrition"] == 1).sum())
rate = (left / total * 100) if total else 0
avg_income = filtered["MonthlyIncome"].mean() if total else 0
avg_age = filtered["Age"].mean() if total else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Employees", f"{total:,}")
c2.metric("Attrition Rate", f"{rate:.2f}%")
c3.metric("Employees Left", f"{left:,}")
c4.metric("Avg. Monthly Income", f"${avg_income:,.0f}")

st.divider()

tab1, tab2, tab3 = st.tabs(["📈 Dashboard", "🔎 Attrition Analysis", "💡 Insights"])

with tab1:
    st.subheader("Attrition Overview")
    a, b = st.columns(2)

    with a:
        counts = filtered["AttritionLabel"].value_counts().rename_axis("Status").reset_index(name="Employees")
        fig = px.pie(counts, names="Status", values="Employees", hole=0.55,
                     title="Employee Attrition Distribution")
        fig.update_layout(margin=dict(t=60, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with b:
        age = filtered.groupby("AgeBand", sort=False)["Attrition"].mean().mul(100).reset_index()
        age.columns = ["Age Band", "Attrition Rate"]
        fig = px.bar(age, x="Age Band", y="Attrition Rate", text_auto=".1f",
                     title="Attrition Rate by Age Band")
        fig.update_yaxes(title="Attrition Rate (%)")
        st.plotly_chart(fig, use_container_width=True)

    a, b = st.columns(2)
    with a:
        dep = filtered.groupby("Department")["Attrition"].mean().mul(100).sort_values(ascending=False).reset_index()
        dep.columns = ["Department", "Attrition Rate"]
        fig = px.bar(dep, x="Department", y="Attrition Rate", text_auto=".1f",
                     title="Attrition Rate by Department")
        fig.update_yaxes(title="Attrition Rate (%)")
        st.plotly_chart(fig, use_container_width=True)

    with b:
        ot = filtered.groupby("OverTime")["Attrition"].mean().mul(100).reset_index()
        ot.columns = ["Overtime", "Attrition Rate"]
        fig = px.bar(ot, x="Overtime", y="Attrition Rate", text_auto=".1f",
                     title="Attrition Rate by Overtime")
        fig.update_yaxes(title="Attrition Rate (%)")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Detailed Employee Attrition Analysis")

    role = filtered.groupby("JobRole")["Attrition"].mean().mul(100).sort_values(ascending=False).reset_index()
    role.columns = ["Job Role", "Attrition Rate"]
    st.plotly_chart(
        px.bar(role, x="Attrition Rate", y="Job Role", orientation="h",
               text_auto=".1f", title="Attrition Rate by Job Role"),
        use_container_width=True
    )

    a, b = st.columns(2)
    with a:
        travel = filtered.groupby("BusinessTravel")["Attrition"].mean().mul(100).reset_index()
        travel.columns = ["Business Travel", "Attrition Rate"]
        st.plotly_chart(px.bar(travel, x="Business Travel", y="Attrition Rate",
                               text_auto=".1f", title="Attrition vs Business Travel"),
                        use_container_width=True)
    with b:
        sat = filtered.groupby("JobSatisfaction")["Attrition"].mean().mul(100).reset_index()
        sat.columns = ["Job Satisfaction", "Attrition Rate"]
        st.plotly_chart(px.line(sat, x="Job Satisfaction", y="Attrition Rate",
                                markers=True, title="Attrition vs Job Satisfaction"),
                        use_container_width=True)

    a, b = st.columns(2)
    with a:
        wlb = filtered.groupby("WorkLifeBalance")["Attrition"].mean().mul(100).reset_index()
        wlb.columns = ["Work-Life Balance", "Attrition Rate"]
        st.plotly_chart(px.bar(wlb, x="Work-Life Balance", y="Attrition Rate",
                               text_auto=".1f", title="Attrition vs Work-Life Balance"),
                        use_container_width=True)
    with b:
        income = filtered.groupby("IncomeBand")["Attrition"].mean().mul(100).reset_index()
        income.columns = ["Income Band", "Attrition Rate"]
        st.plotly_chart(px.bar(income, x="Income Band", y="Attrition Rate",
                               text_auto=".1f", title="Attrition by Income Band"),
                        use_container_width=True)

    st.subheader("Filtered Employee Data")
    st.dataframe(filtered, use_container_width=True, height=360)

with tab3:
    st.subheader("Key Findings")
    st.markdown(f"""
    - **Overall attrition rate:** {rate:.2f}% for the current filter selection.
    - **Overtime:** employees working overtime generally show substantially higher attrition.
    - **Age:** younger employees, particularly the under-25 group, show elevated attrition.
    - **Income:** lower income bands tend to have higher attrition.
    - **Job roles:** attrition varies considerably across roles, with some operational/sales roles showing higher risk.
    - **Work-life balance:** low work-life-balance scores are associated with higher attrition.
    - **Job satisfaction:** lower satisfaction levels are associated with greater employee turnover.
    """)

    st.subheader("Recommended Retention Actions")
    st.markdown("""
    1. Monitor and reduce excessive overtime and workload.
    2. Create mentoring and career-development programs for early-career employees.
    3. Review compensation and promotion pathways for lower-income groups.
    4. Investigate high-attrition job roles and departments individually.
    5. Improve work-life balance and employee-support initiatives.
    6. Conduct regular employee-satisfaction surveys and act on recurring concerns.
    """)

st.divider()
st.caption("Note: This dashboard identifies associations in the dataset; it does not establish that a factor directly causes attrition.")
