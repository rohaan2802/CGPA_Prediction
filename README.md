<div align="center">

# CGPA Prediction — Study Habits and Prior Grades

**Two models that predict a student's final CGPA from study hours, attendance, sleep, social hours, and previous CGPA.**

[![Python](https://img.shields.io/badge/Python-3-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://github.com/rohaan2802/CGPA_Prediction)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-LinearRegression%20%2B%20RandomForest-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://github.com/rohaan2802/CGPA_Prediction)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://github.com/rohaan2802/CGPA_Prediction)
[![Repo Size](https://img.shields.io/github/repo-size/rohaan2802/CGPA_Prediction?style=for-the-badge)](https://github.com/rohaan2802/CGPA_Prediction)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Mohammad Rohaan** · 22I-2327

</div>

---

## Live Links

| What | Link |
|------|------|
| Repository | [https://github.com/rohaan2802/CGPA_Prediction](https://github.com/rohaan2802/CGPA_Prediction) |
| Website | [https://rohaan2802.github.io/CGPA_Prediction/](https://rohaan2802.github.io/CGPA_Prediction/) |
| Download ZIP | [https://github.com/rohaan2802/CGPA_Prediction/archive/refs/heads/main.zip](https://github.com/rohaan2802/CGPA_Prediction/archive/refs/heads/main.zip) |

---

## Table of Contents

1. [Live Links](#live-links)
2. [Overview](#overview)
3. [What's Inside](#whats-inside)
4. [The Data](#the-data)
5. [How the Models Are Fitted](#how-the-models-are-fitted)
6. [Test Results](#test-results)
7. [Learned Equation](#learned-equation)
8. [What the Residuals Show](#what-the-residuals-show)
9. [Training and Test Files](#training-and-test-files)
10. [Folder Structure](#folder-structure)
11. [How to Use This Repository](#how-to-use-this-repository)
12. [Running the Fit](#running-the-fit)
13. [Screenshots](#screenshots)
14. [License](#license)
15. [Author](#author)

---

## Overview

This is a Probability & Statistics project. I wanted to see how well I could predict a student's final CGPA from a short list of academic and lifestyle numbers: study hours per day, attendance, sleep, social hours in the week, and the CGPA they already had.

The table is a public Kaggle set — 5,000 university students, ten columns, no missing cells. Gender, age and major are in the file as well, and I summarised them, but they are not inputs to either model. The five predictors above, and `Final_CGPA` as the target, are what both fits use.

I ran two models on the same 4,000 / 1,000 split (`test_size=0.2`, `random_state=42`):

- Multiple linear regression, through `sklearn.linear_model.LinearRegression` (ordinary least squares, intercept on, no scaling).
- A random forest, through `sklearn.ensemble.RandomForestRegressor` with 100 trees and `random_state=42`.

I re-ran the work from [src/predict_cgpa.py](src/predict_cgpa.py). Linear regression came back with exactly the numbers the original notebook printed: test MSE 0.02601314 and R² 0.90928834. The forest is ahead of that — MSE 0.01632421, R² 0.94307506 — close to the notebook's 0.01634155 and 0.94301461. I take the small gap as a scikit-learn version difference; the story is the same either way. Previous CGPA does most of the work (Pearson correlation 0.8789 with the target, and a linear coefficient of 0.9262). Sleep and social hours barely move the needle.

The raw numbers from that run are under [results/](results/). The written report I submitted, and its LaTeX source, are under [docs/](docs/).

---

## What's Inside

| Section | Path | What's there |
|---------|------|----------------|
| Notebook | [notebooks/cgpa_prediction.ipynb](notebooks/cgpa_prediction.ipynb) | The cleaned walkthrough: load the table, print statistics, correlations and outliers, fit both models, print the metrics and the equation, and plot the charts |
| Script | [src/predict_cgpa.py](src/predict_cgpa.py) | The same two fits, runnable from the command line. It prints the report and writes the files under `results/` |
| Data | [data/Student_data.csv](data/Student_data.csv) | The 5,000-row table, included in the repository. Source notes are in [data/README.md](data/README.md) |
| Results | [results/](results/) | `metrics.csv`, `coefficients.csv`, `feature_importances.csv`, `predictions_head.csv`, the other tables, and the figures |
| Report | [docs/report/CGPA_Prediction_Report.pdf](docs/report/CGPA_Prediction_Report.pdf) | The written report (LaTeX source in [docs/latex/main.tex](docs/latex/main.tex)) |
| Screenshots | [screenshots/](screenshots/) | 24 images, all 1600×1000, covering the data, the fits, the charts and the website |
| Website | [index.html](index.html) | The GitHub Pages site for this repo (charcoal and mandarin, dark and light) |
| Dependencies | [requirements.txt](requirements.txt) | pandas, numpy, matplotlib, seaborn, scikit-learn |

---

## The Data

`Student_data.csv` has 5,000 rows and 10 columns. Every cell is filled, and every `Student_ID` is unique. I took the file from the original project folder; the notebook and the report both name this Kaggle source:

https://www.kaggle.com/datasets/robiulhasanjisan/university-student-performance-and-habits-dataset

| Column | Role | What I actually saw |
|--------|------|---------------------|
| `Student_ID` | Identifier | 5,000 distinct values, `ID00001` through `ID05000` |
| `Gender` | Collected, not used in the models | Male 2,748; Female 2,252 |
| `Age` | Collected, not used in the models | Integers 18–24, mean 20.95 |
| `Major` | Collected, not used in the models | Six majors; Psychology is the most common (869), then Mathematics (859), Business (843), Economics (835), Engineering (799), Computer Science (795) |
| `Attendance_Pct` | Predictor | 26.2 to 100, mean 83.80. Mode is 100 (779 students) |
| `Study_Hours_Per_Day` | Predictor | 0.1 to 14, mean 4.52 |
| `Previous_CGPA` | Predictor | 1.35 to 4.00, mean 3.09 |
| `Sleep_Hours` | Predictor | 4.0 to 10.0, mean 7.01 |
| `Social_Hours_Week` | Predictor | 0 to 20, mean 8.01. Mode is 8 (722 students) |
| `Final_CGPA` | Target | 1.16 to 4.00, mean 3.27. Mode is 4.00 (510 students) |

Summary of the numeric columns (rounded):

| Column | Mean | Std | Min | Q1 | Median | Q3 | Max | Mode (count) |
|--------|-----:|----:|----:|---:|-------:|---:|----:|-------------:|
| Age | 20.9486 | 2.0174 | 18 | 19 | 21 | 23 | 24 | 19 (765) |
| Attendance_Pct | 83.7957 | 12.8679 | 26.2 | 75.1 | 85.05 | 94.8 | 100 | 100 (779) |
| Study_Hours_Per_Day | 4.5178 | 2.5681 | 0.1 | 2.6 | 4.0 | 6.0 | 14 | 2.9 (108) |
| Previous_CGPA | 3.0938 | 0.4768 | 1.35 | 2.76 | 3.10 | 3.43 | 4.00 | 4.00 (172) |
| Sleep_Hours | 7.0121 | 1.4244 | 4.0 | 6.0 | 7.0 | 8.0 | 10.0 | 7.4 (153) |
| Social_Hours_Week | 8.0064 | 2.7978 | 0 | 6 | 8 | 10 | 20 | 8 (722) |
| Final_CGPA | 3.2722 | 0.5080 | 1.16 | 2.92 | 3.31 | 3.68 | 4.00 | 4.00 (510) |

Pearson correlations with `Final_CGPA`:

| Column | corr(Final_CGPA) |
|--------|-----------------:|
| Previous_CGPA | **0.8789** |
| Attendance_Pct | 0.3028 |
| Study_Hours_Per_Day | 0.2309 |
| Sleep_Hours | 0.0026 |
| Social_Hours_Week | −0.0049 |
| Age | −0.0122 |

Previous CGPA is in a league of its own. Attendance and study hours are moderate. Sleep, social hours and age are essentially uncorrelated with the target — I still left sleep and social hours in the models, because that is how the original notebook was written, but I would not read a lifestyle story into those two coefficients.

Tukey IQR outliers (1.5 × IQR fences), which I counted and then left in, the same as the original notebook:

| Column | Outliers | Share |
|--------|--------:|------:|
| Age | 0 | 0% |
| Attendance_Pct | 24 | 0.48% |
| Study_Hours_Per_Day | 97 | 1.94% |
| Previous_CGPA | 11 | 0.22% |
| Sleep_Hours | 0 | 0% |
| Social_Hours_Week | 21 | 0.42% |
| Final_CGPA | 17 | 0.34% |

The study-hours tail is the largest: anything above 11.1 hours is flagged, up to a recorded 14.

---

## How the Models Are Fitted

The work is in [src/predict_cgpa.py](src/predict_cgpa.py) and in the notebook. The steps are the same in both:

1. Read `data/Student_data.csv`. If the file is missing, the script stops with a short message that points at [data/README.md](data/README.md).
2. Print the shape, the gender and major counts, the summary statistics (mean, median, mode, quartiles), the Pearson correlations, and the Tukey outlier counts.
3. Split the 5,000 rows into 4,000 for training and 1,000 for testing (`train_test_split`, `test_size=0.2`, `random_state=42`).
4. Fit `LinearRegression()` on the five predictors, predict on the test set, and compute MSE, RMSE, MAE and R².
5. Fit `RandomForestRegressor(n_estimators=100, random_state=42)` on the same split, and compute the same metrics plus feature importances.
6. Print the intercept, the five coefficients, the linear equation, and the first ten test predictions. Write the tables and charts under `results/`.

Neither model standardises the inputs. I did not drop outliers, add interactions, or tune the forest. The point of the exercise is this comparison, on the same split the original notebook used.

The linear model is:

```
Final_CGPA = β0 + β1·Study_Hours_Per_Day + β2·Attendance_Pct
           + β3·Sleep_Hours + β4·Social_Hours_Week + β5·Previous_CGPA
```

---

## Test Results

Test set, 1,000 rows. The linear-regression figures below match the original notebook exactly. The random-forest figures are from my re-run (scikit-learn 1.9.1); the notebook had MSE 0.01634155 and R² 0.94301461, which is the same conclusion to four decimal places on R².

| Model | MSE | RMSE | MAE | R² |
|-------|----:|-----:|----:|---:|
| Linear Regression | 0.02601314 | 0.16128589 | 0.13021230 | 0.90928834 |
| **Random Forest** | **0.01632421** | **0.12776624** | **0.10311690** | **0.94307506** |

The forest is ahead on every test metric. On the training set the picture is a little less tidy: linear regression is consistent (train R² 0.9022, test 0.9093), while the forest is nearly perfect on the training rows (R² 0.9906, MSE 0.002347) and drops to 0.9431 on the test set. It is over-fitting a bit, but it still wins on held-out data.

Random-forest feature importances:

| Feature | Importance |
|---------|-----------:|
| Previous_CGPA | **0.7961** |
| Attendance_Pct | 0.1080 |
| Study_Hours_Per_Day | 0.0692 |
| Sleep_Hours | 0.0159 |
| Social_Hours_Week | 0.0108 |

Previous CGPA accounts for about four-fifths of the forest's splits. That matches the 0.8789 correlation and the 0.9262 linear coefficient.

First ten test rows, actual vs predicted (four decimal places):

| Student | Actual | Pred. LR | Pred. RF | Err. LR | Err. RF |
|---------|-------:|---------:|---------:|--------:|--------:|
| ID01502 | 3.1100 | 3.0939 | 3.0874 | −0.0161 | −0.0226 |
| ID02587 | 3.7000 | 3.5330 | 3.6802 | −0.1670 | −0.0198 |
| ID02654 | 2.9300 | 2.8024 | 2.8503 | −0.1276 | −0.0797 |
| ID01056 | 2.6700 | 2.4309 | 2.4456 | −0.2391 | −0.2244 |
| ID00706 | 3.6900 | 3.4348 | 3.4207 | −0.2552 | −0.2693 |
| ID00107 | 3.6800 | 3.6198 | 3.7177 | −0.0602 | 0.0377 |
| ID00590 | 3.5400 | 3.4789 | 3.4800 | −0.0611 | −0.0600 |
| ID02469 | 3.2700 | 3.0897 | 3.2444 | −0.1803 | −0.0256 |
| ID02414 | 3.9000 | 3.8490 | 3.9276 | −0.0510 | 0.0276 |
| ID01601 | 2.7600 | 2.7725 | 2.8353 | 0.0125 | 0.0753 |

On these ten rows the forest is usually closer. ID00706 is a miss for both (actual 3.69, predictions around 3.43). The largest absolute test error I saw across the full 1,000 rows is 0.6372 for linear regression and 0.6179 for the forest. Full-precision tables are in [results/metrics.csv](results/metrics.csv) and [results/predictions.csv](results/predictions.csv).

The original report recorded the notebook's random-forest numbers (MSE 0.01634155, R² 0.94301461) and reached the same conclusion: the forest is the better of the two on this test set.

---

## Learned Equation

Coefficients rounded to six decimal places, as the script prints them:

```
Final_CGPA = -0.678843
           + 0.045074×Study_Hours_Per_Day
           + 0.010971×Attendance_Pct
           − 0.000971×Sleep_Hours
           − 0.003800×Social_Hours_Week
           + 0.926166×Previous_CGPA
```

A few things worth pointing at:

- Previous CGPA carries almost all of the linear fit: holding the other four variables fixed, a one-point difference in previous CGPA maps to about 0.93 points of final CGPA.
- Study hours: about +0.045 CGPA points per extra hour per day.
- Attendance: about +0.011 per percentage point of classes attended.
- Sleep (−0.000971) and social hours (−0.003800) are tiny, and slightly negative. Given how close their correlations are to zero, I would not treat those signs as a finding.

The intercept is −0.678843. The raw coefficients are in [results/coefficients.csv](results/coefficients.csv).

---

## What the Residuals Show

The residual plots (predicted value against actual minus predicted) are in the screenshots below, one for the linear model. They are a fairly tight band around zero — the scale of `Final_CGPA` is only about three points, and a test RMSE of 0.16 is small in that light. I do not see a strong curve the way I would if a straight line were the wrong shape entirely. The leftover error is real, just not dramatic.

The forest tightens that band further (test RMSE 0.1278). The assignment asked for a comparison of predicted and original values on a graph as well as by MSE; those actual-versus-predicted charts are in the screenshots and under [results/figures/](results/figures/).

---

## Training and Test Files

The dataset is in this repository, at [data/Student_data.csv](data/Student_data.csv). The train/test cut is made in the script, not stored as a second pair of files.

| File | Rows | Columns | Where it lives |
|------|------|---------|----------------|
| `Student_data.csv` | 5,000 | 10 | [data/Student_data.csv](data/Student_data.csv) |

Source, as named in the original notebook and the report:

https://www.kaggle.com/datasets/robiulhasanjisan/university-student-performance-and-habits-dataset

A re-run of [src/predict_cgpa.py](src/predict_cgpa.py) on this file reproduces the linear-regression test metrics exactly, and the random-forest metrics to the precision discussed above.

The written report is [docs/report/CGPA_Prediction_Report.pdf](docs/report/CGPA_Prediction_Report.pdf). The assignment brief that was already in the original project folder is at [docs/assignment/Probability_and_Statistics_Project.pdf](docs/assignment/Probability_and_Statistics_Project.pdf).

---

## Folder Structure

```
CGPA_Prediction/
├── notebooks/
│   └── cgpa_prediction.ipynb
├── src/
│   └── predict_cgpa.py
├── data/
│   ├── Student_data.csv
│   └── README.md
├── results/
│   ├── metrics.csv
│   ├── coefficients.csv
│   ├── feature_importances.csv
│   ├── summary_stats.csv
│   ├── correlations.csv
│   ├── outliers.csv
│   ├── equations.txt
│   ├── predictions_head.csv
│   ├── predictions.csv
│   ├── README.txt
│   └── figures/
├── docs/
│   ├── report/CGPA_Prediction_Report.pdf
│   ├── latex/main.tex
│   └── assignment/Probability_and_Statistics_Project.pdf
├── screenshots/               (24 images, 1600×1000, used in this README)
├── assets/
│   ├── css/style.css
│   ├── js/main.js
│   └── favicon.svg
├── index.html
├── requirements.txt
├── LICENSE
├── .gitignore
└── README.md
```

---

## How to Use This Repository

1. **Browse** – this README and the [website](https://rohaan2802.github.io/CGPA_Prediction/) walk through the data, the two fits, the numbers and the charts.
2. **Clone the repo:**
   ```bash
   git clone https://github.com/rohaan2802/CGPA_Prediction.git
   cd CGPA_Prediction
   ```
   or download the [ZIP of main](https://github.com/rohaan2802/CGPA_Prediction/archive/refs/heads/main.zip).
3. **Run the fit** – the commands are in the next section. The CSV is already in `data/`. The script prints the full report and writes `results/`.
4. **Open the notebook** if you would rather step through the same work in Jupyter.

---

## Running the Fit

Python 3, with the packages in [requirements.txt](requirements.txt).

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/predict_cgpa.py
```

**Windows:**

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src\predict_cgpa.py
```

That prints the summary statistics, the correlations, the outlier counts, the coefficients, the test metrics and the linear equation, and writes the files under `results/`. Optional flags: `--data-dir`, `--results-dir` and `--no-plots`.

To walk through the same steps in Jupyter:

```bash
jupyter notebook notebooks/cgpa_prediction.ipynb
```

---

## Screenshots

Every image is 1600×1000. Click one to open it at full size.

### 1. Repository Folder Structure

<p align="center"><img src="screenshots/01-repo-structure.png" alt="Repository folder structure" width="900"></p>

### 2. The Problem

<p align="center"><img src="screenshots/02-problem.png" alt="Predict Final CGPA from five student-habit variables" width="900"></p>

### 3. The Data Table

<p align="center"><img src="screenshots/03-data-schema.png" alt="Shape, columns and first rows of Student_data.csv" width="900"></p>

### 4. Summary Statistics

<p align="center"><img src="screenshots/04-summary-statistics.png" alt="Mean, median, mode and quartiles of the numeric columns" width="900"></p>

### 5. Correlations with Final CGPA

<p align="center"><img src="screenshots/05-correlations.png" alt="Pearson correlations of the numeric columns with Final CGPA" width="900"></p>

### 6. Outliers

<p align="center"><img src="screenshots/06-outliers.png" alt="Tukey IQR outlier counts for each numeric column" width="900"></p>

### 7. Box Plots

<p align="center"><img src="screenshots/07-boxplots.png" alt="Box plots of the seven numeric columns, one panel each" width="900"></p>

### 8. Previous CGPA vs Final CGPA

<p align="center"><img src="screenshots/08-scatter-previous-cgpa.png" alt="Scatter plot of Previous CGPA against Final CGPA" width="900"></p>

### 9. Study Hours vs Final CGPA

<p align="center"><img src="screenshots/09-scatter-study-hours.png" alt="Scatter plot of study hours per day against Final CGPA" width="900"></p>

### 10. Attendance vs Final CGPA

<p align="center"><img src="screenshots/10-scatter-attendance.png" alt="Scatter plot of attendance percentage against Final CGPA" width="900"></p>

### 11. Fitting the Two Models

<p align="center"><img src="screenshots/11-fit-code.png" alt="Python code that fits linear regression and a random forest" width="900"></p>

### 12. Learned Equation

<p align="center"><img src="screenshots/12-learned-equation.png" alt="The fitted multiple linear regression equation" width="900"></p>

### 13. Test Metrics

<p align="center"><img src="screenshots/13-evaluation-metrics.png" alt="Test-set MSE, RMSE, MAE and R-squared for both models" width="900"></p>

### 14. First Ten Test Predictions

<p align="center"><img src="screenshots/14-predictions-head.png" alt="First ten actual and predicted Final CGPA values" width="900"></p>

### 15. Linear-Regression Coefficients

<p align="center"><img src="screenshots/15-coefficients.png" alt="Bar chart of the five linear-regression coefficients" width="900"></p>

### 16. Random-Forest Importances

<p align="center"><img src="screenshots/16-feature-importances.png" alt="Bar chart of random-forest feature importances" width="900"></p>

### 17. Actual vs Predicted — Linear Regression

<p align="center"><img src="screenshots/17-actual-vs-predicted-lr.png" alt="Actual versus predicted scatter plot for linear regression" width="900"></p>

### 18. Actual vs Predicted — Random Forest

<p align="center"><img src="screenshots/18-actual-vs-predicted-rf.png" alt="Actual versus predicted scatter plot for the random forest" width="900"></p>

### 19. Residuals — Linear Regression

<p align="center"><img src="screenshots/19-residuals-lr.png" alt="Residual plot for linear regression" width="900"></p>

### 20. Website Home, Dark Theme

<p align="center"><img src="screenshots/20-website-home-dark.png" alt="Project website home, dark theme" width="900"></p>

### 21. Website Home, Light Theme

<p align="center"><img src="screenshots/21-website-home-light.png" alt="Project website home, light theme" width="900"></p>

### 22. Website on a Phone

<p align="center"><img src="screenshots/22-website-phone.png" alt="Project website on a 390-pixel-wide phone" width="900"></p>

### 23. Website — Results

<p align="center"><img src="screenshots/23-website-results.png" alt="Website results section, test metrics" width="900"></p>

### 24. Website — How to Run

<p align="center"><img src="screenshots/24-website-how-to-run.png" alt="Website how-to-run section" width="900"></p>

---

## License

The code in this repository is under the [MIT License](LICENSE), Copyright (c) 2026 Mohammad Rohaan.

The dataset was sourced from the Kaggle page named above. The assignment brief under `docs/assignment/` was already part of the original project folder.

---

## Author

**Mohammad Rohaan**
22I-2327

- GitHub: [@rohaan2802](https://github.com/rohaan2802)
- Email: [m.rohaanarshad@gmail.com](mailto:m.rohaanarshad@gmail.com)
