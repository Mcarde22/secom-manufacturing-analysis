"""This is the exploration script for the yield data. It is meant to be run in a Jupyter notebook, but can also be run as a standalone script. 
It is not meant to be run as a standalone script, but rather as a module that can be imported into a Jupyter notebook.
Though it is worth noting that I will not be doing that. I just want to see the imbalnces from the cleaned csv file from dashboard_1.py. I will be using the cleaned csv file from dashboard_1.py to explore the yield data."""


import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR.parent / "data" / "uci-secom-cleaned.csv"
df = pd.read_csv(csv_path)

# A quick look into the columns to identify the column we are looking for 
print(df.columns.tolist()) 

# The column we are looking for is 'Pass/Fail' which is the last column in the dataframe.
#now we can check the value counts of the 'Pass/Fail' column to see the distribution of the yield data.
print(df["Pass/Fail"].value_counts())

"""Our output in the end showed 
   Pass/Fail
   -1    158
   1     12
This means we had 158 passed and 12 failed. This is a very imbalanced dataset, which is not ideal for training a machine learning model. We will need to -
address this imbalance before we can train a model on this data.
It is kind of intresting because it is about a 13 to 1 ratio of passed to failed. In a small scale this is "okay" but in a large scale this is not ideal."""

print("An important thing to notice, our cleaned csv file from dashboard_1.py has an agressive row drop.We now need to verify that " \
"what we did was the right procedure.Check yeild_explore_2.py for the next steps in this process. We will be using the cleaned csv file from dashboard_1.py to explore the yield data.")