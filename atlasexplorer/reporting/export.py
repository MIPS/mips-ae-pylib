from __future__ import annotations
from .models import SummaryReportModel, Metric
from datetime import datetime
import json, html, tempfile, shutil, math
from pathlib import Path
from typing import List, Iterable, Optional
import os
import zipfile

try:
    import plotly.graph_objects as go  # type: ignore
except Exception:  # pragma: no cover - optional
    go = None

HEADER = "# Atlas Explorer Summary Report\n"

def export_json(report: SummaryReportModel, path: str):
    Path(path).write_text(json.dumps(report.to_dict(), indent=2))


def export_markdown(report: SummaryReportModel, path: str):
    lines = [HEADER]
    lines.append(f"Generated: {datetime.utcnow().isoformat()}Z\n")
    kpis = [
        "Total Cycles Consumed",
        "Total Instructions Retired (All Threads)",
        "Instructions Per Cycle (IPC)",
        "CPI",
        "Branch Prediction Accuracy %",
    ]
    lines.append("## KPIs\n")
    for k in kpis:
        m = report.get_metric(k)
        if m:
            lines.append(f"- **{k}**: {m.value}")
    # Categories
    cats = {}
    for m in report.metrics:
        cats.setdefault(m.category, []).append(m)
    for cat, metrics in sorted(cats.items()):
        lines.append(f"\n### {cat}\n")
        for m in metrics:
            val = m.value if m.value is not None else 'NA'
            lines.append(f"- {m.name}: {val}")
    Path(path).write_text("\n".join(lines))


def export_html(report: SummaryReportModel, path: str):
    """Basic HTML export (lightweight, no JS dependencies except static page)."""
    rows = []
    for m in report.metrics:
        val = '' if m.value is None else (f"{m.value:.4g}" if isinstance(m.value, (int, float)) else str(m.value))
        rows.append(f"<tr><td>{html.escape(m.category)}</td><td>{html.escape(m.name)}</td><td class='num'>{html.escape(val)}</td></tr>")
    html_doc = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>Atlas Explorer Report</title>
    <style>
    body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;margin:1.5rem;line-height:1.35}}
    table{{border-collapse:collapse;width:100%;margin-top:1rem}}
    th,td{{border:1px solid #d0d0d0;padding:4px 8px;font-size:13px;vertical-align:top}}
    th{{background:#f6f6f6;text-align:left;position:sticky;top:0;z-index:1}}
    h1{{margin-top:0;font-size:1.6rem}}
    .kpi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-top:1rem}}
    .kpi{{background:#1d3557;color:#fff;padding:10px 12px;border-radius:6px;box-shadow:0 1px 3px rgba(0,0,0,.15)}}
    .kpi span.val{{display:block;font-weight:600;font-size:1.05rem;margin-top:2px;letter-spacing:.5px}}
    .footer{{margin-top:2rem;font-size:11px;color:#666}}
    td.num{{text-align:right;font-variant-numeric:tabular-nums}}
    </style></head>
    <body><h1>Atlas Explorer Summary Report</h1><p>Generated: {html.escape(datetime.utcnow().isoformat())}Z</p>
    {build_kpi_grid(report)}
    <details open><summary><strong>All Metrics</strong></summary>
    <table><thead><tr><th>Category</th><th>Metric</th><th>Value</th></tr></thead><tbody>{''.join(rows)}</tbody></table></details>
    <div class='footer'>Basic HTML export • atlasexplorer-report</div>
    </body></html>"""
    Path(path).write_text(html_doc)


def build_kpi_grid(report: SummaryReportModel) -> str:
    keys = [
        "Total Cycles Consumed",
        "Total Instructions Retired (All Threads)",
        "Instructions Per Cycle (IPC)",
        "CPI",
        "Branch Prediction Accuracy %",
    ]
    blocks = []
    for k in keys:
        m = report.get_metric(k)
        if not m:
            continue
        val = m.value
        if isinstance(val, float):
            if abs(val) >= 1000:
                val_s = f"{val:,.0f}"
            else:
                val_s = f"{val:.4g}"
        else:
            val_s = str(val)
        blocks.append(f"<div class='kpi'><div>{html.escape(k)}</div><span class='val'>{html.escape(val_s)}</span></div>")
    return f"<div class='kpi-grid'>{''.join(blocks)}</div>"


def export_rich_html(report: SummaryReportModel, path: str):
    """Richer HTML with embedded Plotly charts (if Plotly available)."""
    charts_html = ""
    if go:
        # Build instruction mix if available
        inst_keys = [
            "Instructions Executed on ALU 0",
            "Instructions Executed on ALU 1",
            "Instrution Executed on FPU 0",
            "Instrution Executed on FPU 1",
        ]
        values = []
        labels = []
        total = 0
        for k in inst_keys:
            m = report.get_metric(k)
            if m and m.value:
                values.append(m.value)
                labels.append(k.replace('Instructions Executed on ', '').replace('Instrution Executed on ', ''))
                total += m.value
        if values:
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.45)])
            fig.update_layout(margin=dict(l=10,r=10,t=30,b=10), title='Execution Unit Mix')
            charts_html += fig.to_html(full_html=False, include_plotlyjs='cdn')
        # Branch accuracy gauge (simple bar)
        acc = report.get_metric("Branch Prediction Accuracy %")
        if acc and acc.value is not None and go:
            fig2 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=acc.value,
                number={'suffix': '%'},
                gauge={'axis': {'range': [0,100]}, 'bar': {'color': '#1d3557'}},
                title={'text': 'Branch Accuracy'}
            ))
            fig2.update_layout(height=280, margin=dict(l=20,r=20,t=40,b=10))
            charts_html += fig2.to_html(full_html=False, include_plotlyjs=False)
    else:  # pragma: no cover - optional path
        charts_html = "<p><em>Plotly not installed; rich charts unavailable.</em></p>"

    # Reuse basic table but add charts section
    rows = []
    for m in report.metrics:
        val = '' if m.value is None else (f"{m.value:.4g}" if isinstance(m.value, (int, float)) else str(m.value))
        rows.append(f"<tr><td>{html.escape(m.category)}</td><td>{html.escape(m.name)}</td><td class='num'>{html.escape(val)}</td></tr>")
    html_doc = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>Atlas Explorer Report (Rich)</title>
    <style>body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;margin:1.2rem;line-height:1.35}}table{{border-collapse:collapse;width:100%;margin-top:1rem}}th,td{{border:1px solid #d0d0d0;padding:4px 6px;font-size:12.5px}}th{{background:#f5f7fa}}.flex{{display:flex;flex-wrap:wrap;gap:22px;margin-top:1rem}}.panel{{flex:1 1 320px;min-width:300px;background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:12px;box-shadow:0 1px 2px rgba(0,0,0,.06)}}h1{{margin:.2rem 0 0.6rem;font-size:1.55rem}}.kpi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}}.kpi{{background:#1d3557;color:#fff;padding:8px 10px;border-radius:6px}}.kpi span.val{{display:block;font-weight:600;font-size:1.05rem;margin-top:4px}}td.num{{text-align:right;font-variant-numeric:tabular-nums}}footer{{margin-top:2rem;font-size:11px;color:#666}}</style></head>
    <body><h1>Atlas Explorer Summary Report (Rich)</h1><p>Generated: {html.escape(datetime.utcnow().isoformat())}Z</p>
    {build_kpi_grid(report)}
    <div class='flex'>
      <div class='panel'>{charts_html}</div>
      <div class='panel'><strong>All Metrics</strong><table><thead><tr><th>Category</th><th>Metric</th><th>Value</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
    </div>
    <footer>Rich HTML export • atlasexplorer-report</footer>
    </body></html>"""
    Path(path).write_text(html_doc)


def export_zip(report: SummaryReportModel, zip_path: str, rich: bool = True):
    """Create a zip bundle with JSON, Markdown, and HTML variants.

    Args:
        report: model
        zip_path: output zip file path
        rich: include rich HTML (else basic)
    """
    tmpdir = Path(tempfile.mkdtemp(prefix="atlasexp_"))
    try:
        export_json(report, str(tmpdir / 'report.json'))
        export_markdown(report, str(tmpdir / 'report.md'))
        if rich:
            export_rich_html(report, str(tmpdir / 'report.html'))
        else:
            export_html(report, str(tmpdir / 'report.html'))
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            for f in tmpdir.iterdir():
                zf.write(f, arcname=f.name)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
