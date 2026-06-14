import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Quality of Life & Happiness", layout="wide")
st.title("Quality of Life and Happiness Analysis")

# ────────────────────────────────────────────
# LOAD DATA
# ────────────────────────────────────────────
@st.cache_data
def load_data():
    all_data = pd.read_csv("data_sets/al.csv")
    clean_data = pd.read_csv("data_sets/quality_of_life_indices_by_country.csv")

    # QoL cleanup
    clean_data = clean_data.drop(columns=["Climate Index"], errors="ignore")
    clean_data["Year"] = clean_data["Year"].astype(str).str.replace("/2", "", regex=False)
    clean_data["Year"] = clean_data["Year"].astype(int)
    clean_data = clean_data.groupby(["Country", "Year"], as_index=False).mean()
    clean_data = clean_data.drop(columns=["Rank"], errors="ignore")
    good2 = clean_data.groupby("Country")["Year"].nunique()
    clean_data = clean_data[clean_data["Country"].isin(good2[good2 == 10].index)]

    # Merge
    final_data = pd.merge(clean_data, all_data, on=["Country", "Year"], how="inner")
    final_data = final_data.drop(columns=["Happiness Rank"], errors="ignore")

    # Transformations
    final_data["Affordability"] = final_data["Purchasing Power Index"] / final_data["Cost of Living Index"]
    final_data["Health_and_Safety"] = (final_data["Health Care Index"] + final_data["Safety Index"]) / 2
    final_data["Freedom Level"] = pd.cut(final_data["Freedom"], bins=3,
                                          labels=["Low Freedom", "Medium Freedom", "High Freedom"])
    final_data["Safety Level"] = pd.cut(final_data["Safety Index"], bins=3,
                                         labels=["Low Safety", "Medium Safety", "High Safety"])
    return all_data, clean_data, final_data

all_data, clean_data, final_data = load_data()
years_available = sorted(all_data["Year"].unique())

# ────────────────────────────────────────────
# ABSTRACT
# ────────────────────────────────────────────
st.header("Abstract")
st.write("""
This project investigates how external socioeconomic factors are associated with Quality of Life
and Happiness Score across different countries over the period from 2015 to 2022. Two datasets were
merged — the World Happiness Report and the Quality of Life Index by Country — to enable a
comprehensive cross-analysis of indicators such as Social Support, Freedom, Generosity, Trust in
Government, Purchasing Power, Safety, and Pollution. The analysis includes descriptive statistics,
trend visualization, correlation analysis, and hypothesis testing aimed at identifying which factors
most strongly drive well-being at a national level.

The project was completed by a team of two. Visualizations and descriptive analysis of the World
Happiness dataset were handled primarily by Sofia, while analysis of the Quality of Life dataset was
handled primarily by Anastasia. The merged dataset analysis, cleanup, hypothesis formulation and
hypothesis testing were completed collaboratively by both team members.
""")

# ────────────────────────────────────────────
# 1. WORLD HAPPINESS DATASET
# ────────────────────────────────────────────
st.header("1. World Happiness Dataset")

st.subheader("Dataset Description")
st.write("""
The datasets belong to the field of social and economic statistics. They contain annual data for
multiple countries from 2015 to 2022 and include indicators such as economic conditions (GDP per capita),
social support (Family), healthy life expectancy (Health), freedom to make life choices (Freedom),
generosity, trust in institutions, and overall happiness scores.
""")

st.subheader("Descriptive Statistics")
stats_h = pd.DataFrame({
    "Mean": [all_data[c].mean() for c in ["Happiness Score", "Family", "Freedom", "Generosity", "Trust"]],
    "Median": [all_data[c].median() for c in ["Happiness Score", "Family", "Freedom", "Generosity", "Trust"]],
    "Std": [all_data[c].std() for c in ["Happiness Score", "Family", "Freedom", "Generosity", "Trust"]],
    "Min": [all_data[c].min() for c in ["Happiness Score", "Family", "Freedom", "Generosity", "Trust"]],
    "Max": [all_data[c].max() for c in ["Happiness Score", "Family", "Freedom", "Generosity", "Trust"]],
}, index=["Happiness Score", "Family (Social Support)", "Freedom", "Generosity", "Trust in Government"])
st.dataframe(stats_h.round(3))
st.write("""
The descriptive statistics provide a general overview of the dataset. Most indicators have reasonable
ranges and average values that correspond to the expected scale of the World Happiness Report data.
""")

st.subheader("Plots — World Happiness")

# Plot 1: Generosity histogram with year slider
st.markdown("**Distribution of Generosity**")
selected_year = st.slider("Select year:", min_value=min(years_available),
                           max_value=max(years_available), value=min(years_available))
fig, ax = plt.subplots(figsize=(9, 5))
sns.histplot(data=all_data[all_data["Year"] == selected_year],
             x="Generosity", bins=20, kde=True, color="#FF69B4", ax=ax)
ax.set_xlim(all_data["Generosity"].min(), all_data["Generosity"].max())
ax.set_title(f"Distribution of Generosity — {selected_year}")
ax.set_xlabel("Generosity")
ax.set_ylabel("Count")
st.pyplot(fig); plt.close(fig)
st.write("The distribution is right-skewed, with most values concentrated between -0.2 and 0.4.")

# Plot 2: Freedom vs Happiness scatter
st.markdown("**Freedom vs Happiness Score**")
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(all_data["Freedom"], all_data["Happiness Score"], alpha=0.5, color="#98FB98")
ax.set_title("Freedom vs Happiness Score")
ax.set_xlabel("Freedom")
ax.set_ylabel("Happiness Score")
ax.grid(alpha=0.3)
st.pyplot(fig); plt.close(fig)
st.write("The scatter plot reveals a positive relationship between freedom and happiness.")

# Plot 3: Social Support histogram
st.markdown("**Distribution of Social Support**")
fig, ax = plt.subplots(figsize=(9, 5))
sns.histplot(data=all_data, x="Family", bins=20, kde=True, color="#A8DADC", ax=ax)
ax.set_title("Distribution of Social Support")
ax.set_xlabel("Social Support")
ax.set_ylabel("Count")
st.pyplot(fig); plt.close(fig)
st.write("Most observations are concentrated between 0.8 and 1.3, indicating moderate to high social support.")

# Plot 4: Average Happiness Score by Year (line)
st.markdown("**Average Happiness Score by Year**")
mean_happiness = all_data.groupby("Year")["Happiness Score"].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(data=mean_happiness, x="Year", y="Happiness Score",
             color="#FF69B4", marker="o", linewidth=3, ax=ax)
ax.set_title("Average Happiness Score by Year")
st.pyplot(fig); plt.close(fig)
st.write("The average score shows a gradual increase from 2015 to 2021, with a slight decline in 2022.")

# ────────────────────────────────────────────
# 2. QUALITY OF LIFE DATASET
# ────────────────────────────────────────────
st.header("2. Quality of Life Dataset")

st.subheader("Dataset Description")
st.write("""
The dataset belongs to the socio-economic domain and contains quality of life indicators for different
countries between 2015 and 2024. It includes the overall Quality of Life Index, Purchasing Power Index,
Safety Index, Health Care Index, Cost of Living Index, Property Price to Income Ratio,
Traffic Commute Time Index, Pollution Index, and Climate Index.
""")

st.subheader("Descriptive Statistics")
qol_cols = ["Quality of Life Index", "Purchasing Power Index", "Safety Index",
            "Health Care Index", "Cost of Living Index"]
stats_q = pd.DataFrame({
    "Mean": [clean_data[c].mean() for c in qol_cols],
    "Median": [clean_data[c].median() for c in qol_cols],
    "Std": [clean_data[c].std() for c in qol_cols],
    "Min": [clean_data[c].min() for c in qol_cols],
    "Max": [clean_data[c].max() for c in qol_cols],
}, index=qol_cols)
st.dataframe(stats_q.round(2))
st.write("The Quality of Life Index has the highest variability, while the Health Care Index shows the lowest.")

st.subheader("Plots — Quality of Life")

# Plot 1: QoL histogram
st.markdown("**Distribution of Quality of Life Index**")
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(clean_data["Quality of Life Index"], bins=20, edgecolor="black")
ax.set_title("Distribution of Quality of Life Index")
ax.set_xlabel("Quality of Life Index")
ax.set_ylabel("Frequency")
ax.grid(axis="y", linestyle="--")
st.pyplot(fig); plt.close(fig)
st.write("Most values fall between 90 and 190 points; extremely low and high values are rare.")

# Plot 2: QoL boxplot by year
st.markdown("**Quality of Life Index by Year**")
fig, ax = plt.subplots(figsize=(9, 5))
clean_data.boxplot(column="Quality of Life Index", by="Year", ax=ax)
plt.suptitle("")
ax.set_title("Quality of Life Index by Year")
ax.set_xlabel("Year")
ax.set_ylabel("Quality of Life Index")
st.pyplot(fig); plt.close(fig)
st.write("The median Quality of Life Index remains relatively stable between 2015 and 2024.")

# Plot 3: Purchasing Power Index scatter vs Safety Index
st.markdown("**Purchasing Power Index vs Safety Index**")
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(clean_data["Safety Index"], clean_data["Purchasing Power Index"],
           alpha=0.5, color="#87CEFA")
ax.set_title("Safety Index vs Purchasing Power Index")
ax.set_xlabel("Safety Index")
ax.set_ylabel("Purchasing Power Index")
ax.grid(alpha=0.3)
st.pyplot(fig); plt.close(fig)
st.write("Countries with higher safety levels tend to show a wider spread in purchasing power.")

# ────────────────────────────────────────────
# 3. MERGED DATASET
# ────────────────────────────────────────────
st.header("3. Merged Dataset")
st.write(f"""
The two datasets were merged using an inner join on Country and Year.
The final dataset contains **{final_data.shape[0]} observations** and **{final_data.shape[1]} variables**,
covering 2015–2022 with 55 countries.
""")

st.subheader("Detailed Overview")

# Overview 1: Median Happiness by Region
st.markdown("**Median Happiness Score by Region**")
region_happiness = all_data.groupby("Region")["Happiness Score"].median().sort_values()
fig, ax = plt.subplots(figsize=(9, 6))
region_happiness.plot(kind="barh", color="#FFB6C1", ax=ax)
ax.set_title("Median Happiness Score by Region")
ax.set_xlabel("Median Happiness Score")
ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
st.pyplot(fig); plt.close(fig)
st.write("Australia, New Zealand, North America and Western Europe rank highest. South Asia and Sub-Saharan Africa rank lowest.")

# Overview 2: Freedom, Generosity, Trust trends
st.markdown("**Average Freedom, Generosity and Trust by Year**")
trend = all_data.groupby("Year")[["Freedom", "Generosity", "Trust"]].mean().reset_index()
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(trend["Year"], trend["Freedom"], marker="o", label="Freedom", color="#87CEFA")
ax.plot(trend["Year"], trend["Generosity"], marker="s", label="Generosity", color="#FF69B4")
ax.plot(trend["Year"], trend["Trust"], marker="^", label="Trust in Government", color="#98FB98")
ax.set_title("Average Freedom, Generosity and Trust by Year")
ax.set_xlabel("Year"); ax.set_ylabel("Average Value")
ax.legend(); ax.grid(alpha=0.3)
st.pyplot(fig); plt.close(fig)
st.write("Freedom and Trust increase in 2020–2021, while Generosity drops to its lowest level in the same period.")

# Overview 3: Top-10 comparison 2015 vs 2022
st.markdown("**Top-10 Happiest Countries: 2015 vs 2022**")
data_first = final_data[final_data["Year"] == 2015]
data_last = final_data[final_data["Year"] == 2022]
top_first = data_first.nlargest(10, "Happiness Score")[["Country", "Happiness Score"]]
top_last = data_last.nlargest(10, "Happiness Score")[["Country", "Happiness Score"]]
first_countries = set(top_first["Country"]); last_countries = set(top_last["Country"])
colors_first = ["green" if c in last_countries else "skyblue" for c in top_first["Country"]]
colors_last = ["green" if c in first_countries else "pink" for c in top_last["Country"]]
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
axes[0].barh(top_first["Country"], top_first["Happiness Score"], color=colors_first)
axes[0].invert_yaxis()
axes[0].set_title("Top-10 by Happiness (2015)\nGreen = also in top-10 in 2022")
axes[0].set_xlabel("Happiness Score")
axes[1].barh(top_last["Country"], top_last["Happiness Score"], color=colors_last)
axes[1].invert_yaxis()
axes[1].set_title("Top-10 by Happiness (2022)\nGreen = also in top-10 in 2015")
axes[1].set_xlabel("Happiness Score")
plt.suptitle("Comparison: Top-10 Happiest Countries, 2015 vs 2022", fontsize=14)
plt.tight_layout()
st.pyplot(fig); plt.close(fig)
st.write("The composition of the top 10 remained highly stable — most countries appear in both rankings.")

# Overview 4: High vs Low Happiness comparison
st.markdown("**High vs Low Happiness Countries — Key Indicators**")
median_h = final_data["Happiness Score"].median()
high = final_data[final_data["Happiness Score"] >= median_h]
low = final_data[final_data["Happiness Score"] < median_h]
comparison = pd.DataFrame({
    "High Happiness": [high[c].mean() for c in ["Quality of Life Index", "Purchasing Power Index", "Safety Index", "Pollution Index"]],
    "Low Happiness": [low[c].mean() for c in ["Quality of Life Index", "Purchasing Power Index", "Safety Index", "Pollution Index"]],
}, index=["Quality of Life", "Purchasing Power", "Safety", "Pollution"]).round(2)
st.dataframe(comparison)
fig, ax = plt.subplots(figsize=(9, 5))
comparison.plot(kind="bar", ax=ax)
ax.set_title("High vs Low Happiness Countries")
ax.set_xlabel("Indicator"); ax.set_ylabel("Mean Value")
ax.tick_params(axis="x", rotation=0)
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig); plt.close(fig)
st.write("Countries with higher happiness have higher Quality of Life, greater Purchasing Power and lower Pollution.")

# Overview 5: Correlation Heatmap
st.markdown("**Correlation Heatmap**")
corr_cols = ["Happiness Score", "Family", "Freedom", "Generosity",
             "Quality of Life Index", "Purchasing Power Index", "Safety Index",
             "Health Care Index", "Cost of Living Index",
             "Property Price to Income Ratio", "Traffic Commute Time Index", "Pollution Index"]
correlation = final_data[corr_cols].corr()
fig, ax = plt.subplots(figsize=(11, 8))
sns.heatmap(correlation, annot=True, cmap="Blues", fmt=".2f", ax=ax)
ax.set_title("Correlation Heatmap")
plt.tight_layout()
st.pyplot(fig); plt.close(fig)
st.write("Happiness Score is positively correlated with Quality of Life and Purchasing Power, and negatively with Pollution.")

# ────────────────────────────────────────────
# DATA TRANSFORMATION
# ────────────────────────────────────────────
st.header("Data Transformation")
st.write("""
Two new columns were added to the merged dataset:
- **Affordability** = Purchasing Power Index / Cost of Living Index. Higher values mean residents can afford everyday life more easily.
- **Health_and_Safety** = average of Health Care Index and Safety Index. Combines healthcare quality and public safety into one indicator.
""")
st.dataframe(final_data[["Country", "Year", "Affordability", "Health_and_Safety"]].head(10).round(2))

# ────────────────────────────────────────────
# HYPOTHESIS CHECK
# ────────────────────────────────────────────
st.header("Hypothesis Check")

# --- Hypothesis 1 ---
st.subheader("Hypothesis 1")
st.write("**The correlation between Purchasing Power Index and Happiness Score is stronger in countries with higher levels of Freedom.**")
st.write("""
This hypothesis was motivated by the heatmap, which showed that both Freedom and Purchasing Power Index
are positively correlated with Happiness Score. This raised the question of whether Freedom acts as a
moderating factor — whether the strength of the link between purchasing power and happiness depends on
how free people feel in a given country.
""")

levels = ["Low Freedom", "Medium Freedom", "High Freedom"]
colors = ["#87CEFA", "#FF69B4", "#98FB98"]
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for ax, level, color in zip(axes, levels, colors):
    subset = final_data[final_data["Freedom Level"] == level]
    r = subset["Purchasing Power Index"].corr(subset["Happiness Score"])
    ax.scatter(subset["Purchasing Power Index"], subset["Happiness Score"],
               alpha=0.6, color=color, s=40)
    m, b = np.polyfit(subset["Purchasing Power Index"], subset["Happiness Score"], 1)
    x_s = sorted(subset["Purchasing Power Index"])
    ax.plot(x_s, [m*x + b for x in x_s], color="black", linewidth=1.5)
    ax.set_title(f"{level}\nr = {r:.2f}", fontsize=11)
    ax.set_xlabel("Purchasing Power Index"); ax.set_ylabel("Happiness Score")
    ax.grid(alpha=0.3)
plt.suptitle("Hypothesis 1: Correlation between Purchasing Power and Happiness by Freedom Level",
             fontsize=13, fontweight="bold")
plt.tight_layout()
st.pyplot(fig); plt.close(fig)
st.write("""
The results confirm the hypothesis. The correlation increases from r = 0.56 (Low Freedom)
to r = 0.64 (Medium Freedom) to r = 0.75 (High Freedom), indicating that in countries where people
have greater freedom, economic prosperity is more strongly linked to happiness.
""")

# --- Hypothesis 2 ---
st.subheader("Hypothesis 2")
st.write("**The relationship between Purchasing Power Index and Happiness Score differs across countries with different Safety levels, and this difference became more pronounced in the second half of the study period (2019–2022) compared to the first half (2015–2018).**")
st.write("""
This hypothesis was motivated by the observation that Safety Index is one of the most distinct
indicators between high- and low-happiness countries. Combined with Hypothesis 1, this raised the
question of whether Safety similarly moderates the link between purchasing power and happiness —
and whether this pattern remained stable over time.
""")

early = final_data[final_data["Year"] <= 2018]
late = final_data[final_data["Year"] > 2018]
safety_levels = ["Low Safety", "Medium Safety", "High Safety"]
safety_colors = ["#FFB347", "#C39BD3", "#76D7C4"]
periods = [("2015–2018", early), ("2019–2022", late)]

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
for row, (period_label, period_data) in enumerate(periods):
    for col, (level, color) in enumerate(zip(safety_levels, safety_colors)):
        ax = axes[row][col]
        subset = period_data[period_data["Safety Level"] == level]
        ax.scatter(subset["Purchasing Power Index"], subset["Happiness Score"],
                   alpha=0.6, color=color, s=40)
        if len(subset) > 2:
            m, b = np.polyfit(subset["Purchasing Power Index"], subset["Happiness Score"], 1)
            x_s = sorted(subset["Purchasing Power Index"])
            ax.plot(x_s, [m*x + b for x in x_s], color="black", linewidth=1.5)
            r = subset["Purchasing Power Index"].corr(subset["Happiness Score"])
            ax.set_title(f"{level}\n{period_label}  |  r = {r:.2f}", fontsize=11)
        ax.set_xlabel("Purchasing Power Index"); ax.set_ylabel("Happiness Score")
        ax.grid(alpha=0.3)
plt.suptitle("Hypothesis 2: Purchasing Power vs Happiness by Safety Level and Time Period",
             fontsize=13, fontweight="bold")
plt.tight_layout()
st.pyplot(fig); plt.close(fig)
st.write("""
The results partially confirm the hypothesis. In Medium and High Safety countries, the positive
correlation is stable across both periods (r ≈ 0.63–0.76). The most notable change is in
Low Safety countries, where the negative correlation strengthened from r = −0.32 to r = −0.89
in 2019–2022, suggesting the disconnect between purchasing power and happiness intensified.
However, the Low Safety group is small (n = 16–21), so this result should be interpreted with caution.
""")

# --- Hypothesis 3 ---
st.subheader("Hypothesis 3")
st.write("**The three factors most strongly correlated with the Quality of Life Index are also the three factors most strongly correlated with the Happiness Score.**")
st.write("""
This hypothesis was motivated by the fact that both Quality of Life Index and Happiness Score measure
well-being, and the heatmap showed several indicators correlating with both targets simultaneously.
""")

cols = ["Family", "Freedom", "Generosity", "Purchasing Power Index", "Safety Index",
        "Health Care Index", "Cost of Living Index", "Property Price to Income Ratio",
        "Traffic Commute Time Index", "Pollution Index"]
corr_qol = final_data[cols + ["Quality of Life Index"]].corr()["Quality of Life Index"].drop("Quality of Life Index").abs().sort_values(ascending=False)
corr_hap = final_data[cols + ["Happiness Score"]].corr()["Happiness Score"].drop("Happiness Score").abs().sort_values(ascending=False)
top3_qol = list(corr_qol.head(3).index)
top3_hap = list(corr_hap.head(3).index)
overlap = set(top3_qol) & set(top3_hap)

st.write(f"Top-3 correlated with Quality of Life Index: **{top3_qol}**")
st.write(f"Top-3 correlated with Happiness Score: **{top3_hap}**")
st.write(f"Overlap: **{overlap}**")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
bars0 = axes[0].bar(corr_qol.head(5).index, corr_qol.head(5).values,
                    color=["#E74C3C" if f in overlap else "#F1948A" for f in corr_qol.head(5).index])
axes[0].set_title("Top-5 Factors Correlated\nwith Quality of Life Index")
axes[0].set_ylabel("Absolute Correlation")
axes[0].tick_params(axis="x", rotation=45)
axes[0].set_ylim(0, 1)
for bar, val in zip(bars0, corr_qol.head(5).values):
    axes[0].text(bar.get_x() + bar.get_width()/2, val + 0.01, f"{val:.2f}", ha="center", fontsize=9)

bars1 = axes[1].bar(corr_hap.head(5).index, corr_hap.head(5).values,
                    color=["#8E44AD" if f in overlap else "#C39BD3" for f in corr_hap.head(5).index])
axes[1].set_title("Top-5 Factors Correlated\nwith Happiness Score")
axes[1].set_ylabel("Absolute Correlation")
axes[1].tick_params(axis="x", rotation=45)
axes[1].set_ylim(0, 1)
for bar, val in zip(bars1, corr_hap.head(5).values):
    axes[1].text(bar.get_x() + bar.get_width()/2, val + 0.01, f"{val:.2f}", ha="center", fontsize=9)

plt.suptitle("Hypothesis 3: Do the same factors drive Quality of Life and Happiness?\n(darker = appears in top-3 of both)",
             fontsize=13, fontweight="bold")
plt.tight_layout()
st.pyplot(fig); plt.close(fig)
st.write("""
The hypothesis is confirmed. All three top factors for Quality of Life Index (Pollution Index,
Purchasing Power Index, Cost of Living Index) also appear in the top-3 for Happiness Score,
giving a full overlap. The ranking differs — for Happiness Score, Cost of Living Index ranks first,
while for Quality of Life Index, Pollution Index leads.
""")
