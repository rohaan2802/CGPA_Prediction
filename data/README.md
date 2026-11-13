# Data

`Student_data.csv` is included in this folder. It is the same table that was already in the original project: 5,000 rows and 10 columns, with no missing cells.

Source, as recorded in the original notebook and the written report:

https://www.kaggle.com/datasets/robiulhasanjisan/university-student-performance-and-habits-dataset

Columns: `Student_ID`, `Gender`, `Age`, `Major`, `Attendance_Pct`, `Study_Hours_Per_Day`, `Previous_CGPA`, `Sleep_Hours`, `Social_Hours_Week`, `Final_CGPA`.

The two models in this repository use five of those columns as predictors — `Study_Hours_Per_Day`, `Attendance_Pct`, `Sleep_Hours`, `Social_Hours_Week`, `Previous_CGPA` — and `Final_CGPA` as the target. The 4,000 / 1,000 train–test split is made in the script (`test_size=0.2`, `random_state=42`), not stored as a separate pair of files.
