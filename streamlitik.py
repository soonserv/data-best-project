import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("World Happiness Dashboard")

with st.spinner("Loading data..."):
    all_data = pd.read_csv("data_sets/al.csv")

years_available = sorted(all_data["Year"].unique())

#График 1: Distribution of Generosity by Year
st.subheader("Distribution of Generosity by Year")

selected_year_2 = st.slider(
    "Select year:",
    min_value=min(years_available),
    max_value=max(years_available),
    value=min(years_available),
    key="slider_hist"
)

with st.spinner("Building histogram..."):
    fig, ax = plt.subplots(figsize=(9, 7))
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

st.caption("The histogram shows the distribution of the Generosity indicator across all countries and years included in the dataset. The distribution is right-skewed, with most values concentrated between −0.2 and 0.4, and a long tail extending toward higher values. This suggests that while most countries report relatively low or moderate levels of generosity, a smaller number of countries stand out with noticeably higher scores.")

#График 2: Freedom vs Happiness Score
st.subheader("Freedom vs Happiness Score")

with st.spinner("Building scatter plot..."):
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.scatter(all_data["Freedom"], all_data["Happiness Score"],
               alpha=0.5, color="#98FB98")
    ax.set_title("Freedom vs Happiness Score")
    ax.set_xlabel("Freedom")
    ax.set_ylabel("Happiness Score")
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)

st.caption("The scatter plot reveals a positive relationship between freedom and happiness — countries where people report higher freedom to make life choices tend to score higher on the happiness scale.")

#График 3: Distribution of Social Support
st.subheader("Distribution of Social Support")

selected_year_3 = st.slider(
    "Select year:",
    min_value=min(years_available),
    max_value=max(years_available),
    value=min(years_available),
    key="slider_family"
)

with st.spinner("Building histogram..."):
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.histplot(
        data=all_data[all_data["Year"] == selected_year_3],
        x="Family",
        bins=20,
        kde=True,
        color="#A8DADC",
        ax=ax
    )
    ax.set_xlim(all_data["Family"].min(), all_data["Family"].max())
    ax.set_title(f"Distribution of Social Support — {selected_year_3}")
    ax.set_xlabel("Social Support")
    ax.set_ylabel("Count")
    st.pyplot(fig)
    plt.close(fig)

st.caption("The histogram shows the distribution of the Social Support indicator across all countries and years in the dataset. Most observations are concentrated between 0.8 and 1.3, indicating that moderate to high levels of social support are common among countries. Very low values occur relatively rarely.")

#График 4: Average Happiness Score by Year
st.subheader("Average Happiness Score by Year")

with st.spinner("Building line plot..."):
    mean_happiness = (
        all_data.groupby("Year")["Happiness Score"]
        .mean()
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(9, 7))
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

st.caption("The line plot displays the trend in average Happiness Score from 2015 to 2022. The average score shows a gradual increase from 2015 to 2021, rising from approximately 5.5 to 5.7. A slight decline is observed in 2022, although the overall trend remains positive.")

#Кнопкап
if st.button("💖 I really liked it!"):
    st.balloons()