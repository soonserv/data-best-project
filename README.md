# data-best-project

A data analysis project that explores how socioeconomic factors relate to quality of life and happiness across countries in 2015–2022. Two open datasets, the World Happiness Report and the Quality of Life Index by Country, are cleaned, merged and analysed. Three hypotheses are tested, and the key findings are presented in an interactive Streamlit dashboard.

Team project (2 people), HSE University, Faculty of Computer Science. Grade: X/10.

## Features
- **Data cleaning:** merging eight yearly World Happiness tables, fixing inconsistent year formats (`2015/2`) and non-numeric values, removing unreliable columns, and keeping only countries with complete data for every year
- **Merged dataset:** an inner join on Country and Year gives 440 observations for 55 countries over 8 years with 17 variables
- **Exploratory analysis:** descriptive statistics, distributions, trends over time, regional comparisons, top countries by happiness and quality of life, and a correlation heatmap
- **Hypothesis testing:** three hypotheses about Purchasing Power, Freedom, Safety and Happiness (see below)
- **Feature engineering:** new indicators `Affordability` (Purchasing Power / Cost of Living) and `Health_and_Safety` (mean of Health Care and Safety indices)
- **Interactive dashboard:** a Streamlit app with year sliders for histograms, a scatter plot and a happiness trend line

## Key findings
| Hypothesis | Result |
|---|---|
| The link between Purchasing Power and Happiness is stronger in countries with more Freedom | Supported: correlation rises from 0.56 (low Freedom) to 0.75 (high Freedom) |
| The link between Purchasing Power and Happiness differs by Safety level | Supported: weak or negative in low-Safety countries, strong and positive in medium and high-Safety countries |
| The top 3 factors correlated with Quality of Life are also the top 3 for Happiness | Supported: Pollution (\|r\| = 0.84), Purchasing Power (0.77) and Cost of Living (0.68) lead both lists |

Other observations: Finland was the happiest country every year from 2018 to 2022; happiness is strongly negatively correlated with pollution; Freedom and Trust peaked in 2020–2021 while Generosity hit its lowest point.

## Project structure
| Path | Contents |
|---|---|
| `data_sets/` | Raw World Happiness tables for 2015–2022, the merged table `al.csv`, and the Quality of Life dataset |
| `notebooks/SA_notebook.ipynb` | Main notebook: both datasets, merging, analysis, hypotheses and conclusion |
| `notebooks/Sofia.ipynb` | World Happiness Report: preparation and exploratory analysis |
| `notebooks/Nastya.ipynb` | Quality of Life Index: preparation and exploratory analysis |
| `streamlitik.py` | Streamlit dashboard |

## Data sources
- [World Happiness Report (Kaggle)](https://www.kaggle.com/datasets/hari31416/world-happiness-report/data)
- [Quality of Life Index by Country (Kaggle)](https://www.kaggle.com/datasets/marcelobatalhah/quality-of-life-index-by-country/data)

## Tech stack
Python 3.9+, pandas, NumPy, Matplotlib, seaborn, Jupyter, Streamlit, uv for dependency management, Git/GitHub.

## How to run
```bash
git clone https://github.com/soonserv/data-best-project.git
cd data-best-project
uv sync                      # or: pip install -r requirements.txt
uv run streamlit run streamlitik.py
```
The notebooks can be opened with `uv run jupyter lab`.

## Team
- **Sofia Servetnik** — World Happiness Report: data preparation, cleaning and exploratory analysis; Streamlit dashboard; merged dataset and hypothesis testing
- **Anastasia Ivanova** — Quality of Life Index: data preparation, cleaning and exploratory analysis; merged dataset and hypothesis testing
