"""HTML Report generator for EDA dataset profiles."""

from __future__ import annotations

from pathlib import Path
from src.profiler import DatasetProfile


def generate_html_report(profile: DatasetProfile, dataset_name: str = "Dataset") -> str:
    """Renders a self-contained HTML exploratory analysis dashboard."""
    total_missing = sum(v["missing_count"] for v in profile.missing_summary.values())

    # Build Numeric Rows HTML
    numeric_rows = []
    for col, stats in profile.numeric_columns.items():
        numeric_rows.append(f"""
        <tr>
            <td><strong>{col}</strong></td>
            <td>{stats['mean']}</td>
            <td>{stats['std']}</td>
            <td>{stats['min']}</td>
            <td>{stats['q25']}</td>
            <td>{stats['median']}</td>
            <td>{stats['q75']}</td>
            <td>{stats['max']}</td>
            <td>{stats['skewness']}</td>
        </tr>""")
    numeric_table_html = "\n".join(numeric_rows) if numeric_rows else "<tr><td colspan='9'>No numeric columns found.</td></tr>"

    # Build Categorical Rows HTML
    cat_rows = []
    for col, stats in profile.categorical_columns.items():
        cat_rows.append(f"""
        <tr>
            <td><strong>{col}</strong></td>
            <td>{stats['unique']}</td>
            <td>{stats['top']}</td>
            <td>{stats['top_freq']}</td>
        </tr>""")
    cat_table_html = "\n".join(cat_rows) if cat_rows else "<tr><td colspan='4'>No categorical columns found.</td></tr>"

    # Build Missing Rows HTML
    missing_rows = []
    for col, stats in profile.missing_summary.items():
        bar_width = min(100, stats['missing_pct'])
        missing_rows.append(f"""
        <tr>
            <td><strong>{col}</strong></td>
            <td>{stats['dtype']}</td>
            <td>{stats['missing_count']}</td>
            <td>{stats['missing_pct']}%</td>
            <td>
                <div style="background:#334155; border-radius:4px; height:8px; width:100px;">
                    <div style="background:#ef4444; border-radius:4px; height:8px; width:{bar_width}px;"></div>
                </div>
            </td>
        </tr>""")
    missing_table_html = "\n".join(missing_rows)

    # Build Collinear Pairs HTML
    collinear_items = []
    for c1, c2, r in profile.collinear_pairs:
        collinear_items.append(f"<li><strong>{c1}</strong> &harr; <strong>{c2}</strong> (Pearson <em>r = {r}</em>)</li>")
    collinear_html = "<ul>" + "\n".join(collinear_items) + "</ul>" if collinear_items else "<p>No highly collinear feature pairs (|r| &ge; 0.80) detected.</p>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EDA Profile Report | {dataset_name}</title>
    <style>
        :root {{
            --bg: #0f172a;
            --surface: #1e293b;
            --border: #334155;
            --text: #f8fafc;
            --muted: #94a3b8;
            --accent: #38bdf8;
            --danger: #ef4444;
            --success: #22c55e;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            padding: 2rem;
            line-height: 1.5;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        header {{ margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 1rem; }}
        h1 {{ font-size: 2rem; margin-bottom: 0.25rem; }}
        .subtitle {{ color: var(--muted); font-size: 1rem; }}
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .kpi-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.25rem;
            text-align: center;
        }}
        .kpi-title {{ font-size: 0.85rem; color: var(--muted); text-transform: uppercase; margin-bottom: 0.5rem; }}
        .kpi-value {{ font-size: 1.8rem; font-weight: 700; color: var(--accent); }}

        section {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }}
        h2 {{ font-size: 1.3rem; margin-bottom: 1rem; color: var(--accent); }}
        
        table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; text-align: left; }}
        th, td {{ padding: 0.75rem; border-bottom: 1px solid var(--border); }}
        th {{ color: var(--muted); font-weight: 600; text-transform: uppercase; font-size: 0.75rem; }}
        tr:hover {{ background: rgba(255, 255, 255, 0.02); }}

        ul {{ padding-left: 1.5rem; }}
        li {{ margin-bottom: 0.5rem; }}
        footer {{ text-align: center; color: var(--muted); font-size: 0.85rem; margin-top: 3rem; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Exploratory Data Analysis Report</h1>
            <p class="subtitle">Dataset: <strong>{dataset_name}</strong> &bull; Generated by <a href="https://github.com/piyush1008-cyber/eda-insights-toolkit" style="color:var(--accent);">eda-insights-toolkit</a></p>
        </header>

        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Total Records</div>
                <div class="kpi-value">{profile.row_count:,}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Total Features</div>
                <div class="kpi-value">{profile.col_count}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Memory Footprint</div>
                <div class="kpi-value">{profile.memory_kb} KB</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Duplicate Rows</div>
                <div class="kpi-value">{profile.duplicated_rows}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Missing Cells</div>
                <div class="kpi-value">{total_missing}</div>
            </div>
        </div>

        <section>
            <h2>Numerical Feature Statistics</h2>
            <table>
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>Mean</th>
                        <th>Std</th>
                        <th>Min</th>
                        <th>25%</th>
                        <th>Median</th>
                        <th>75%</th>
                        <th>Max</th>
                        <th>Skewness</th>
                    </tr>
                </thead>
                <tbody>
                    {numeric_table_html}
                </tbody>
            </table>
        </section>

        <section>
            <h2>Categorical Feature Summary</h2>
            <table>
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>Distinct Values</th>
                        <th>Top Value</th>
                        <th>Frequency</th>
                    </tr>
                </thead>
                <tbody>
                    {cat_table_html}
                </tbody>
            </table>
        </section>

        <section>
            <h2>Missing Values & Data Types</h2>
            <table>
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>Data Type</th>
                        <th>Missing Count</th>
                        <th>Missing %</th>
                        <th>Distribution</th>
                    </tr>
                </thead>
                <tbody>
                    {missing_table_html}
                </tbody>
            </table>
        </section>

        <section>
            <h2>Multicollinearity & Feature Correlation (|r| &ge; 0.80)</h2>
            {collinear_html}
        </section>

        <footer>
            &copy; 2026 Piyush Kangle. Built for automated machine learning preprocessing and data diagnostics.
        </footer>
    </div>
</body>
</html>
"""
    return html


def save_html_report(profile: DatasetProfile, output_path: Path | str, dataset_name: str = "Dataset") -> Path:
    """Writes rendered HTML report to file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = generate_html_report(profile, dataset_name=dataset_name)
    path.write_text(content, encoding="utf-8")
    return path
