
---

### `app.py`

```python
import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

# ─── 1. PAGE CONFIG ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EA Attrition Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── 2. LOAD DATA ───────────────────────────────────────────────────────────
    df = pd.read_csv("EA.csv")

# ─── 3. SIDEBAR CONTROLS ────────────────────────────────────────────────────
st.sidebar.title("🔧 Filters & Controls")

# Attrition filter
attr_sel = st.sidebar.multiselect(
    "Attrition Status",
    options=data["attrition"].unique(),
    default=list(data["attrition"].unique()),
)

# Age slider
age_min, age_max = int(data["age"].min()), int(data["age"].max())
age_sel = st.sidebar.slider("Age Range", age_min, age_max, (age_min, age_max))

# Department filter
dept_sel = st.sidebar.multiselect(
    "Department",
    options=data["department"].unique(),
    default=list(data["department"].unique()),
)

# Gender filter
gender_sel = st.sidebar.multiselect(
    "Gender",
    options=data["gender"].unique(),
    default=list(data["gender"].unique()),
)

# Apply filters
df = data.query(
    "attrition in @attr_sel and age >= @age_sel[0] and age <= @age_sel[1] and "
    "department in @dept_sel and gender in @gender_sel"
)

# ─── 4. TAB LAYOUT ──────────────────────────────────────────────────────────
tabs = st.tabs([
    "1️⃣ Attrition Count",
    "2️⃣ Age Histogram",
    "3️⃣ Dept vs Attrition",
    "4️⃣ Monthly Income Dist",
    "5️⃣ JobSat vs Attrition",
    "6️⃣ Correlation Heatmap",
    "7️⃣ Age vs Income Scatter",
    "8️⃣ Tenure vs Attrition",
    "9️⃣ Gender vs Attrition",
    "🔟 Edu Level Dist",
    "1️⃣1️⃣ Overtime vs Attrition",
    "1️⃣2️⃣ Business Travel",
    "1️⃣3️⃣ Dist From Home",
    "1️⃣4️⃣ Perf Rating",
    "1️⃣5️⃣ Salary by Role",
    "1️⃣6️⃣ Companies Worked",
    "1️⃣7️⃣ Training Times",
    "1️⃣8️⃣ Env Sat",
    "1️⃣9️⃣ WLB Sat",
    "2️⃣0️⃣ Stock Option Level",
])

# ─── Chart 1 ────────────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown("**Attrition Count**: How many employees stayed vs left the company.")
    count_df = df["attrition"].value_counts().reset_index()
    count_df.columns = ["Attrition", "Count"]
    chart = alt.Chart(count_df).mark_bar().encode(
        x="Attrition:N", y="Count:Q", color="Attrition:N"
    )
    st.altair_chart(chart, use_container_width=True)

# ─── Chart 2 ────────────────────────────────────────────────────────────────
with tabs[1]:
    st.markdown("**Age Distribution**: Histogram of employee ages.")
    hist = alt.Chart(df).mark_bar().encode(
        alt.X("age:Q", bin=alt.Bin(maxbins=30)), y="count():Q"
    )
    st.altair_chart(hist, use_container_width=True)

# ─── Chart 3 ────────────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown("**Department vs Attrition**: Attrition rate across departments.")
    dept_ct = df.groupby(["department", "attrition"]).size().reset_index(name="Count")
    dept_bar = alt.Chart(dept_ct).mark_bar().encode(
        x="department:N", y="Count:Q", color="attrition:N", column="attrition:N"
    )
    st.altair_chart(dept_bar, use_container_width=True)

# ─── Chart 4 ────────────────────────────────────────────────────────────────
with tabs[3]:
    st.markdown("**Monthly Income Distribution**: KDE plot of monthly income.")
    fig, ax = plt.subplots()
    sns.kdeplot(df["monthlyincome"], fill=True, ax=ax)
    ax.set_xlabel("Monthly Income")
    ax.set_ylabel("Density")
    st.pyplot(fig)

# ─── Chart 5 ────────────────────────────────────────────────────────────────
with tabs[4]:
    st.markdown("**Job Satisfaction vs Attrition**: Boxplot of job satisfaction by attrition.")
    fig, ax = plt.subplots()
    sns.boxplot(x="attrition", y="jobsatisfaction", data=df, ax=ax)
    ax.set_xlabel("Attrition")
    ax.set_ylabel("Job Satisfaction")
    st.pyplot(fig)

# ─── Chart 6 ────────────────────────────────────────────────────────────────
with tabs[5]:
    st.markdown("**Correlation Heatmap**: Relationships between numeric features.")
    num_cols = df.select_dtypes(include="number")
    corr = num_cols.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", ax=ax)
    st.pyplot(fig)

# ─── Chart 7 ────────────────────────────────────────────────────────────────
with tabs[6]:
    st.markdown("**Age vs Monthly Income**: Scatter with trendline.")
    scatter = alt.Chart(df).mark_circle(size=60).encode(
        x="age:Q", y="monthlyincome:Q", color="attrition:N", tooltip=["age","monthlyincome"]
    ).interactive()
    st.altair_chart(scatter, use_container_width=True)

# ─── Chart 8 ────────────────────────────────────────────────────────────────
with tabs[7]:
    st.markdown("**Years at Company vs Attrition**: Attrition by tenure.")
    tenure_ct = df.groupby(["yearsAtCompany","attrition"]).size().reset_index(name="Count")
    line = alt.Chart(tenure_ct).mark_line(point=True).encode(
        x="yearsAtCompany:Q", y="Count:Q", color="attrition:N"
    )
    st.altair_chart(line, use_container_width=True)

# ─── Chart 9 ────────────────────────────────────────────────────────────────
with tabs[8]:
    st.markdown("**Gender vs Attrition**: Bar chart by gender.")
    gen_ct = df.groupby(["gender","attrition"]).size().reset_index(name="Count")
    gen_bar = alt.Chart(gen_ct).mark_bar().encode(
        x="gender:N", y="Count:Q", color="attrition:N", column="attrition:N"
    )
    st.altair_chart(gen_bar, use_container_width=True)

# ─── Chart 10 ───────────────────────────────────────────────────────────────
with tabs[9]:
    st.markdown("**Education Level Distribution**: Count of education levels.")
    edu = df["education"].value_counts().reset_index()
    edu.columns = ["Education Level","Count"]
    edu_bar = alt.Chart(edu).mark_bar().encode(
        x="Education Level:N", y="Count:Q"
    )
    st.altair_chart(edu_bar, use_container_width=True)

# ─── Chart 11 ───────────────────────────────────────────────────────────────
with tabs[10]:
    st.markdown("**OverTime vs Attrition**: Who works overtime?")
    ot_ct = df.groupby(["overtime","attrition"]).size().reset_index(name="Count")
    ot_bar = alt.Chart(ot_ct).mark_bar().encode(
        x="overtime:N", y="Count:Q", color="attrition:N", column="attrition:N"
    )
    st.altair_chart(ot_bar, use_container_width=True)

# ─── Chart 12 ───────────────────────────────────────────────────────────────
with tabs[11]:
    st.markdown("**Business Travel vs Attrition**")
    bt_ct = df.groupby(["businesstravel","attrition"]).size().reset_index(name="Count")
    bt_bar = alt.Chart(bt_ct).mark_bar().encode(
        x="businesstravel:N", y="Count:Q", color="attrition:N", column="attrition:N"
    )
    st.altair_chart(bt_bar, use_container_width=True)

# ─── Chart 13 ───────────────────────────────────────────────────────────────
with tabs[12]:
    st.markdown("**Distance From Home**: Histogram of commute distance.")
    dist = alt.Chart(df).mark_bar().encode(
        alt.X("distancefromhome:Q", bin=alt.Bin(maxbins=20)), y="count():Q"
    )
    st.altair_chart(dist, use_container_width=True)

# ─── Chart 14 ───────────────────────────────────────────────────────────────
with tabs[13]:
    st.markdown("**Performance Rating**: Count by performance rating.")
    pr = df["performancerating"].value_counts().reset_index()
    pr.columns = ["Performance Rating","Count"]
    pr_bar = alt.Chart(pr).mark_bar().encode(
        x="Performance Rating:N", y="Count:Q"
    )
    st.altair_chart(pr_bar, use_container_width=True)

# ─── Chart 15 ───────────────────────────────────────────────────────────────
with tabs[14]:
    st.markdown("**Monthly Income by Job Role**: Boxplot.")
    fig, ax = plt.subplots(figsize=(8,4))
    sns.boxplot(x="jobrole", y="monthlyincome", data=df, ax=ax)
    ax.set_xlabel("Job Role")
    ax.set_ylabel("Monthly Income")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

# ─── Chart 16 ───────────────────────────────────────────────────────────────
with tabs[15]:
    st.markdown("**NumCompaniesWorked**: Histogram.")
    nc = alt.Chart(df).mark_bar().encode(
        alt.X("numcompaniesworked:Q", bin=alt.Bin(maxbins=10)), y="count():Q"
    )
    st.altair_chart(nc, use_container_width=True)

# ─── Chart 17 ───────────────────────────────────────────────────────────────
with tabs[16]:
    st.markdown("**Training Times Last Year**: Histogram.")
    tt = alt.Chart(df).mark_bar().encode(
        alt.X("trainingtimslastyear:Q", bin=alt.Bin(maxbins=10)), y="count():Q"
    )
    st.altair_chart(tt, use_container_width=True)

# ─── Chart 18 ───────────────────────────────────────────────────────────────
with tabs[17]:
    st.markdown("**Environment Satisfaction**: Boxplot by attrition.")
    fig, ax = plt.subplots()
    sns.boxplot(x="attrition", y="environmentsatisfaction", data=df, ax=ax)
    st.pyplot(fig)

# ─── Chart 19 ───────────────────────────────────────────────────────────────
with tabs[18]:
    st.markdown("**Work Life Balance**: Boxplot by attrition.")
    fig, ax = plt.subplots()
    sns.boxplot(x="attrition", y="worklifebalance", data=df, ax=ax)
    st.pyplot(fig)

# ─── Chart 20 ───────────────────────────────────────────────────────────────
with tabs[19]:
    st.markdown("**Stock Option Level**: Count by level.")
    sol = df["stockoptionlevel"].value_counts().reset_index()
    sol.columns = ["Stock Option Level","Count"]
    sol_bar = alt.Chart(sol).mark_bar().encode(
        x="Stock Option Level:N", y="Count:Q"
    )
    st.altair_chart(sol_bar, use_container_width=True)

# ─── Data Sample at Bottom ─────────────────────────────────────────────────
st.markdown("### 📋 Data Sample")
st.dataframe(df.head(), use_container_width=True)
