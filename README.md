# CGPA Prediction

Probability & Statistics **final project** (Section E): predict university **Final CGPA** from study habits and lifestyle using EDA, **multiple linear regression**, and a **Random Forest** regressor, plus a formal **LaTeX** report.

**Author:** Mohammad Rohaan · **Roll:** 22I-2327 · [rohaan2802](https://github.com/rohaan2802)

---

## Table of contents

1. [Research question](#research-question)
2. [Dataset](#dataset)
3. [Tasks (as implemented)](#tasks-as-implemented)
4. [Models and metrics](#models-and-metrics)
5. [LaTeX report](#latex-report)
6. [How to run](#how-to-run)
7. [File layout](#file-layout)
8. [Limitations](#limitations)

---

## Research question

Which academic and personal factors associate with **Final CGPA**, and can a linear model or a tree ensemble predict it on held-out students?

**Dependent variable:** `Final_CGPA`

**Independent variables used in both models:**

- `Study_Hours_Per_Day`
- `Attendance_Pct`
- `Sleep_Hours`
- `Social_Hours_Week`
- `Previous_CGPA`

CSV also has `Student_ID`, `Gender`, `Age`, `Major` (EDA only in the shipped script).

---

## Dataset

| Item | Detail |
|------|--------|
| Local file | `Probability_Proj_DataSet_Student_data.csv` / `Probability_Proj_DataSet/Student_data.csv` |
| Rows | **5,000** |
| Header | `Student_ID,Gender,Age,Major,Attendance_Pct,Study_Hours_Per_Day,Previous_CGPA,Sleep_Hours,Social_Hours_Week,Final_CGPA` |
| Source | [Kaggle — University Student Performance and Habits](https://www.kaggle.com/datasets/robiulhasanjisan/university-student-performance-and-habits-dataset) |

The `.py` export still contains **Google Colab `drive.mount`** and a Drive path. For local runs, replace that block with `pd.read_csv("Probability_Proj_DataSet_Student_data.csv")`.

---

## Tasks (as implemented)

| Task | Implementation |
|------|----------------|
| 1 Collect data | Load CSV; `df.head()` |
| 2 Summary stats | `df.describe()` plus `df.mode().iloc[0]` |
| 3 Box plots | Seaborn `boxplot` on Age, Attendance, Study hours, Previous CGPA, Sleep, Social, Final CGPA; red outlier markers |
| 4 Scatter grid | 2×2: Study, Attendance, Sleep, Social **vs Final CGPA** |
| 5 Two models | MLR + Random Forest; compare MSE / R² |
| Conclusion | Print which model wins on MSE and on R² |

Literature framing in `Latex_SourceFile_main.tex`: study habits, sleep, social time, prior GPA (Smith, Johnson, Zhao, White & Brown citations as used in the write-up).

---

## Models and metrics

```python
X = df[['Study_Hours_Per_Day', 'Attendance_Pct', 'Sleep_Hours',
        'Social_Hours_Week', 'Previous_CGPA']]
y = df['Final_CGPA']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

| Model | sklearn class | Notes |
|-------|---------------|--------|
| A | `LinearRegression` | OLS, five features |
| B | `RandomForestRegressor(n_estimators=100, random_state=42)` | Same split |

Metrics: `mean_squared_error`, `r2_score`. The script prints both and a textual winner.

**Techniques listed in the notebook header:** MLR, cleaning, box/scatter, MSE.

---

## LaTeX report

`Latex_SourceFile_main.tex` — title *Probability and Statistics Project: CGPA Prediction*, author block with name / 22I-2327 / Sec-E. Sections: Introduction, Literature Review, Description of Variables, then methods/results (rest of the zip). Compile with a LaTeX engine; PDF copy lives under `PDF Document/` on GitHub.

---

## How to run

```bash
pip install pandas matplotlib seaborn scikit-learn jupyter
```

```python
import pandas as pd
df = pd.read_csv("Probability_Proj_DataSet_Student_data.csv")
```

```bash
jupyter notebook "Python Files/i222327_E_FinalProject_Prob&Stat.ipynb"
# or
python Python_Files_i222327_e_finalproject_prob&stat.py
```

---

## File layout

```text
CGPA_Prediction/
├── Python Files/  (ipynb, py, Colab PDF)
├── Probability_Proj_DataSet/Student_data.csv
├── Latex_SourceFile/main.tex
├── PDF Document/
└── Project Description/
```

---

## Limitations

- Colab Drive paths in the `.py` dump.  
- Gender/Age/Major not in the regression (could be dummy-encoded as an extension).  
- No residual diagnostics / VIF in the Python file (may appear in the PDF).  
- RF vs OLS: trees can win on nonlinearities; report both MSE and R² as the script does.

---

## Author

**Mohammad Rohaan** — 22I-2327 · Sec-E  
[rohaan2802](https://github.com/rohaan2802)
