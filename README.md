# Final Report, Automation & Presentation (Task 5)

An automated data pipeline plus an executive summary report, built as the final project of the ApexPlanet internship.
It loads raw data, cleans it, saves the processed data, calculates KPIs and exports everything to Excel, on a schedule.

## Features
- Loads raw CSV data
- Cleans it: standardises column names, removes duplicates, fixes text, parses dates, fills missing values
- Saves processed data to `data/processed/`
- Calculates KPIs (total sales, average sales, total profit, profit margin) and breakdowns by region and category
- Exports a formatted multi-sheet Excel report to `output/kpi_report.xlsx`
- Runs automatically with **GitHub Actions** (daily) or **Windows Task Scheduler**

## Project structure
```
.
├── data/
│   ├── raw/                  # input data (sales_data.csv)
│   └── processed/            # cleaned output
├── output/                   # Excel KPI report
├── docs/                     # report PDF + dashboard screenshot
├── .github/workflows/
│   └── pipeline.yml          # GitHub Actions schedule
├── pipeline.py               # main automation script
├── generate_sample_data.py   # creates sample data
├── run_pipeline.bat          # Windows Task Scheduler entry point
├── requirements.txt
└── README.md
```

## Tech stack
Python, pandas, openpyxl, GitHub Actions

## How to run
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt
python generate_sample_data.py   # optional: only if you have no data yet
python pipeline.py
```
The Excel report appears in `output/kpi_report.xlsx`.

To use your own data, put your CSV in `data/raw/` and update the CONFIG section at the top of `pipeline.py`.

## Scheduling
**GitHub Actions:** the workflow in `.github/workflows/pipeline.yml` runs daily at 06:00 UTC. You can also trigger it manually from the *Actions* tab and download the report from the run's *Artifacts*.

**Windows Task Scheduler:**
1. Open Task Scheduler and choose *Create Basic Task*.
2. Set a trigger (e.g. Daily).
3. Action: *Start a program* and select `run_pipeline.bat`.

## Report
The 2-page executive summary (key findings, dashboard, top 5 insights, 3 recommendations) is in `docs/final_report.pdf`.

## Author
**Your Name**: [LinkedIn](https://www.linkedin.com/in/your-profile) | [GitHub](https://github.com/your-username)

Version: v1.0.0
