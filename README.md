# EDA Insights Toolkit

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: Pytest](https://img.shields.io/badge/tests-pytest-brightgreen.svg)](https://docs.pytest.org/)
[![Data: Pandas & NumPy](https://img.shields.io/badge/data-Pandas%20%26%20NumPy-orange.svg)](https://pandas.pydata.org/)
[![Reports: Interactive HTML](https://img.shields.io/badge/reports-Interactive%20HTML-blueviolet.svg)](https://github.com/piyush1008-cyber/eda-insights-toolkit)

> **Automated Exploratory Data Analysis (EDA) engine in Python.** Computes comprehensive parametric statistics, data quality metrics, missingness breakdowns, Pearson correlation matrices, and renders self-contained, responsive HTML data visualization dashboards.

---

## Architectural Flow

```mermaid
flowchart LR
    A[Tabular Dataset\nCSV / DataFrame] --> B[Dataset Profiler]
    B --> C[Statistical Analysis\nMean, Std, Quartiles, Skewness]
    B --> D[Categorical Profiler\nCardinality, Modes, Frequencies]
    B --> E[Quality Diagnostics\nMissingness, Null Bars, Duplicates]
    B --> F[Multicollinearity Detector\nPearson r >= 0.80 Matrix]
    C & D & E & F --> G[HTML Dashboard Generator]
    G --> H[Standalone Responsive Report\nreport.html]
```

---

## Key Features

- **Automated Parametric Profiling:** Computes mean, standard deviation, min, 25th percentile, median, 75th percentile, max, and skewness for numeric attributes.
- **Categorical Diagnostics:** Profiles distinct values, high-frequency modes, and distribution frequencies.
- **Data Quality & Missingness Audits:** Highlights missing cells, missing percentages, and duplicate row detection.
- **Multicollinearity Flagging:** Automatically scans numeric correlation matrices to flag redundant pairs ($|r| \ge 0.80$) for feature selection.
- **Zero-Dependency HTML Reporting:** Renders modern, responsive HTML reports with dark mode styling and zero external runtime dependencies.

---

## Quickstart & CLI Commands

### 1. Run Automated Demonstration
```bash
python main.py demo
```
Generates a realistic customer dataset, conducts profiling, and outputs an interactive HTML report to `reports/eda_report.html`.

### 2. Profile an Existing CSV File
```bash
python main.py profile data/train.csv --out dashboard.html --threshold 0.85
```

---

## Running the Test Suite

```bash
pytest -v
```

Unit and integration tests verify:
- Parametric calculations (mean, std, quartiles, skewness)
- Missing value percentage accuracy and duplicate detection
- Collinear feature pair isolation
- HTML template compilation and file export.

---

## Author & License

- **Author:** Piyush Kangle ([@piyush1008-cyber](https://github.com/piyush1008-cyber))
- **Email:** piyushkangle@gmail.com
- **License:** [MIT License](LICENSE)
