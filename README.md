# ds1 — Data Analysis & Projects Collection

This repository collects data-analysis projects and FreeCodeCamp boilerplates. Each project lives under the `Projects/` directory. Below you will find a short summary and quick run instructions for each project so you or others can get started quickly.

---

## Projects

### 1) Airline Analytics Project
Description: A Streamlit dashboard for analyzing airline flight data: pricing, durations, airline comparisons, and seasonal trends.

Quick start:
```
pip install -r "Projects/Airline Analytics Project/requirements.txt"
cd "Projects/Airline Analytics Project"
streamlit run app.py
```

Key files:
- `Projects/Airline Analytics Project/app.py` — Streamlit app entrypoint
- `Projects/Airline Analytics Project/data/Clean_Dataset.csv` — cleaned dataset used by the dashboard
- `Projects/Airline Analytics Project/requirements.txt` — Python requirements

Notes: Uses Pandas, NumPy, Matplotlib/Seaborn/Plotly and Streamlit for interactive visualizations.

---

### 2) Demographic Data Analyzer (boilerplate)
Description: FreeCodeCamp boilerplate for the Demographic Data Analyzer project. Follow the FreeCodeCamp instructions to complete or run.

Quick start:
```
See Projects/boilerplate-demographic-data-analyzer-main/README.md and follow FreeCodeCamp instructions
```

Key files:
- `Projects/boilerplate-demographic-data-analyzer-main/README.md`

---

### 3) Mean-Variance-Standard Deviation Calculator (boilerplate)
Description: FreeCodeCamp boilerplate for computing mean, variance, and standard deviation across data sets.

Quick start:
```
See Projects/boilerplate-mean-variance-standard-deviation-calculator-main/README.md and follow FreeCodeCamp instructions
```

Key files:
- `Projects/boilerplate-mean-variance-standard-deviation-calculator-main/README.md`

---

### 4) Medical Data Visualizer (boilerplate)
Description: FreeCodeCamp boilerplate for visualizing medical datasets (plots, charts, and basic analysis).

Quick start:
```
See Projects/boilerplate-medical-data-visualizer-main/README.md and follow FreeCodeCamp instructions
```

Key files:
- `Projects/boilerplate-medical-data-visualizer-main/README.md`

---

### 5) Page View Time Series Visualizer (boilerplate)
Description: FreeCodeCamp time-series visualizer boilerplate to plot and analyze page views over time.

Quick start:
```
See Projects/boilerplate-page-view-time-series-visualizer-main/README.md and follow FreeCodeCamp instructions
```

Key files:
- `Projects/boilerplate-page-view-time-series-visualizer-main/README.md`

---

### 6) Sea Level Predictor (boilerplate)
Description: FreeCodeCamp boilerplate for predicting sea-level trends and building a simple model.

Quick start:
```
See Projects/boilerplate-sea-level-predictor-main/README.md and follow FreeCodeCamp instructions
```

Key files:
- `Projects/boilerplate-sea-level-predictor-main/README.md`

---

## Repo structure (top-level)
- `Projects/` — All the included projects and boilerplates
- `Learning Modules/` — notebooks and tutorials (freecodecamp/RDP etc.)
- `.idea/` — IDE metadata (you may want to add this to `.gitignore`)
- Other helper files and datasets

---

## Recommended .gitignore (paste into `.gitignore` at repo root)
```
# macOS
.DS_Store

# Python
__pycache__/
*.pyc
env/
venv/
.venv

# IDEs
.idea/
.vscode/

# Data
*.csv
*.sqlite3
```

---

## How to contribute / run locally
- Clone the repo:
```
git clone https://github.com/heetshah15/ds1.git
cd ds1
```
- Pick a project under `Projects/`, open its folder, install dependencies (if present), and run the app or scripts per the project's README above.

---

If you'd like, I can commit this README for you and add the recommended `.gitignore` as a follow-up.
