These files are written by a run of src/predict_cgpa.py (same 80/20 split,
random_state=42, LinearRegression and RandomForestRegressor with 100 trees).

  metrics.csv              test and train MSE, RMSE, MAE, R-squared
  coefficients.csv         linear-regression intercept and coefficients
  feature_importances.csv  random-forest importances on the five predictors
  summary_stats.csv        count, mean, std, min, quartiles, max, mode
  correlations.csv         Pearson correlations of the numeric columns
  outliers.csv             Tukey's IQR outlier counts
  equations.txt            the fitted linear equation
  predictions_head.csv     first ten test rows, actual vs both models
  predictions.csv          all 1,000 test rows
  figures/                 charts from the same run
