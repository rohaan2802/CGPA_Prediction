#!/usr/bin/env python3
"""Fit two models that predict Final_CGPA from five student-habit columns.

Multiple linear regression (ordinary least squares) and a random forest
(100 trees). The 5,000-row table is split 80/20 with random_state=42,
which is the same split the original notebook used.

Run from the repository root:

    python src/predict_cgpa.py

Optional flags: --data-dir, --results-dir, --no-plots.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

FEATURES = [
    "Study_Hours_Per_Day",
    "Attendance_Pct",
    "Sleep_Hours",
    "Social_Hours_Week",
    "Previous_CGPA",
]
TARGET = "Final_CGPA"
NUMERIC = [
    "Age",
    "Attendance_Pct",
    "Study_Hours_Per_Day",
    "Previous_CGPA",
    "Sleep_Hours",
    "Social_Hours_Week",
    "Final_CGPA",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_data(data_dir: Path) -> pd.DataFrame:
    path = data_dir / "Student_data.csv"
    if not path.is_file():
        sys.exit(
            f"Could not find {path}. The table should sit in data/ as "
            "Student_data.csv. See data/README.md."
        )
    df = pd.read_csv(path)
    missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing:
        sys.exit(f"Student_data.csv is missing columns: {missing}")
    return df


def summary_table(df: pd.DataFrame) -> pd.DataFrame:
    desc = df[NUMERIC].describe().T
    modes = []
    mode_counts = []
    for col in NUMERIC:
        mode = df[col].mode().iloc[0]
        modes.append(mode)
        mode_counts.append(int((df[col] == mode).sum()))
    desc["mode"] = modes
    desc["mode_count"] = mode_counts
    desc = desc.rename(
        columns={
            "50%": "median",
            "25%": "q1",
            "75%": "q3",
        }
    )
    return desc[
        ["count", "mean", "std", "min", "q1", "median", "q3", "max", "mode", "mode_count"]
    ]


def iqr_outliers(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col in NUMERIC:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        mask = (df[col] < lo) | (df[col] > hi)
        rows.append(
            {
                "column": col,
                "n_outliers": int(mask.sum()),
                "pct": 100.0 * float(mask.sum()) / len(df),
                "fence_low": lo,
                "fence_high": hi,
                "min": df[col].min(),
                "max": df[col].max(),
            }
        )
    return pd.DataFrame(rows)


def metrics(y_true, y_pred) -> dict:
    mse = float(mean_squared_error(y_true, y_pred))
    return {
        "MSE": mse,
        "RMSE": float(np.sqrt(mse)),
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "R2": float(r2_score(y_true, y_pred)),
    }


def fit_models(df: pd.DataFrame):
    X = df[FEATURES]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    lr_train = lr.predict(X_train)

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_train = rf.predict(X_train)

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "lr": lr,
        "rf": rf,
        "lr_pred": lr_pred,
        "rf_pred": rf_pred,
        "lr_train": lr_train,
        "rf_train": rf_train,
    }


def equation_text(lr: LinearRegression) -> str:
    terms = [f"{lr.intercept_:.6f}"]
    for name, coef in zip(FEATURES, lr.coef_):
        sign = "+" if coef >= 0 else "-"
        terms.append(f"{sign} {abs(coef):.6f}*{name}")
    return f"{TARGET} = " + " ".join(terms)


def write_plots(fit: dict, out_dir: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns

    out_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", font="DejaVu Sans")

    y_test = fit["y_test"]
    lr_pred = fit["lr_pred"]
    rf_pred = fit["rf_pred"]
    lr = fit["lr"]
    rf = fit["rf"]
    df = fit["df"]

    # Box plots, one panel per variable so the scales stay readable.
    fig, axes = plt.subplots(2, 4, figsize=(14, 7))
    axes = axes.ravel()
    palette = sns.color_palette("Set2", n_colors=len(NUMERIC))
    for ax, col, color in zip(axes, NUMERIC, palette):
        sns.boxplot(y=df[col], ax=ax, color=color, fliersize=3)
        ax.set_xlabel("")
        ax.set_ylabel(col)
        ax.set_title(col, fontsize=10)
    axes[-1].axis("off")
    fig.suptitle("Box plots of the numeric columns", fontsize=13)
    fig.tight_layout()
    fig.savefig(out_dir / "boxplots.png", dpi=140, bbox_inches="tight")
    plt.close(fig)

    def scatter(x, title, fname, color):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(df[x], df[TARGET], s=10, alpha=0.28, c=color, linewidths=0)
        ax.set_xlabel(x)
        ax.set_ylabel(TARGET)
        ax.set_title(title)
        fig.tight_layout()
        fig.savefig(out_dir / fname, dpi=140, bbox_inches="tight")
        plt.close(fig)

    scatter("Previous_CGPA", "Previous CGPA vs Final CGPA", "scatter_previous_cgpa.png", "#c45e12")
    scatter("Study_Hours_Per_Day", "Study hours vs Final CGPA", "scatter_study_hours.png", "#2f6f8f")
    scatter("Attendance_Pct", "Attendance vs Final CGPA", "scatter_attendance.png", "#3d7a4a")
    scatter("Sleep_Hours", "Sleep hours vs Final CGPA", "scatter_sleep.png", "#7a4e2a")
    scatter("Social_Hours_Week", "Social hours vs Final CGPA", "scatter_social.png", "#5c4a78")

    corr = df[NUMERIC].corr()
    fig, ax = plt.subplots(figsize=(8.5, 7))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".3f",
        cmap="YlOrBr",
        vmin=-1,
        vmax=1,
        ax=ax,
        square=True,
        annot_kws={"size": 8},
    )
    ax.set_title("Pearson correlations")
    fig.tight_layout()
    fig.savefig(out_dir / "correlations.png", dpi=140, bbox_inches="tight")
    plt.close(fig)

    def actual_vs_pred(pred, title, fname, color):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(y_test, pred, s=14, alpha=0.4, c=color, linewidths=0)
        lo = min(float(y_test.min()), float(pred.min()))
        hi = max(float(y_test.max()), float(pred.max()))
        ax.plot([lo, hi], [lo, hi], color="#222", linewidth=1.2, label="y = x")
        ax.set_xlabel("Actual Final CGPA")
        ax.set_ylabel("Predicted Final CGPA")
        ax.set_title(title)
        ax.legend()
        fig.tight_layout()
        fig.savefig(out_dir / fname, dpi=140, bbox_inches="tight")
        plt.close(fig)

    actual_vs_pred(lr_pred, "Actual vs predicted — linear regression", "actual_vs_predicted_lr.png", "#c45e12")
    actual_vs_pred(rf_pred, "Actual vs predicted — random forest", "actual_vs_predicted_rf.png", "#2f6f8f")

    def residuals(pred, title, fname, color):
        resid = y_test.to_numpy() - pred
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(pred, resid, s=14, alpha=0.4, c=color, linewidths=0)
        ax.axhline(0, color="#222", linewidth=1.2)
        ax.set_xlabel("Predicted Final CGPA")
        ax.set_ylabel("Residual (actual − predicted)")
        ax.set_title(title)
        fig.tight_layout()
        fig.savefig(out_dir / fname, dpi=140, bbox_inches="tight")
        plt.close(fig)

    residuals(lr_pred, "Residuals — linear regression", "residuals_lr.png", "#c45e12")
    residuals(rf_pred, "Residuals — random forest", "residuals_rf.png", "#2f6f8f")

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#c45e12" if c >= 0 else "#7a2e0e" for c in lr.coef_]
    ax.barh(FEATURES, lr.coef_, color=colors)
    ax.axvline(0, color="#222", linewidth=1)
    ax.set_xlabel("Coefficient")
    ax.set_title("Linear-regression coefficients")
    fig.tight_layout()
    fig.savefig(out_dir / "coefficients_lr.png", dpi=140, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(FEATURES, rf.feature_importances_, color="#c45e12")
    ax.set_xlabel("Importance")
    ax.set_title("Random-forest feature importances")
    fig.tight_layout()
    fig.savefig(out_dir / "feature_importances.png", dpi=140, bbox_inches="tight")
    plt.close(fig)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    root = repo_root()
    parser.add_argument("--data-dir", type=Path, default=root / "data")
    parser.add_argument("--results-dir", type=Path, default=root / "results")
    parser.add_argument("--no-plots", action="store_true")
    args = parser.parse_args(argv)

    df = load_data(args.data_dir)
    results_dir = args.results_dir
    results_dir.mkdir(parents=True, exist_ok=True)
    figures = results_dir / "figures"

    print(f"Loaded {len(df)} rows × {df.shape[1]} columns from {args.data_dir / 'Student_data.csv'}")
    print(f"Missing cells: {int(df.isna().sum().sum())}")
    print(f"Duplicate Student_ID values: {int(df['Student_ID'].duplicated().sum()) if 'Student_ID' in df.columns else 'n/a'}")
    print()

    if "Gender" in df.columns:
        print("Gender counts:")
        print(df["Gender"].value_counts().to_string())
        print()
    if "Major" in df.columns:
        print("Major counts:")
        print(df["Major"].value_counts().to_string())
        print()

    summary = summary_table(df)
    print("Summary statistics (numeric columns):")
    print(summary.to_string(float_format=lambda x: f"{x:.6f}"))
    print()
    summary.to_csv(results_dir / "summary_stats.csv")

    corr = df[NUMERIC].corr()
    print("Pearson correlations:")
    print(corr.round(6).to_string())
    print()
    corr.to_csv(results_dir / "correlations.csv")

    outliers = iqr_outliers(df)
    print("Tukey IQR outliers (1.5 × IQR fences):")
    print(outliers.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print()
    outliers.to_csv(results_dir / "outliers.csv", index=False)

    fit = fit_models(df)
    fit["df"] = df
    lr = fit["lr"]
    rf = fit["rf"]

    print(f"Train rows: {len(fit['X_train'])}   Test rows: {len(fit['X_test'])}")
    print("Split: test_size=0.2, random_state=42")
    print()

    print("Linear regression coefficients:")
    print(f"  intercept             {lr.intercept_:.12f}")
    for name, coef in zip(FEATURES, lr.coef_):
        print(f"  {name:<22s} {coef:.12f}")
    print()
    eq = equation_text(lr)
    print("Learned equation (six decimal places):")
    print(f"  {eq}")
    print()

    lr_test = metrics(fit["y_test"], fit["lr_pred"])
    lr_tr = metrics(fit["y_train"], fit["lr_train"])
    rf_test = metrics(fit["y_test"], fit["rf_pred"])
    rf_tr = metrics(fit["y_train"], fit["rf_train"])

    print("Test-set metrics:")
    print(f"  Linear Regression   MSE={lr_test['MSE']:.12f}  RMSE={lr_test['RMSE']:.8f}  MAE={lr_test['MAE']:.8f}  R2={lr_test['R2']:.12f}")
    print(f"  Random Forest       MSE={rf_test['MSE']:.12f}  RMSE={rf_test['RMSE']:.8f}  MAE={rf_test['MAE']:.8f}  R2={rf_test['R2']:.12f}")
    print()
    print("Training-set metrics:")
    print(f"  Linear Regression   MSE={lr_tr['MSE']:.12f}  R2={lr_tr['R2']:.12f}")
    print(f"  Random Forest       MSE={rf_tr['MSE']:.12f}  R2={rf_tr['R2']:.12f}")
    print()

    print("Random-forest feature importances:")
    for name, val in zip(FEATURES, rf.feature_importances_):
        print(f"  {name:<22s} {val:.12f}")
    print()

    if rf_test["MSE"] < lr_test["MSE"]:
        print("On this test set the random forest has the lower MSE and the higher R-squared.")
    else:
        print("On this test set linear regression has the lower MSE.")
    print()

    coef_df = pd.DataFrame(
        {
            "term": ["intercept"] + FEATURES,
            "coefficient": [float(lr.intercept_)] + [float(c) for c in lr.coef_],
        }
    )
    coef_df.to_csv(results_dir / "coefficients.csv", index=False)

    imp_df = pd.DataFrame(
        {"feature": FEATURES, "importance": [float(v) for v in rf.feature_importances_]}
    )
    imp_df.to_csv(results_dir / "feature_importances.csv", index=False)

    metrics_df = pd.DataFrame(
        [
            {"model": "LinearRegression", "split": "test", **lr_test},
            {"model": "RandomForest", "split": "test", **rf_test},
            {"model": "LinearRegression", "split": "train", **lr_tr},
            {"model": "RandomForest", "split": "train", **rf_tr},
        ]
    )
    metrics_df.to_csv(results_dir / "metrics.csv", index=False)

    (results_dir / "equations.txt").write_text(eq + "\n", encoding="utf-8")

    pred = pd.DataFrame(
        {
            "Student_ID": df.loc[fit["X_test"].index, "Student_ID"].values
            if "Student_ID" in df.columns
            else fit["X_test"].index,
            "Actual": fit["y_test"].values,
            "Pred_LR": fit["lr_pred"],
            "Pred_RF": fit["rf_pred"],
            "Err_LR": fit["lr_pred"] - fit["y_test"].values,
            "Err_RF": fit["rf_pred"] - fit["y_test"].values,
        }
    )
    pred.to_csv(results_dir / "predictions.csv", index=False)
    pred.head(10).to_csv(results_dir / "predictions_head.csv", index=False)

    print("First ten test rows (actual vs predicted):")
    print(pred.head(10).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print()

    if not args.no_plots:
        write_plots(fit, figures)
        print(f"Wrote charts to {figures}")

    print(f"Wrote tables to {results_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
