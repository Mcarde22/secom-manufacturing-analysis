"""Mini Process-Stability Dashboard

This script builds control charts (basic SPC - Statistical Process Control)
for a handful of sensors from the SECOM dataset. The idea: for each sensor,
plot its readings over time with lines for the mean and +/- 3 standard
deviations (the "control limits"). Any point outside those lines is
considered "out of control" - i.e. the process might be drifting or
something weird happened on that unit.

"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR.parent / "data" / "uci-secom-cleaned.csv"
df = pd.read_csv(csv_path)

# ---------------------------------------------------------
# STEP 1: pick the sensors we actually want to look at
# ---------------------------------------------------------
# don't try to dashboard all 590 columns, nobody can read that.
# instead of just grabbing the first N columns, use the outlier ranking
# csv that panda_1_2.py now saves - that gives us the sensors that are
# actually the "worst behaved" (most outliers), which is exactly what
# we want to keep an eye on in a process-stability dashboard.

N_SENSORS = 9  # change this if you want more/fewer panels in the grid

ranking_path = BASE_DIR.parent / "data" / "sensor_outlier_ranking.csv"
ranking_df = pd.read_csv(ranking_path)

# column names got read in as strings here, and df's columns are also
# strings (SECOM sensor columns are named '0', '1', '2', ... etc), so
# this lines up fine as long as both were saved/read consistently.
selected_sensors = ranking_df["sensor"].astype(str).head(N_SENSORS).tolist()

print(f"Building dashboard for {len(selected_sensors)} sensors: {selected_sensors}")

# ---------------------------------------------------------
# STEP 2 + 3: calculate control limits per sensor and flag
# out-of-control points
# ---------------------------------------------------------
# for each sensor:
#   mean = average reading
#   std = standard deviation (how spread out the readings are)
#   UCL (upper control limit) = mean + 3*std
#   LCL (lower control limit) = mean - 3*std
# anything outside [LCL, UCL] gets flagged as "out of control"

summary_rows = []  # we'll build a little summary table as we go

for col in selected_sensors:
    mean = df[col].mean()
    std = df[col].std()
    ucl = mean + 3 * std
    lcl = mean - 3 * std

    out_of_control = (df[col] > ucl) | (df[col] < lcl)
    pct_out = out_of_control.mean() * 100  # mean() on a bool series = % True

    summary_rows.append({
        "sensor": col,
        "mean": mean,
        "std": std,
        "pct_out_of_control": pct_out,
        "n_out_of_control": int(out_of_control.sum())
    })

summary_df = pd.DataFrame(summary_rows).sort_values("pct_out_of_control", ascending=False)
print("\nSummary (worst sensors first):")
print(summary_df.to_string(index=False))

# STEP 4: build the multi-panel control charts
# 3x3 grid

n_sensors = len(selected_sensors)
ncols = 3
nrows = -(-n_sensors // ncols)  # ceiling division so we always have enough panels

fig, axes = plt.subplots(nrows, ncols, figsize=(15, 4 * nrows))
axes = axes.flatten()  # makes it easier to loop through regardless of grid shape

for i, col in enumerate(selected_sensors):
    ax = axes[i]
    mean = df[col].mean()
    std = df[col].std()
    ucl = mean + 3 * std
    lcl = mean - 3 * std

    out_of_control = (df[col] > ucl) | (df[col] < lcl)

    # plot in-control points in blue, out-of-control points in red
    ax.scatter(df.index[~out_of_control], df[col][~out_of_control], s=8, color="steelblue", alpha=0.5)
    ax.scatter(df.index[out_of_control], df[col][out_of_control], s=12, color="red")

    ax.axhline(mean, color="green", linestyle="-", linewidth=1, label="mean")
    ax.axhline(ucl, color="orange", linestyle="--", linewidth=1, label="UCL/LCL (+-3 std)")
    ax.axhline(lcl, color="orange", linestyle="--", linewidth=1)

    ax.set_title(f"Sensor {col}", fontsize=10)
    ax.tick_params(labelsize=7)

# hide any unused subplot panels (happens if n_sensors isn't a perfect multiple of ncols)
for j in range(n_sensors, len(axes)):
    axes[j].axis("off")

fig.suptitle("Mini Process-Stability Dashboard - SECOM Sensors", fontsize=14)
fig.tight_layout()

# ---------------------------------------------------------
# STEP 6: save it as a standalone report
# ---------------------------------------------------------
dashboard_dir = BASE_DIR.parent / "dashboard"
dashboard_dir.mkdir(exist_ok=True)  # makes the dashboard/ folder if it doesn't exist yet

fig_path = dashboard_dir / "process_stability_dashboard.png"
fig.savefig(fig_path, dpi=150)
print(f"\nDashboard image saved to: {fig_path}")

summary_path = dashboard_dir / "process_stability_summary.csv"
summary_df.to_csv(summary_path, index=False)
print(f"Summary table saved to: {summary_path}")

plt.show()