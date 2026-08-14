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
