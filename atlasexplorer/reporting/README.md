# Atlas Explorer — Reporting (Junior-Friendly Guide)

This folder turns raw Atlas Explorer JSON into readable reports.

You can:
- Parse the simulator output (summary.json)
- Add derived metrics (like CPI)
- Classify metrics with green/yellow/red thresholds
- Render nice terminal tables
- Export Markdown/HTML/ZIP bundles

The flow is simple:

summary.json → parser → derivations → thresholds → render/export

---

## Quick start

1) Get a summary.json path from your experiment run.

2) Run the CLI to view KPIs and categories in your terminal:

```bash
atlasexplorer-report path/to/summary.json
```

3) Compare to a baseline and export:

```bash
atlasexplorer-report path/to/summary.json \
  --baseline path/to/baseline/summary.json \
  --percent-delta \
  --export-md report.md \
  --export-html report_basic.html \
  --export-rich-html report_rich.html \
  --export-zip report_bundle.zip
```

Notes:
- The rich HTML uses Plotly for charts. If Plotly isn’t installed, it still works—just without charts.
- You can filter categories in the terminal output:

```bash
atlasexplorer-report path/to/summary.json --categories core_summary branch
```

---

## What each module does (and how to use it)

### 1) parser.py — Read and categorize metrics

- Function: `parse_summary_json(path)`
  - Reads `summary.json` from a run.
  - Converts raw payloads into `Metric` objects and returns a `SummaryReportModel`.
  - Assigns each metric to a category using simple regex rules.

- Categories are defined in `CATEGORY_RULES` (a list of regex → category mappings). Examples:
  - Core summary (cycles, instructions, IPC/CPI)
  - Thread summary (Thread 0/1 metrics)
  - Branch, caches/TLBs, bonding, execution mix, stalls, other

Tips:
- To re-categorize a metric, add/adjust a regex in `CATEGORY_RULES`.
- Only touch the patterns you need; keep them short and readable.


### 2) models.py — Data shapes

- `Metric` — a single metric with:
  - `name`, `value` (float or None), `raw_value` (original), `category`
  - Optional: `thread`, `unit`, `description`, `status` (green/yellow/red/na)
  - Flags: `derived` and `formula` for derived metrics

- `SummaryReportModel` — list of `Metric` plus optional `metadata/siminfo`.
  - Helper: `get_metric(name)` to fetch a metric by name.

- `RawMetric` — helper for parsing raw JSON values safely.

You don’t need to memorize these—just know that everything becomes a `SummaryReportModel` with `metrics` you can loop over.


### 3) derive.py — Add derived metrics

- Register a derived metric with the `@derived_metric` decorator:

```python
@derived_metric("CPI", ["Total Cycles Consumed", "Total Instructions Retired (All Threads)"], "cycles / instructions")
def derive_cpi(values):
    cycles, instr = values
    return cycles / instr if instr else None
```

- Function: `apply_derivations(report)`
  - Looks up dependencies by name and computes new metrics.
  - Skips anything that is missing or invalid.

Built-in examples:
- CPI
- Branch Prediction Accuracy %
- I/D Cache / DTLB miss rates
- Load/Store Bond success %
- Thread Balance %
- ALU/FPU Instruction Mix %

Add new derived metrics by:
1) Defining a function with `@derived_metric` (give it a friendly name, deps, and a short formula string)
2) Returning a number or `None` when undefined (divide-by-zero, missing deps, etc.)


### 4) thresholds.py — Green/Yellow/Red status

- Class: `ThresholdRule(pattern, direction, green, yellow, description)`
  - `pattern`: regex to match metric names
  - `direction`: `'higher'` or `'lower'` is better
  - Values at/above `green` (for higher-is-better) are green; between yellow and green are yellow; below yellow are red. The inverse applies to lower-is-better.

- Function: `apply_thresholds(report, extra=None)`
  - Applies `DEFAULT_RULES` plus any extra rules you pass in.

Defaults include:
- Branch Accuracy %, CPI, I/D Cache miss %, DTLB miss %, Load/Store Bond %, Thread Balance %

Add a rule by appending to `DEFAULT_RULES` or passing `extra` at call time. Keep ranges realistic and document units if needed.


### 5) render_cli.py — Pretty terminal output

- Uses `rich` for tables (falls back to plain text if `rich` isn’t installed).
- `render_kpis(report)` — prints a compact KPI table.
- `render_category_tables(report, categories=None, baseline=None, show_percent=False)`
  - Shows per-category tables
  - Optional baseline column and Δ/Δ% column
- `render_legend()` — status legend table

Use these helpers in your own scripts to keep output consistent.


### 6) export.py — Save reports to files

- `export_json(report, path)` — full report model as JSON
- `export_markdown(report, path)` — human-readable Markdown
- `export_html(report, path)` — lightweight HTML (no JS)
- `export_rich_html(report, path)` — richer HTML with charts (needs Plotly)
- `export_zip(report, path)` — bundle with JSON + Markdown + both HTML flavors

All exporters accept a `SummaryReportModel`. The rich HTML will add charts like execution-unit mix and a branch-accuracy gauge when data is present and Plotly is installed.


### 7) cli.py — The glue (command-line tool)

- Command: `atlasexplorer-report`
- Arguments:
  - `summary_json` — path to the run’s `summary.json`
  - `--baseline PATH` — optional baseline `summary.json`
  - `--percent-delta` — show % deltas instead of absolute
  - `--kpi-only` — just the KPI table
  - `--categories ...` — filter category list
  - Export flags: `--export-json`, `--export-md`, `--export-html`, `--export-rich-html`, `--export-zip`

Under the hood it:
1) Parses the summary
2) Applies derivations
3) Applies thresholds
4) Renders to terminal
5) Saves any requested exports

---

## Common tasks (copy/paste friendly)

- Show only KPIs:

```bash
atlasexplorer-report path/to/summary.json --kpi-only
```

- Show only branch and memory categories with percent deltas vs baseline:

```bash
atlasexplorer-report path/to/summary.json \
  --baseline path/to/baseline/summary.json \
  --percent-delta \
  --categories branch data_mem
```

- Produce a ZIP bundle for sharing:

```bash
atlasexplorer-report path/to/summary.json --export-zip diff_bundle.zip
```

---

## Extending the reporting pipeline

- New category rule: edit `CATEGORY_RULES` in `parser.py`.
- New derived metric: use `@derived_metric` in `derive.py`; keep names friendly and formulas short.
- New threshold: add a `ThresholdRule` to `DEFAULT_RULES` in `thresholds.py`.
- New export: add a function to `export.py` and wire it in `cli.py`.

Rule of thumb: small, readable additions with clear names and short regexes.

---

## Troubleshooting

- “Value shows NA” — the input was missing, not numeric, or a derived metric had invalid inputs (e.g., divide-by-zero). That’s OK.
- “Charts don’t show” — install Plotly or use the basic HTML export.
- “A metric landed in ‘other’” — add/update a regex in `CATEGORY_RULES`.

---

## Where to look in this repo

- Sample experiment reports: `atlas-explorer-experiments/.../reports/summary/summary.json`
- A prebuilt diff bundle example: `diff_bundle/` (JSON/Markdown/HTML)
- Tests to learn patterns: `tests/reporting/`

---

## Keep it maintainable

- Prefer tiny functions and short regexes
- Add small, well-named derived metrics instead of giant formulas
- Document thresholds (units and intent)
- Keep exports minimal and fast by default

You’ve got this—iterate in small steps and run the CLI to see results fast.
