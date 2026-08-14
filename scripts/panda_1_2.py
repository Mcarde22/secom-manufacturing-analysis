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