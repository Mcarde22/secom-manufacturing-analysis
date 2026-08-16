"""Pandas DataFrame operations

Converting Into a Correct Format

We need to see if there is any dat with wrong format. The obvious problem is that this is an enourmous file
and it is not possible to check all the data manually."""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR.parent / "data" / "uci-secom.csv"

df = pd.read_csv(csv_path)

#a look at the actual data 
print(df.head())

#print the data types of each column to see if there are any columns with wrong data types
print(df.dtypes)

print("You can see that the data types of the columns are good.\nYes Time has object data type but it is not a problem because we will not use it in our analysis.\nThe rest of the columns are float64 which is good.")
print("If there were issues you would have to convert the data types of the columns to the correct data types.\nFor example, if a column has object data type but it should be float64, you would have to convert it using df['column_name'] = pd.to_numeric(df['column_name'], format = 'mixed')\nThis will convert the column to float64 and any values that cannot be converted will be set to NaN.\nYou can also use df['column_name'] = df['column_name'].astype(float) if you are sure that all the values can be converted to float64.\n")
print("Now we will tackle a big probelm that SECOM data has. Empty Values.")

# variable to store the number of empty values in each column
empty_values = df.isnull().sum()
print("Number of empty values in each column:")
print(empty_values)

#display the columns with empty values
print("Columns with empty values:")
print(f"\nColumns with missing data: {len(empty_values[empty_values > 0])} out of {df.shape[1]}")

#the total number of empty cells in the dataset
total_empty_values = df.isnull().sum().sum()
print(f"\nTotal empty cells in the dataset: {total_empty_values}") 

#the total number of rows that are missing data
total_missing_rows = df.isnull().any(axis=1).sum()
print(f"\nTotal rows with missing data: {total_missing_rows}")


"""Now lets address the empty values. One way to deal withe mpty values
is to simply remove the entire row that has empty values. This is a good approach if the number of rows with empty values is small compared to the total number of rows in the dataset. However, if the number of rows with empty values is large, then we will lose a lot of data and this is not a good approach."""


# drop only rows missing MORE than some threshold - much more realistic
# thresh = minimum number of NON-null values required to keep the row
df_dropped_rows = df.dropna(thresh=df.shape[1] - 50)  # allow up to 50 missing per row

# drop COLUMNS instead, if a column is missing too much to be useful
df_dropped_cols = df.dropna(axis=1, thresh=len(df) * 0.5)  # keep cols with >=50% data present

#now reprint the number of empty rows and columns after dropping the rows and columns with too many empty values
print(f"\nAfter dropping rows with more than 50 missing values, the number of rows with missing data is: {df_dropped_rows.isnull().any(axis=1).sum()}")
print(f"\nAfter dropping columns with more than 50% missing values, the number of columns with missing data is: {df_dropped_cols.isnull().sum().sum()}")

print("\nNow lets address wrong data. It can be simple inequivalent numeric types, and fixing them manually is really easy" \
"\nwell, atleast with df.loc[row_index, column_index] = new_value, but it is not a good approach if there are many wrong data points. In that case, we can use a for loop to iterate through the rows and fix them.")
print("In our case, we will create boundires for allowable values.\n")


sensor_cols = df.select_dtypes(include='number').columns.drop('Pass/Fail')

outlier_counts = {}

for col in sensor_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    # 3.0 instead of 1.5 = wider net, only flags truly extreme values
    lower_bound = Q1 - 3.0 * IQR
    upper_bound = Q3 + 3.0 * IQR

    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]

    if len(outliers) > 0:
        outlier_counts[col] = len(outliers)

outlier_series = pd.Series(outlier_counts).sort_values(ascending=False)
print(f"\nColumns with outliers: {len(outlier_series)} out of {len(sensor_cols)}")
print(outlier_series.head(20))

# save the ranked outlier counts to their own csv so we can just read
# the top sensor names later instead of copy-pasting from the console
outlier_series_path = BASE_DIR.parent / "data" / "sensor_outlier_ranking.csv"
outlier_series.rename("outlier_count").rename_axis("sensor").to_csv(outlier_series_path)
print(f"Sensor outlier ranking saved to: {outlier_series_path}")

# now see it from the ROW side - how many rows have at least one out-of-bound value
row_has_outlier = pd.Series(False, index=df.index)
for col in sensor_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 3.0 * IQR
    upper_bound = Q3 + 3.0 * IQR
    row_has_outlier |= (df[col] < lower_bound) | (df[col] > upper_bound)

print(f"\nRows with at least one outlier value: {row_has_outlier.sum()} out of {len(df)}")

"""Now lets actually drop the bad rows."""
# before removing - keep a record of how many rows you're about to lose
print(f"Rows before removal: {len(df)}")

# keep only rows where row_has_outlier is False (i.e. no outlier anywhere in that row)
df_cleaned = df[~row_has_outlier]

print(f"Rows after removal: {len(df_cleaned)}")
print(f"Rows removed: {len(df) - len(df_cleaned)}")

"""Now lets see if there are anyduplicare rows. The following prints a boolean
\n value for each row indicating whether it is a duplicate of a previous row.\n We can use this to drop the duplicate rows."""

print(df.duplicated())

#now drop the duplicate rows

df.drop_duplicates(inplace = True)

"""Lets use the correlation method to see if there are any columns that are highly correlated with each other. 
\nIf there are, we can drop one of the columns because they are redundant."""

correlation_matrix = df.corr(numeric_only=True)

# find pairs of columns with correlation above 0.95 (very likely redundant)
high_corr_pairs = []
cols = correlation_matrix.columns

for i in range(len(cols)):
    for j in range(i + 1, len(cols)):  # only check each pair once
        corr_value = correlation_matrix.iloc[i, j]
        if abs(corr_value) > 0.95:
            high_corr_pairs.append((cols[i], cols[j], corr_value))

print(f"Highly correlated pairs found: {len(high_corr_pairs)}")
for col1, col2, val in high_corr_pairs:
    print(f"{col1} <-> {col2}: {val:.3f}")
# save the cleaned dataframe to a new CSV so other scripts (like plot_1.py) can use it
df_cleaned.to_csv(BASE_DIR.parent / "data" / "uci-secom-cleaned.csv", index=False)
print(f"\nCleaned data saved: {len(df_cleaned)} rows, {df_cleaned.shape[1]} columns")