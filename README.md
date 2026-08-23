# CGPA Prediction

Probability and Statistics final project that predicts university students’ Final CGPA from academic and lifestyle factors using EDA, multiple linear regression, and a Random Forest regressor.

## Overview

Course project (section E, i222327) covering:

1. Data from a public Kaggle student-performance dataset
2. Summary statistics (mean, median, mode, quartiles)
3. Box plots and scatter grids for exploration / outliers
4. Multiple Linear Regression and Random Forest Regressor
5. Formal LaTeX report and PDF

### Dependent variable

`Final_CGPA`

### Key independent variables

- Study hours per day
- Attendance percentage
- Sleep hours
- Social hours per week
- Previous CGPA

(CSV also includes identifiers / demographics such as gender, age, and major.)

## Dataset

| Item | Detail |
|------|--------|
| File | `Probability_Proj_DataSet/Student_data.csv` |
| Rows | 5,000 students |
| Source | [University Student Performance and Habits (Kaggle)](https://www.kaggle.com/datasets/robiulhasanjisan/university-student-performance-and-habits-dataset) |

## Repository Layout

```
CGPA_Prediction/
├── Python Files/
│   ├── i222327_E_FinalProject_Prob&Stat.ipynb
│   ├── i222327_e_finalproject_prob&stat.py
│   └── i222327_E_FinalProject_Prob&Stat.ipynb - Colab.pdf
├── Probability_Proj_DataSet/
│   ├── Student_data.csv
│   └── Probability_Proj_DataSet.zip
├── Latex_SourceFile/
│   ├── main.tex
│   └── i222327_E_FinalProject_Prob_Stat.zip
├── PDF Document/
│   └── i222327_E_FinalProject_Prob_Stat.pdf
└── Project Description/
    └── Proability &  Statistics Project.pdf
```

## Methods

| Stage | Technique |
|-------|-----------|
| EDA | `describe()`, mode, Seaborn box plots, scatter subplots |
| Model A | `sklearn.linear_model.LinearRegression` |
| Model B | `sklearn.ensemble.RandomForestRegressor` (100 trees) |
| Split | 80% / 20% (`random_state=42`) |
| Metrics | MSE, R² |

## Tech Stack

Python 3 / Jupyter / Colab · pandas · Matplotlib · Seaborn · scikit-learn · LaTeX

## Getting Started

```bash
pip install pandas matplotlib seaborn scikit-learn jupyter
```

```python
df = pd.read_csv("Probability_Proj_DataSet/Student_data.csv")
```

```bash
jupyter notebook "Python Files/i222327_E_FinalProject_Prob&Stat.ipynb"
```

## Author

Mohammad Rohaan — i222327 · [rohaan2802](https://github.com/rohaan2802)
