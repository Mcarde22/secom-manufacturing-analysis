SECOM Manufacturing Analysis

Exploratory data analysis and process monitoring tools built on the UCI SECOM dataset - a real-world semiconductor manufacturing dataset capturing sensor readings from the wafer fabrication process alongside pass/fail outcomes.

This project is part of my prep for a semiconductor manufacturing internship, combining data analysis, process monitoring, and low-level systems programming.

Roadmap
 SECOM dataset analysis - load, explore, and clean the dataset (missing values, outliers, basic stats)
 Process dashboard - visualize sensor trends and pass/fail patterns
 Standard Operating Procedure (SOP) - document a repeatable process for monitoring manufacturing data
 C data logger - lightweight C program for logging sensor-style data in real time
Dataset

This project uses the SECOM dataset from the UCI Machine Learning Repository. It contains 1567 samples of 590 anonymized sensor measurements collected during semiconductor manufacturing, along with a pass/fail label for each unit.

The dataset is not included in this repository. Download it from the link above and place it in the data/ folder as uci-secom.csv.

Project Structure
secom-manufacturing-analysis/
|-- data/           # dataset (gitignored, download separately)
|-- scripts/        # Python analysis scripts
|-- dashboard/       # process dashboard (in progress)
|-- docs/           # SOP and project notes
|-- c_logger/       # C data logger (planned)
|-- .gitignore
|-- LICENSE
└-- README.md
Setup
Clone this repository
   git clone https://github.com/Mcarde22/secom-manufacturing-analysis.git
Install dependencies
   pip install pandas
Download the SECOM dataset and place uci-secom.csv in the data/ folder
Run the analysis script
   python scripts/panda_1_1.py
Tech Stack
Python (pandas)
C (planned, for the data logger)
About

By Mario Cardenas, a Computer Science student pursuing a career in semiconductor and defense manufacturing. This repo is also a running log of learning pandas and data cleaning techniques from the ground up.
 Known limitation/decision log
- Initial cleaning used a per-row outlier filter (any sensor outside 3×IQR removed the row).
  With ~590 sensor columns, this compounded aggressively and dropped rows from 1,567 → 170,
  disproportionately removing rare fail-case rows.
- Switched to a column-based missing-data threshold instead, to preserve as many rows
  (especially fail cases) as possible. Outlier detection may be revisited later as a
  per-sensor flag rather than a row-elimination filter.

License

This project's code is licensed under the MIT License - see LICENSE for details. The SECOM dataset itself is used under UCI Machine Learning Repository's terms and is not covered by this project's license.
