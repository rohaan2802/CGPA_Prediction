# CGPA Prediction — Probability and Statistics Final Project (Sec-E)

University **Final CGPA** is modeled from study habits and lifestyle using **exploratory statistics**, a **2×2 scatter grid**, **multiple linear regression**, and a **Random Forest** regressor (100 trees). The report is a **LaTeX** article; the code is a Colab-exported `.py` plus a Jupyter notebook on GitHub. Dataset: **5,000** students from a public Kaggle table.

**Author:** Mohammad Rohaan · **22I-2327** · Section **E** · [rohaan2802](https://github.com/rohaan2802)

There are **no named hypothesis tests** (no t-test, ANOVA, or χ²) in `Python_Files_i222327_e_finalproject_prob&stat.py` or `Latex_SourceFile_main.tex`. Inference in the submitted work is **summary statistics, plots, and test-set MSE / R²**. The project-description PDF (`Proability &  Statistics Project.pdf`) is in the tree; this README follows the **implemented** Python and LaTeX.

## Table of contents

- [Problem statement / academic context](#problem-statement--academic-context)
- [Features](#features)
- [Architecture / design](#architecture--design)
- [Algorithms and data structures](#algorithms-and-data-structures)
- [File-by-file reference](#file-by-file-reference)
- [Data formats / schemas](#data-formats--schemas)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Prerequisites and install](#prerequisites-and-install)
- [How to build and run](#how-to-build-and-run)
- [Usage walkthrough](#usage-walkthrough)
- [Configuration / constants](#configuration--constants)
- [Results / metrics](#results--metrics)
- [Controls / CLI](#controls--cli)
- [Known limitations / bugs](#known-limitations--bugs)
- [How to extend](#how-to-extend)
- [Author](#author)

## Problem statement / academic context

**Research question (as implemented):** which of study hours, attendance, sleep, social time, and previous CGPA associate with **Final CGPA**, and can OLS or a tree ensemble predict held-out students?

LaTeX title: *Probability and Statistics Project: CGPA Prediction*. Literature bullets cite Smith et al. (2018) on study habits, Johnson (2020) on sleep, Zhao et al. (2021) on regression for GPA, White and Brown (2017) on social media — as written in `main.tex`, not re-checked against journals.

**Dependent variable:** `Final_CGPA`  
**Independent variables in both models:** `Study_Hours_Per_Day`, `Attendance_Pct`, `Sleep_Hours`, `Social_Hours_Week`, `Previous_CGPA`  
CSV also has `Student_ID`, `Gender`, `Age`, `Major` (EDA / boxplots for Age; **not** in the regressors).

## Features

Mapped to the Python task headings:

| Task | Spec in the `.py` | Implementation |
|------|-------------------|----------------|
| 01 | Collect dependent CGPA and listed independents from an authentic source | `pd.read_csv` from Google Drive; Kaggle URL in the header |
| 02 | Mean, median, mode, quartiles | `df.describe()` + `df.mode().iloc[0]` |
| 03 | Box-and-whisker plots, identify outliers | One seaborn `boxplot` of seven numeric columns, red flier markers |
| 04 | Scatter plots on one grid; interpret each panel | 2×2: Study, Attendance, Sleep, Social **vs Final_CGPA** (Previous CGPA is **not** on this grid) |
| 05 | ≥ five independents, ≥ 50 observations; two models | n = 5000; MLR + `RandomForestRegressor` |
| Conclusion | Compare predictions with originals using graphs and MSE | Prints MSE/R² twice and if-statements for the winner; **no actual-vs-pred plot** in the `.py` |

Techniques listed in the notebook header: *Multiple Linear Regression, Data Cleaning, Data Visualization (Box Plot, Scatter Plot), Model Evaluation (MSE)*. The script never calls `dropna`/`fillna`; the CSV has **0** missing cells.

## Architecture / design

```
Student_data.csv (5000 × 10)
        │
   describe + mode; boxplots; 2×2 scatters
        │
   X = 5 numeric habits/GPA, y = Final_CGPA
        │
   train_test_split(0.2, random_state=42)  →  4000 / 1000
        │
   LinearRegression ──► MSE, R²
   RandomForestRegressor(100, seed=42) ──► MSE, R²
        │
   print which model has lower MSE / higher R²
```

LaTeX writes the OLS equation

\[
\text{Final CGPA} = \beta_0 + \beta_1(\text{study}) + \beta_2(\text{attendance}) + \beta_3(\text{sleep}) + \beta_4(\text{social}) + \beta_5(\text{previous CGPA})
\]

Coefficients are **not printed** in the Python file (no `coef_` / intercept dump).

## Algorithms and data structures

- **OLS:** sklearn `LinearRegression` (closed-form, intercept on).
- **Random Forest:** `RandomForestRegressor(n_estimators=100, random_state=42)` — default `max_depth=None`, MSE splitting.
- **Metrics:** `mean_squared_error`, `r2_score` on the **same** test split.
- **Plots:** seaborn `whitegrid`; boxplot `figsize=(18, 10)`, `palette="Set2"`, `flierprops` red circles size 12; scatters `figsize=(15, 10)`.

Pearson correlations below are computed from `Probability_Proj_DataSet_Student_data.csv` (the file `describe()` would summarize). They are **not** printed by the `.py`.

## File-by-file reference

| File | Description |
|------|-------------|
| `Python_Files_i222327_e_finalproject_prob&stat.py` | Colab export of the notebook. |
| `Python Files/i222327_E_FinalProject_Prob&Stat.ipynb` | Same project as a notebook (GitHub). |
| `Probability_Proj_DataSet_Student_data.csv` | Local CSV copy (5,000 rows). |
| `Probability_Proj_DataSet/Student_data.csv` | Same table in the zip folder. |
| `Latex_SourceFile_main.tex` / `Latex_SourceFile/main.tex` | Report source. |
| `PDF Document/i222327_E_FinalProject_Prob_Stat.pdf` | Compiled report. |
| `Project Description/Proability &  Statistics Project.pdf` | Course brief (filename typo “Proability”). |

## Data formats / schemas

Header (exact):

```text
Student_ID,Gender,Age,Major,Attendance_Pct,Study_Hours_Per_Day,Previous_CGPA,Sleep_Hours,Social_Hours_Week,Final_CGPA
```

Source stated in code and tex: [Kaggle — University Student Performance and Habits](https://www.kaggle.com/datasets/robiulhasanjisan/university-student-performance-and-habits-dataset).

**Counts:** 5,000 rows, **0** nulls. `Gender`: Male **2748**, Female **2252**. `Major`: Psychology 869, Mathematics 859, Business 843, Economics 835, Engineering 799, Computer Science 795.

**Numeric summary (from the CSV; matches what `df.describe()` reports):**

| Column | Mean | Std | Min | ~Q1 | Median | ~Q3 | Max | Mode (`df.mode`) |
|--------|------|-----|-----|-----|--------|-----|-----|------------------|
| Age | 20.949 | 2.017 | 18 | 19 | 21 | 23 | 24 | 19 |
| Attendance_Pct | 83.796 | 12.868 | 26.2 | 75.1 | 85.1 | 94.8 | 100 | 100 |
| Study_Hours_Per_Day | 4.518 | 2.568 | 0.1 | 2.6 | 4.0 | 6.0 | 14 | 2.9 |
| Previous_CGPA | 3.094 | 0.477 | 1.35 | 2.76 | 3.10 | 3.43 | 4.0 | 4.0 |
| Sleep_Hours | 7.012 | 1.424 | 4.0 | 6.0 | 7.0 | 8.0 | 10 | 7.4 |
| Social_Hours_Week | 8.006 | 2.798 | 0 | 6 | 8 | 10 | 20 | 8 |
| Final_CGPA | 3.272 | 0.508 | 1.16 | 2.92 | 3.31 | 3.68 | 4.0 | 4.0 |

Quartiles above use positional indices (`n//4`) for a compact README; use pandas `describe()` for the exact 25/75 percentiles.

**Pearson r with `Final_CGPA` (CSV):** Previous_CGPA **0.8789**, Attendance_Pct **0.3028**, Study_Hours_Per_Day **0.2309**, Age **−0.0122**, Sleep_Hours **0.0026**, Social_Hours_Week **−0.0049**. Prior GPA dominates; sleep and social time are essentially uncorrelated with the target in this table. That is why a linear model can still reach R² ≈ 0.91 without those two features doing much work.

Sample row 1: `ID00001`, Male, 20, Engineering, attendance 83.9, study 4.4, previous 2.65, sleep 9.1, social 8, final **2.78**.

## Tech stack

- Python 3: pandas, matplotlib, seaborn, scikit-learn
- Google Colab (`google.colab.drive`) in the shipped `.py`
- LaTeX: `article`, `graphicx`, `amsmath`, `url`

## Project structure

```
CGPA_Prediction/
├── Python Files/          # ipynb, .py, Colab PDF
├── Probability_Proj_DataSet/Student_data.csv
├── Latex_SourceFile/main.tex
├── PDF Document/
└── Project Description/
```

Local flattened copies: `Python_Files_i222327_e_finalproject_prob&stat.py`, `Latex_SourceFile_main.tex`, `Probability_Proj_DataSet_Student_data.csv`.

## Prerequisites and install

```bash
pip install pandas matplotlib seaborn scikit-learn jupyter
```

LaTeX: a TeX distribution with `pdflatex` (or Overleaf). Packages: `graphicx`, `amsmath`, `url`.

## How to build and run

**Python (local).** The export still has:

```python
from google.colab import drive
drive.mount('/content/drive')
file_path = '/content/drive/MyDrive/Probability_DataSet/Student_data.csv'
```

Replace that block with:

```python
import pandas as pd
df = pd.read_csv("Probability_Proj_DataSet_Student_data.csv")
# or: Probability_Proj_DataSet/Student_data.csv
```

Then:

```bash
python Python_Files_i222327_e_finalproject_prob&stat.py
# or
jupyter notebook "Python Files/i222327_E_FinalProject_Prob&Stat.ipynb"
```

Run top to bottom so `df`, `mse`/`r2`, and `mse_rf`/`r2_rf` exist before the conclusion cell.

**LaTeX:**

```bash
cd Latex_SourceFile
pdflatex main.tex
pdflatex main.tex
```

`\date{\today}` stamps the compile day. A prebuilt PDF is under `PDF Document/`.

## Usage walkthrough

1. Confirm 5,000 rows and the ten column names.
2. Read `describe()` / mode; Age is 18–24, Final CGPA 1.16–4.00.
3. Boxplots: red fliers mark univariate outliers (especially study hours up to 14 and attendance down to 26.2). The script does **not** print outlier counts.
4. Scatter grid: expect a visible slope for study and attendance vs CGPA; sleep and social panels look like noise (r ≈ 0).
5. Fit both models; copy MSE and R². Conclusion prints Random Forest as winner on both criteria given the LaTeX numbers.
6. Compile the tex and check that the Results section matches the Python printout.

## Configuration / constants

| Item | Value |
|------|-------|
| n | 5000 |
| Features in X | 5 (list above) |
| `test_size` | 0.2 → 1000 test rows |
| `random_state` | 42 (split and RF) |
| RF trees | 100 |
| Boxplot columns | Age, Attendance_Pct, Study_Hours_Per_Day, Previous_CGPA, Sleep_Hours, Social_Hours_Week, Final_CGPA |
| Drive path (Colab) | `/content/drive/MyDrive/Probability_DataSet/Student_data.csv` |

## Results / metrics

**From `Latex_SourceFile_main.tex` (executed Python pasted into the report):**

| Model | MSE | R² |
|-------|-----|-----|
| Multiple linear regression | **0.026013138313700883** | **0.9092883364955272** |
| Random Forest (100 trees) | **0.01634154564** | **0.9430146116411523** |

The tex states RF **outperforms** OLS on both metrics (~91% vs ~94% variance explained) and prefers Random Forest for this dataset. The `.py` conclusion uses:

```python
if mse < mse_rf:  # Linear better on MSE
    ...
else:
    print("The Random Forest model performed better with a lower Mean Squared Error (MSE).")
```

With the LaTeX numbers, the `else` branch runs, and RF also wins the R² comparison.

RMSE is not printed; \(\sqrt{0.026013}\approx 0.161\) CGPA points (OLS) and \(\sqrt{0.016342}\approx 0.128\) (RF) on the 0–4 scale.

The script does **not** print feature importances or \(\beta\) values, so “which factor contributes most” in the Introduction is answered only indirectly by the CSV correlations (Previous_CGPA).

## Controls / CLI

No argparse. Colab Drive mount is the only environment hook.

## Known limitations / bugs

- **Colab-only I/O** until the `read_csv` path is changed.
- Gender, Age, Major omitted from X (Age is plotted but not modeled).
- Task 04 never scatters **Previous_CGPA vs Final_CGPA** (the strongest linear relationship).
- Conclusion text promises graphs of predicted vs original; the `.py` has **prints only**.
- No VIF, residual plots, or formal tests despite a probability/statistics course frame.
- RF can overfit; there is no extra validation split.
- Literature citations are not verified here.
- Header lists “Data Cleaning” but the CSV is already complete.

## How to extend

- Dummy-encode `Major`/`Gender`; add Previous_CGPA to the scatter grid.
- `statsmodels.OLS` for coefficient tables, t-stats, and residual diagnostics (if the brief required tests).
- Plot `y_test` vs `y_pred` / `y_pred_rf`.
- Print `linear_model.coef_` and `rf_model.feature_importances_`.

## Author

**Mohammad Rohaan** — 22I-2327 · Sec-E · [rohaan2802](https://github.com/rohaan2802)
