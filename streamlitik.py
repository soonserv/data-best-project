import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("World Happiness Dashboard")

with st.spinner("Loading data..."):
    all_data = pd.read_csv("data_sets/al.csv")

years_available = sorted(all_data["Year"].unique())

# ---------- График 1: Distribution of Generosity by Year ----------
st.subheader("Distribution of Generosity by Year")

selected_year_2 = st.slider(
    "Select year:",
    min_value=min(years_available),
    max_value=max(years_available),
    value=min(years_available),
    key="slider_hist"
)

with st.spinner("Building histogram..."):
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.histplot(
        data=all_data[all_data["Year"] == selected_year_2],
        x="Generosity",
        bins=20,
        kde=True,
        color="#FF69B4",
        ax=ax
    )
    ax.set_xlim(all_data["Generosity"].min(), all_data["Generosity"].max())
    ax.set_title(f"Distribution of Generosity — {selected_year_2}")
    ax.set_xlabel("Generosity")
    ax.set_ylabel("Amount of countries")

    st.pyplot(fig)
    plt.close(fig)

# ---------- График 2: Average Happiness Score by Year ----------
st.subheader("Average Happiness Score by Year")

with st.spinner("Building line plot..."):
    mean_happiness = (
        all_data.groupby("Year")["Happiness Score"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.lineplot(
        data=mean_happiness,
        x="Year",
        y="Happiness Score",
        color="#FF69B4",
        marker="o",
        ax=ax
    )

    ax.set_title("Average Happiness Score by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Average Happiness Score")

    st.pyplot(fig)
    plt.close(fig)

# ---------- Финал ----------
if st.button("💖 I really liked it!"):
    st.balloons()