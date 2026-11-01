"""Integration tests for HTML report generation."""

import pandas as pd
from src.profiler import DatasetProfiler
from src.reporter import generate_html_report, save_html_report


def test_html_report_rendering(tmp_path):
    df = pd.DataFrame({
        "age": [25, 30, 35, 40],
        "department": ["Eng", "Sales", "Eng", "HR"],
    })

    profiler = DatasetProfiler()
    profile = profiler.profile_dataframe(df)

    html = generate_html_report(profile, "Employees")

    assert "Exploratory Data Analysis Report" in html
    assert "Employees" in html
    assert "Total Records" in html
    assert "age" in html
    assert "department" in html

    out_file = tmp_path / "test_report.html"
    saved_path = save_html_report(profile, out_file, "Employees")

    assert saved_path.exists()
    assert len(saved_path.read_text(encoding="utf-8")) > 500
