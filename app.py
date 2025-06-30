import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Page configuration
st.set_page_config(
    page_title="EA Attrition Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Load data (cached)
@st.cache_data
def load_data():
    df = pd.read_csv("EA.csv")
    return df

data = load_data()

# 3. Sidebar filters
st.sidebar.title("Filters & Controls")

attr_sel = st.sidebar.multiselect(
    "Attrition Status",
    options=data["attrition"].unique(),
    default=list(data["attrition"].unique())
)

age_min, age_max = int(data["age"].min()), int(data["age"].max())
age_sel = st.sidebar.slider(
    "Age Range",
    min_value=age_min,
    max_value=age_max,
    value=(age_min, age_max)
)

dept_sel = st.sidebar.multiselect(
    "Department",
    options=data["department"].unique(),
    default=list(data["department"].unique())
)

gender_sel = st.sidebar.multiselect(
    "Gender",
    options=data["gender"].unique(),
    default=list(data["gender"].unique())
)

# Apply filters
df = data.query(
    "attrition in @attr_sel and "
    "age >= @age_sel[0] and age <= @age_sel[1] and "
    "department in @dept_sel and gender in @gender_sel"
)

# 4. Create tabs
tabs = st.tabs([
    "1 Attrition Count",
    "2 Age Histogram",
    "3 Dept vs Attrition",
    "4 Income KDE",
    "5 JobSat Boxplot",
    "6 Correlation",
    "7 Age vs Income",
    "8 Tenure vs Attrition",
    "9 Gender vs Attrition",
    "10 Education Dist",
    "11 Overtime vs Attrition",
    "12 Travel vs Attrition",
    "13 Distance Dist",
    "14 Perf Rating",
    "15 Income by Role",
    "16 Companies Worked",
    "17 Training Times",
    "18 Env Satisfaction",
    "19 WLB Satisfaction",
    "20 Stock Option Level"
])

# Chart 1: Attrition Count
with tabs[0]:
    st.markdown("**Attrition Count**: Number of employees who stayed vs left.")
    cnt = df["attrition"].value_counts().reset_index()
    cnt.columns = ["Attrition", "Count"]
    chart = alt.Chart(cnt).mark_bar().encode(
        x="Attrition:N",
        y="Count:Q",
        color="Attrition:N"
    )
    st.altair_chart(chart, use_container_width=True)

# Chart 2: Age Histogram
with tabs[1]:
    st.markdown("**Age Distribution**: Histogram of employee ages.")
    hist = alt.Chart(df).mark_bar().encode(
        alt.X("age:Q", bin=alt.Bin(maxbins=30)),
        y="count():Q"
    )
    st.altair_chart(hist, use_container_width=True)

# Chart 3: Department vs Attrition
with tabs[2]:
    st.markdown("**Department vs Attrition**: Attrition across departments.")
    dept = df.groupby(["department", "attrition"]).size().reset_index(name="Count")
    dept_chart = alt.Chart(dept).mark_bar().encode(
        x="department:N",
        y="Count:Q",
        color="attrition:N",
        column="attrition:N"
    )
    st.altair_chart(dept_chart, use_container_width=True)

# Chart 4: Monthly Income KDE
with tabs[3]:
    st.markdown("**Monthly Income Distribution**: KDE plot of monthly incomes.")
    fig, ax = plt.subplots()
    sns.kdeplot(df["monthlyincome"], fill=True, ax=ax)
    ax.set_xlabel("Monthly Income")
    ax.set_ylabel("Density")
    st.pyplot(fig)

# Chart 5: Job Satisfaction Boxplot
with tabs[4]:
    st.markdown("**Job Satisfaction vs Attrition**: Boxplot by attrition status.")
    fig, ax = plt.subplots()
    sns.boxplot(x="attrition", y="jobsatisfaction", data=df, ax=ax)
    ax.set_xlabel("Attrition")
    ax.set_ylabel("Job Satisfaction")
    st.pyplot(fig)

# Chart 6: Correlation Heatmap
with tabs[5]:
    st.markdown("**Correlation Heatmap**: Numeric feature correlations.")
    corr = df.select_dtypes(include="number").corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", ax=ax)
    st.pyplot(fig)

# Chart 7: Age vs Monthly Income Scatter
with tabs[6]:
    st.markdown("**Age vs Monthly Income**: Scatter plot with tooltips.")
    scatter = alt.Chart(df).mark_circle(size=60).encode(
        x="age:Q",
        y="monthlyincome:Q",
        color="attrition:N",
        tooltip=["age", "monthlyincome"]
    ).interactive()
    st.altair_chart(scatter, use_container_width=True)

# Chart 8: Years at Company vs Attrition
with tabs[7]:
    st.markdown("**Tenure vs Attrition**: Line chart of attrition by years at company.")
    tenure = df.groupby(["yearsAtCompany", "attrition"]).size().reset_index(name="Count")
    line = alt.Chart(tenure).mark_line(point=True).encode(
        x="yearsAtCompany:Q",
        y="Count:Q",
        color="attrition:N"
    )
    st.altair_chart(line, use_container_width=True)

# Chart 9: Gender vs Attrition
with tabs[8]:
    st.markdown("**Gender vs Attrition**: Comparison of attrition by gender.")
    gen = df.groupby(["gender", "attrition"]).size().reset_index(name="Count")
    gen_chart = alt.Chart(gen).mark_bar().encode(
        x="gender:N",
        y="Count:Q",
        color="attrition:N",
        column="attrition:N"
    )
    st.altair_chart(gen_chart, use_container_width=True)

# Chart 10: Education Level Distribution
with tabs[9]:
    st.markdown("**Education Level Distribution**: Counts by level.")
    edu = df["education"].value_counts().reset_index()
    edu.columns = ["Education", "Count"]
    edu_chart = alt.Chart(edu).mark_bar().encode(
        x="Education:N",
        y="Count:Q"
    )
    st.altair_chart(edu_chart, use_container_width=True)

# Chart 11: OverTime vs Attrition
with tabs[10]:
    st.markdown("**OverTime vs Attrition**: Who works overtime?")
    ot = df.groupby(["overtime", "attrition"]).size().reset_index(name="Count")
    ot_chart = alt.Chart(ot).mark_bar().encode(
        x="overtime:N",
        y="Count:Q",
        color="attrition:N",
        column="attrition:N"
    )
    st.altair_chart(ot_chart, use_container_width=True)

# Chart 12: Business Travel vs Attrition
with tabs[11]:
    st.markdown("**Business Travel vs Attrition**")
    bt = df.groupby(["businesstravel", "attrition"]).size().reset_index(name="Count")
    bt_chart = alt.Chart(bt).mark_bar().encode(
        x="businesstravel:N",
        y="Count:Q",
        color="attrition:N",
        column="attrition:N"
    )
    st.altair_chart(bt_chart, use_container_width=True)

# Chart 13: Distance From Home Histogram
with tabs[12]:
    st.markdown("**Distance From Home**: Commute distance distribution.")
    dist = alt.Chart(df).mark_bar().encode(
        alt.X("distancefromhome:Q", bin=alt.Bin(maxbins=20)),
        y="count():Q"
    )
    st.altair_chart(dist, use_container_width=True)

# Chart 14: Performance Rating
with tabs[13]:
    st.markdown("**Performance Rating**: Counts by rating.")
    pr = df["performancerating"].value_counts().reset_index()
    pr.columns = ["Rating", "Count"]
    pr_chart = alt.Chart(pr).mark_bar().encode(
        x="Rating:N",
        y="Count:Q"
    )
    st.altair_chart(pr_chart, use_container_width=True)

# Chart 15: Income by Job Role
with tabs[14]:
    st.markdown("**Monthly Income by Job Role**: Boxplots.")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(x="jobrole", y="monthlyincome", data=df, ax=ax)
    ax.set_xlabel("Job Role")
    ax.set_ylabel("Monthly Income")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

# Chart 16: Num Companies Worked
with tabs[15]:
    st.markdown("**Number of Companies Worked**: Distribution.")
    nc = alt.Chart(df).mark_bar().encode(
        alt.X("numcompaniesworked:Q", bin=alt.Bin(maxbins=10)),
        y="count():Q"
    )
    st.altair_chart(nc, use_container_width=True)

# Chart 17: Training Times Last Year
with tabs[16]:
    st.markdown("**Training Times Last Year**: Distribution.")
    tt = alt.Chart(df).mark_bar().encode(
        alt.X("trainingtimslastyear:Q", bin=alt.Bin(maxbins=10)),
        y="count():Q"
    )
    st.altair_chart(tt, use_container_width=True)

# Chart 18: Environment Satisfaction
with tabs[17]:
    st.markdown("**Environment Satisfaction vs Attrition**: Boxplot.")
    fig, ax = plt.subplots()
    sns.boxplot(x="attrition", y="environmentsatisfaction", data=df, ax=ax)
    st.pyplot(fig)

# Chart 19: Work Life Balance
with tabs[18]:
    st.markdown("**Work Life Balance vs Attrition**: Boxplot.")
    fig, ax = plt.subplots()
    sns.boxplot(x="attrition", y="worklifebalance", data=df, ax=ax)
    st.pyplot(fig)

# Chart 20: Stock Option Level
with tabs[19]:
    st.markdown("**Stock Option Level**: Counts by level.")
    sol = df["stockoptionlevel"].value_counts().reset_index()
    sol.columns = ["Level", "Count"]
    sol_chart = alt.Chart(sol).mark_bar().encode(
        x="Level:N",
        y="Count:Q"
    )
    st.altair_chart(sol_chart, use_container_width=True)

# Data sample at the bottom
st.markdown("### Data Sample")
st.dataframe(df.head(), use_container_width=True)
