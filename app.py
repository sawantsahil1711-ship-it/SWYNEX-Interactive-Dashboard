from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Titanic Passenger Analytics", page_icon="🚢", layout="wide")
st.title("🚢 Titanic Passenger Analytics Dashboard")
st.caption("SWYNEX Technologies — Task 3: Interactive Dashboard")
st.write("Explore passenger demographics and survival outcomes. Use the sidebar filters to interact with the dashboard.")

DATA_PATH = Path(__file__).parent / "data" / "titanic_cleaned.csv"

@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    for col in ["Survived", "Pclass", "Age", "Fare"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    return data

df = load_data(DATA_PATH)
required = {"Survived", "Pclass", "Sex", "Age", "Fare", "Embarked"}
missing = required - set(df.columns)
if missing:
    st.error(f"Dataset missing required columns: {', '.join(sorted(missing))}")
    st.write("Available columns:", list(df.columns))
    st.stop()

with st.sidebar:
    st.header("Dashboard Filters")
    sexes = sorted(df["Sex"].dropna().astype(str).unique().tolist())
    chosen_sex = st.multiselect("Sex", sexes, default=sexes)
    classes = sorted(df["Pclass"].dropna().unique().tolist())
    chosen_class = st.multiselect("Passenger class", classes, default=classes,
                                  format_func=lambda x: f"Class {int(x)}")
    ports = sorted(df["Embarked"].dropna().astype(str).unique().tolist())
    chosen_port = st.multiselect("Embarkation port", ports, default=ports)
    ages = df["Age"].dropna()
    min_age = int(ages.min()) if not ages.empty else 0
    max_age = int(ages.max()) if not ages.empty else 100
    age_range = st.slider("Age range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

filtered = df[
    df["Sex"].astype(str).isin(chosen_sex)
    & df["Pclass"].isin(chosen_class)
    & df["Embarked"].astype(str).isin(chosen_port)
    & df["Age"].between(age_range[0], age_range[1])
].copy()

if filtered.empty:
    st.warning("No records match these filters. Change the filters in the sidebar.")
    st.stop()

total = len(filtered)
survivors = int((filtered["Survived"] == 1).sum())
survival_rate = survivors / total * 100
avg_fare = filtered["Fare"].mean()
avg_age = filtered["Age"].mean()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Passengers", f"{total:,}")
k2.metric("Survivors", f"{survivors:,}")
k3.metric("Survival rate", f"{survival_rate:.1f}%")
k4.metric("Average fare", f"{avg_fare:.2f}" if pd.notna(avg_fare) else "N/A")
st.caption(f"Average passenger age: {avg_age:.1f} years" if pd.notna(avg_age) else "Average passenger age unavailable.")

left, right = st.columns(2)
with left:
    counts = filtered["Survived"].map({0: "Did not survive", 1: "Survived"}).value_counts().reindex(["Did not survive", "Survived"], fill_value=0).rename_axis("Outcome").reset_index(name="Passengers")
    st.plotly_chart(px.bar(counts, x="Outcome", y="Passengers", color="Outcome", text="Passengers", title="Passenger Survival Counts"), use_container_width=True)
with right:
    by_class = filtered.groupby("Pclass")["Survived"].mean().mul(100).rename("Survival rate (%)").reset_index()
    by_class["Class"] = by_class["Pclass"].apply(lambda x: f"Class {int(x)}")
    st.plotly_chart(px.bar(by_class, x="Class", y="Survival rate (%)", text=by_class["Survival rate (%)"].map(lambda x: f"{x:.1f}%"), title="Survival Rate by Passenger Class", range_y=[0,100]), use_container_width=True)

left, right = st.columns(2)
with left:
    by_sex = filtered.groupby("Sex")["Survived"].mean().mul(100).rename("Survival rate (%)").reset_index()
    st.plotly_chart(px.bar(by_sex, x="Sex", y="Survival rate (%)", color="Sex", text=by_sex["Survival rate (%)"].map(lambda x: f"{x:.1f}%"), title="Survival Rate by Sex", range_y=[0,100]), use_container_width=True)
with right:
    st.plotly_chart(px.histogram(filtered, x="Age", color="Survived", nbins=20, title="Age Distribution by Survival Outcome"), use_container_width=True)

left, right = st.columns(2)
with left:
    st.plotly_chart(px.histogram(filtered, x="Fare", nbins=30, title="Fare Distribution"), use_container_width=True)
with right:
    by_port = filtered.groupby("Embarked").size().rename("Passengers").reset_index()
    st.plotly_chart(px.bar(by_port, x="Embarked", y="Passengers", color="Embarked", text="Passengers", title="Passengers by Embarkation Port"), use_container_width=True)

st.subheader("Filtered passenger records")
st.write(f"{len(filtered):,} records match the selected filters.")
st.dataframe(filtered, use_container_width=True, hide_index=True)
st.download_button("Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"), "titanic_filtered.csv", "text/csv")
st.subheader("How to interpret the dashboard")
st.markdown("- Use the sidebar filters to compare passenger groups.\n- Compare survival rates across passenger class and sex.\n- Review age and fare distributions for patterns and potential outliers.\n- These are descriptive associations and do not prove causation.")
st.caption("Built with Python, Pandas, Streamlit, and Plotly.")
