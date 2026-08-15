"""Finally, lets plot the correlation matrix to see if there are any columns that are highly correlated with each other.
\nIf there are, we can drop one of the columns because they are redundant.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR.parent / "data" / "uci-secom-cleaned.csv")

df['0'].hist(bins=50)
plt.show()

plt.figure(figsize=(8, 6))
plt.scatter(df['0'], df['1'], c=df['Pass/Fail'], cmap='coolwarm', alpha=0.5, s=10)
plt.title("Sensor 0 vs Sensor 1, colored by Pass/Fail")
plt.xlabel("Sensor 0")
plt.ylabel("Sensor 1")
plt.colorbar(label='Pass/Fail')
plt.show()