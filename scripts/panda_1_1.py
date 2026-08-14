#Below is the code segmant to load a CSV file into a Pandas DataFrame:
from pathlib import Path
import pandas as pd
BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR.parent / "data" / "uci-secom.csv"
df = pd.read_csv(csv_path)

print(df.to_string())

print(df.shape)

print(df.head())

"""below is the code segmant to print a simple panda Series
    -> Keep in mind that a Series is a one-dimensional array-like object 
       that can hold many data types, including objects. 
       It is similar to a column in a DataFrame.
"""
my_series = pd.Series([1, 2, 3, 4, 5])
print(my_series)

"""below is the code segment for labels 
    -> Labels are the index values of a Series or DataFrame. 
       They can be used to access specific elements in the data structure.
"""
#Below is the first value of the Series
print(f"The first value of the Series is: {my_series[0]}")

"""now we will access specified row(s)"""

#refer to the row index:
print(f"The first row of the DataFrame is:\n{df.loc[0]}")

"""A check of the max and min values of the DataFrame"""
print(f"print(pd.options.display.max_rows) = {pd.options.display.max_rows}")
print("So as you can see the max rows is set to 60, so if the DataFrame has more than 60 rows, it will not display all of them.\n" \
"To change this setting, you can use the following code:\n" \
"pd.options.display.max_rows = 9999\n" )

pd.options.display.max_rows = 9999

df = pd.read_csv(csv_path)
print(df)

"""Now we will look at the most ost used method for getting a quick overview of the DataFrame, is the head() method.
   The head() method returns the headers and a specified number of rows, starting from the top."""

#Below is the code segment to print the first 10 rows of the DataFrame
print(f'df.head(10): "or first ten rows"{df.head(10)}')

"""There is also a tail() method for viewing the last rows of the DataFrame.
The tail() method returns the headers and a specified number of rows, starting from the bottom."""
print(f'df.tail(10): "or last ten rows"{df.tail(10)}')

"""The DataFrames object has a method called info(), that gives you more information about the data set."""
print(f'df.info():"Code that gives information about the DataFrame"{df.info()}')

"""Now we need to clean the data

Data cleaning means fixing bad data in your data set.

Bad data could be:

->Empty cells
->Data in wrong format
->Wrong data
->Duplicates"""

"""Lets clean empty cells. The reason why it is important to clean empty cells is that they can cause problems when analyzing the data.
For example, if you try to calculate the average of a column that has empty cells, you will get an error. So it is important to clean empty
 cells before analyzing the data.
 -> a quick way of doing this is to emove rows with empty cells
 -> below is the code segment to remove rows with empty cells from the DataFrame"""

df = pd.read_csv(csv_path)
print(df.shape)

new_df = df.dropna()
print(new_df.shape)

print(new_df.to_string())

print("Below is the code segment execution to Remove all rows with NULL values\n")

print("df = pd.read_csv(csv_path)\ndf.dropna(inplace = True)\nprint(df.to_string())")

"""         Replace Empty Values
            --------------------
Another way of dealing with empty cells is to insert a new value instead.

This way you do not have to delete entire rows just because of some empty cells.

The fillna() method allows us to replace empty cells with a value for this example, we wont be doing that. """

"""     Replace Empty Values (better way)
        ----------------------------------
instead of dropping rows with dropna(), we can just fill the empty
spots with a calculated value instead. this way we keep all our
rows instead of losing data.

-> mean() gets the average for EACH column separately, since every
   sensor column is measuring something different on a different
   scale. one big average for the whole table wouldn't make sense.

df.fillna(df.mean(), inplace=True) is doing 3 things:
    1. df.mean() calculates the average of every column
    2. fillna() replaces NaNs in each column with that column's mean
    3. inplace=True just applies it directly to df, no need to
       reassign it to a new variable
"""

df.fillna(df.mean(numeric_only=True), inplace=True)
#KEEP IN MIND THAT THE CODE LOOKS A BIT DIFFERENT THAN THE EXAMPLE IN THE COMMENT, THIS IS BECAUSE OF A DEPRECATION WARNING THAT CAME UP WHEN I RAN THE CODE. I ADDED THE numeric_only=True PARAMETER TO THE mean() FUNCTION TO FIX IT.
print(df.shape)

print(df.to_string())

"""     Replace Empty Values with Median
        ---------------------------------
median is the middle value when you sort all the numbers in a
column. unlike mean, it's not thrown off by extreme outliers
(like if a sensor glitched and gave one crazy high reading).

df.fillna(df.median(), inplace=True) does the same 3 steps as
mean, just uses median() instead:
    1. df.median() finds the middle value for each column
    2. fillna() replaces NaNs in each column with that column's median
    3. inplace=True applies it directly to df
"""

df.fillna(df.median(numeric_only=True), inplace=True)
print(df.shape)

print(df.to_string())

"""     Replace Empty Values with Mode
        --------------------------------
mode is just the most frequently occurring value in a column.
makes more sense for categorical/repeated-value data than for
continuous sensor readings, but still good to know.

df.fillna(df.mode().iloc[0], inplace=True):
    1. df.mode() finds the most common value in each column, but
       it returns a whole DataFrame (there can be more than one
       mode if there's a tie), so we grab the first row with .iloc[0]
    2. fillna() replaces NaNs with that value
    3. inplace=True applies it directly to df
    """

df.fillna(df.mode().iloc[0], inplace=True)

print(df.to_string())
"""     Cleaning Data
        -------------
        Cleaning data is an important step in the data analysis process. It is important to clean the data before analyzing it, because bad data can cause problems when analyzing the data. There are many ways to clean data, but the most common ways are to remove empty cells, replace empty cells with a value, and remove duplicates.
        Below is the code segment to convert into a correct format"""

