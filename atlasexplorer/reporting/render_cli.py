from __future__ import annotations
from .models import SummaryReportModel
from typing import Iterable, Dict, Optional

try:
    from rich.table import Table
    from rich.console import Console
except ImportError:  # fallback minimal
    Table = None
    Console = None

KPI_KEYS = [
    "Total Cycles Consumed",
    "Total Instructions Retired (All Threads)",
    "Instructions Per Cycle (IPC)",
    "CPI",
    "Branch Prediction Accuracy %",
]

def render_kpis(report: SummaryReportModel):
    if Table is None:
        for k in KPI_KEYS:
            m = report.get_metric(k)
            if m:
                print(f"{k}: {m.value}")
        return
    table = Table(title="Key Performance Indicators")
    table.add_column("Metric")
    table.add_column("Value")
    for k in KPI_KEYS:
        m = report.get_metric(k)
        if m:
            val = f"{m.value:.4f}" if isinstance(m.value, float) else str(m.value)
            table.add_row(k, val)
    console = Console()
    console.print(table)


STATUS_STYLES = {
    'green': 'green',
    'yellow': 'yellow',
    'red': 'red',
    'na': 'dim'
}

def _fmt_val(v):
    if v is None:
        return 'NA'
    if isinstance(v, float):
        if abs(v) >= 1000:
            return f"{v:,.0f}"
        return f"{v:.4g}"
    return str(v)

def render_category_tables(report: SummaryReportModel, categories: Iterable[str] | None = None, baseline: Optional[Dict[str,float]] = None, show_percent: bool = False):
    if Table is None:
        return
    console = Console()
    cats: Dict[str, list] = {}
    for m in report.metrics:
        cats.setdefault(m.category, []).append(m)
    for cat, metrics in cats.items():
        if categories and cat not in categories:
            continue
        t = Table(title=f"Category: {cat}")
        t.add_column("Metric")
        if baseline:
            t.add_column("Base")
        t.add_column("Value")
        if baseline:
            t.add_column("Δ%" if show_percent else "Δ")
        t.add_column("Status")
        for m in metrics:
            base_val = baseline.get(m.name) if baseline else None
            delta_str = ''
            if baseline and base_val is not None and m.value is not None:
                if show_percent and base_val != 0:
                    delta = (m.value - base_val) / base_val * 100
                    delta_str = f"{delta:+.2f}%"
                else:
                    delta = m.value - base_val
                    delta_str = f"{delta:+.4g}" if isinstance(delta, float) else str(delta)
            row = [m.name]
            if baseline:
                row.append(_fmt_val(base_val))
            row.append(_fmt_val(m.value))
            if baseline:
                row.append(delta_str)
            row.append(m.status or '')
            style = STATUS_STYLES.get(m.status or 'na', '')
            t.add_row(*row, style=style)
        console.print(t)

def render_legend():
    if Table is None:
        return
    console = Console()
    table = Table(title="Status Legend")
    table.add_column("Status")
    table.add_column("Meaning")
    table.add_row("green", "Optimal", style=STATUS_STYLES['green'])
    table.add_row("yellow", "Warning", style=STATUS_STYLES['yellow'])
    table.add_row("red", "Attention", style=STATUS_STYLES['red'])
    table.add_row("na", "N/A", style=STATUS_STYLES['na'])
    console.print(table)
