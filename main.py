"""Command-line interface for the EDA Insights Toolkit."""

import argparse
import sys
from pathlib import Path
import pandas as pd
from src.profiler import DatasetProfiler
from src.reporter import save_html_report
from samples.generate_sample_dataset import generate_sample_csv


def print_banner():
    banner = """
===================================================================
     EDA INSIGHTS TOOLKIT - Automated Data Profiler & Dashboard    
===================================================================
    """
    print(banner)


def display_console_summary(profile, dataset_name: str):
    print("\n" + "=" * 65)
    print(f"               EDA SUMMARY: {dataset_name.upper()}               ")
    print("=" * 65)
    print(f"Total Rows:            {profile.row_count:,}")
    print(f"Total Features:        {profile.col_count}")
    print(f"Memory Footprint:      {profile.memory_kb} KB")
    print(f"Duplicated Rows:       {profile.duplicated_rows}")
    print(f"Numeric Columns:       {len(profile.numeric_columns)}")
    print(f"Categorical Columns:   {len(profile.categorical_columns)}")

    print("\n--- Missingness Overview ---")
    has_missing = False
    for col, meta in profile.missing_summary.items():
        if meta['missing_count'] > 0:
            has_missing = True
            print(f"  {col:<25} : {meta['missing_count']:>4} nulls ({meta['missing_pct']}%)")
    if not has_missing:
        print("  Clean dataset. Zero missing values detected.")

    if profile.collinear_pairs:
        print("\n--- High Multicollinearity Warning (|r| >= 0.80) ---")
        for c1, c2, r in profile.collinear_pairs:
            print(f"  [!] {c1} <-> {c2} (Pearson r = {r})")
    print("=" * 65 + "\n")


def cmd_profile(args):
    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"Error: File '{csv_path}' not found.")
        sys.exit(1)

    print(f"[*] Ingesting and profiling '{csv_path}'...")
    df = pd.read_csv(csv_path)

    profiler = DatasetProfiler(collinear_threshold=args.threshold)
    profile = profiler.profile_dataframe(df)

    display_console_summary(profile, csv_path.name)

    out_path = Path(args.out)
    save_html_report(profile, out_path, dataset_name=csv_path.name)
    print(f"[+] Interactive HTML dashboard exported to: {out_path.resolve()}")


def cmd_demo(args):
    sample_csv = Path("samples/customers.csv")
    report_html = Path("reports/eda_report.html")

    print("[*] Generating synthetic telecom churn dataset...")
    generate_sample_csv(sample_csv, n_rows=300)

    print(f"[*] Profiling dataset and rendering HTML report...")
    df = pd.read_csv(sample_csv)
    profiler = DatasetProfiler(collinear_threshold=0.80)
    profile = profiler.profile_dataframe(df)

    display_console_summary(profile, "customers.csv")
    save_html_report(profile, report_html, dataset_name="customers.csv")

    assert report_html.exists()
    print(f"[PASS] EDA report successfully generated: {report_html.resolve()}")


def main():
    print_banner()
    parser = argparse.ArgumentParser(description="EDA Insights Toolkit - Automated Data Profiler")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # profile
    p_prof = subparsers.add_parser("profile", help="Profile a CSV dataset and generate HTML dashboard")
    p_prof.add_argument("csv", help="Path to input CSV file")
    p_prof.add_argument("--out", default="report.html", help="Output HTML file path (default: report.html)")
    p_prof.add_argument("--threshold", type=float, default=0.80, help="Collinearity alert threshold (default: 0.80)")
    p_prof.set_defaults(func=cmd_profile)

    # demo
    p_demo = subparsers.add_parser("demo", help="Generate sample dataset and build demo dashboard")
    p_demo.set_defaults(func=cmd_demo)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
