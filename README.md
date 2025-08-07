<div align="center">

# ATLAS EXPLORER Python Library

Accelerate analysis of Atlas simulation experiments: run workloads, collect reports, derive KPIs, compare against baselines, and export shareable artifacts.

</div>

---

## 📌 Table of Contents
1. Quick Start
2. Key Features
3. Installation & Environments
4. Configuration (Credentials & API Version)
5. Running Experiments
6. Reporting & KPIs (`atlasexplorer-report`)
7. Derived Metrics & Threshold Status
8. Exporting Reports (JSON / Markdown / HTML / Rich HTML / ZIP)
9. Common Workflows
10. Project Layout
11. Development & Testing
12. Troubleshooting
13. Extending (New Metrics / Thresholds)
14. Glossary

---

## 🚀 1. Quick Start

```bash
git clone https://github.com/MIPS/mips-ae-pylib.git
cd mips-ae-pylib
uv venv
source .venv/bin/activate   # macOS/Linux
uv pip install -e .[reporting]
uv run atlasexplorer/atlasexplorer.py configure   # set credentials interactively
uv run examples/ae_singlecore.py --elf resources/mandelbrot_rv64_O0.elf --channel development --core "I8500_(1_thread)"

# After experiment completes, generate a report (summary.json inside experiment dir)
atlasexplorer-report "myexperiments/<run>/I8500_*/reports/summary/summary.json" --export rich-html --out report.html
```

---

## ⭐ 2. Key Features

| Area | Capability |
|------|------------|
| Experiment Orchestration | Run single or multi-core simulations via example scripts |
| Parsing | Normalize `summary.json` into typed Pydantic models |
| Derived Metrics | CPI, Branch Accuracy, Cache/DTLB Miss Rates, Bond Success %, Thread Balance %, ALU/FPU Mix % |
| Threshold Evaluation | Color-coded statuses (green / yellow / red / n/a) via regex rules |
| Baseline Comparison | Show absolute or percent deltas vs. a reference report |
| CLI Rendering | Category tables + KPI set with Rich formatting |
| Export Formats | JSON, Markdown, compact HTML, Rich HTML (interactive charts), ZIP bundle |
| Extensibility | Add new derived metrics with a straightforward decorator registry |
| Environment Management | First-class support for `uv` environments |

---

## 🛠️ 3. Installation & Environments

Prerequisites:
- Python 3.12
- Git
- [`uv`](https://github.com/astral-sh/uv) (recommended)

### Base Install
```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Optional Extras
| Extra | Enables |
|-------|---------|
| reporting | Rich CLI reporting & exports |
| notebook | Jupyter / exploratory notebooks |

Install with extras:
```bash
uv pip install -e .[reporting,notebook]
```

> You do NOT need `requirements.txt`. Dependencies are defined in `pyproject.toml`.

---

## 🔐 4. Configuration (Credentials & API Version)

### Credentials
Interactive (creates user config + `.env`):
```bash
uv run atlasexplorer/atlasexplorer.py configure
```
Manual:
```bash
export MIPS_ATLAS_CONFIG=<apikey>:<channel>:<region>
```

### API Extension Version
Override if testing a new backend release:
```env
API_EXT_VERSION=0.0.97
```
Place in `.env` or export in shell. If unset, internal default applies.

### Where Things Live
| Item | Path |
|------|------|
| `.env` | Project root (optional) |
| User config | `$HOME/.config/mips/atlaspy/config.json` (Linux/macOS) |

---

## 🧪 5. Running Experiments

Single-core example:
```bash
uv run examples/ae_singlecore.py --elf resources/mandelbrot_rv64_O0.elf --channel development --core "I8500_(1_thread)" --expdir myexperiments
```

Multi-core example:
```bash
uv run examples/ae_multicore.py --elf resources/mandelbrot_rv64_O0.elf resources/memcpy_rv64.elf --channel development --core "I8500_(2_threads)" --expdir myexperiments
```

Outputs appear under `myexperiments/<timestamped_run>/` including `reports/summary/summary.json`.

---

## 📊 6. Reporting & KPIs (`atlasexplorer-report`)

The reporting CLI consumes a generated `summary.json` and optionally a baseline.

Basic usage:
```bash
atlasexplorer-report "path/to/summary.json"
```

With baseline comparison (absolute deltas):
```bash
atlasexplorer-report "new_run/summary.json" --baseline "baseline_run/summary.json"
```

Percent deltas instead:
```bash
atlasexplorer-report "new_run/summary.json" --baseline "baseline_run/summary.json" --percent-delta
```

Limit to specific categories:
```bash
atlasexplorer-report "summary.json" --categories performance cache branch
```

KPIs only (no category breakdown tables):
```bash
atlasexplorer-report "summary.json" --kpi-only
```

### Export Formats
Append an export flag to write artifacts:
```bash
atlasexplorer-report "summary.json" --export json --out report.json
atlasexplorer-report "summary.json" --export markdown --out report.md
atlasexplorer-report "summary.json" --export html --out report.html         # Minimal
atlasexplorer-report "summary.json" --export rich-html --out rich.html      # Interactive charts
atlasexplorer-report "summary.json" --export zip --out bundle.zip           # Pack multiple assets
```
Multiple exports at once:
```bash
atlasexplorer-report "summary.json" --export json markdown rich-html --out outdir/
```
If `--out` points to a directory, filenames are auto-generated.

---

## 🧮 7. Derived Metrics & Threshold Status

Derived metrics are computed post-parse using dependency formulas:

| Metric | Formula (Conceptual) |
|--------|----------------------|
| CPI | Total Cycles / Instructions |
| Branch Prediction Accuracy % | (1 - Mispredicts / Predictions) * 100 |
| ICache / DCache / DTLB Miss Rate % | Misses / (Hits + Misses) * 100 |
| Load / Store Bond Success % | Good / (Good + Bad) * 100 |
| Thread Balance % | abs(T0 - T1) / avg(T0, T1) * 100 (lower is better) |
| ALU / FPU Instruction Mix % | Component / Total * 100 |

Status coloring (green / yellow / red / n/a) is applied via regex-matched rules. Example defaults:
| Pattern | Direction | Green | Yellow |
|---------|-----------|-------|--------|
| Branch Prediction Accuracy % | higher | >=97 | >=90 |
| ICache/DCache Miss Rate % | lower | <=5 | <=10 |
| DTLB Miss Rate % | lower | <=0.1 | <=0.5 |
| CPI | lower | <=1.0 | <=2.0 |
| Load/Store Bond Success % | higher | >=95 | >=85 |
| Thread Balance % | lower | <=5 | <=15 |

Legend is printed below tables in CLI output.

---

## 📦 8. Exporting Reports

| Format | Use Case |
|--------|----------|
| JSON | Programmatic pipelines / dashboards |
| Markdown | Lightweight sharing (wikis, PRs) |
| HTML | Single-file snapshot without JS heavy charts |
| Rich HTML | Interactive charts (Plotly) + KPI grid |
| ZIP | Bundle raw JSON + rich HTML + markdown together |

Rich HTML currently includes a KPI grid, execution mix pie, and branch accuracy gauge (conditional on available data).
```bash
atlasexplorer-report "new_run/summary.json" --baseline "baseline_run/summary.json"
```
## 🔁 9. Common Workflows

1. Run a single-core experiment → Inspect KPI table.
2. Run an optimized build → Compare against baseline with `--percent-delta`.
3. Export rich HTML + JSON for sharing with teammates.
4. Track regressions in CI: keep a golden baseline and diff each run.
5. Extend metrics: add a new derived function and rebuild.

Example baseline diff (percent):
```bash
atlasexplorer-report "run_opt/reports/summary/summary.json" \
      --baseline "run_ref/reports/summary/summary.json" \
      --percent-delta --export rich-html --out compare.html
```

---

## 🗂️ 10. Project Layout

```
atlasexplorer/                 # Core + reporting subpackage
      reporting/                   # Reporting modules
            derive.py                  # Derived metric registry
            parser.py                  # summary.json parser
            thresholds.py              # Status rule application
            render_cli.py              # Rich console rendering
            export.py                  # Export helpers
examples/                      # Example orchestration scripts
resources/                     # Sample ELF binaries
tests/                         # Pytest suite (includes reporting tests)
myexperiments/                 # (Generated) experiment output trees
```

---

## 🧑‍💻 11. Development & Testing

Editable install with reporting extras:
```bash
uv pip install -e .[reporting]
```

Run tests:
```bash
pytest -q
```

Add a new derived metric (example):
```python
# In atlasexplorer/reporting/derive.py
from .derive import derived_metric

@derived_metric("Foo Rate %", ["Foo Hits", "Foo Misses"], "miss/(hit+miss)*100")
def derive_foo(values):
      hits, misses = values
      total = hits + misses
      return (misses / total) * 100 if total else None

> Always wrap summary file paths in quotes, especially if the experiment directory name contains parentheses, spaces, or shell glob characters (e.g. `"I8500_(2_threads)_.../summary.json"`).
```

---

## 🛠️ 12. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `atlasexplorer-report: command not found` | Extras not installed | `uv pip install -e .[reporting]` |
| ImportError (pydantic) | Wrong env active | Activate `.venv` or recreate with `uv venv` |
| No color output | Terminal lacks color or `TERM=dumb` | Use a modern terminal / unset restrictive TERM |
| API auth failure | Missing/invalid `MIPS_ATLAS_CONFIG` | Re-run configure or export correct variable |
| Missing baseline deltas | Forgot `--baseline` flag | Add baseline path |
| Percent delta all `inf` | Baseline metric zero | Use absolute delta or adjust baseline |

---

## 🧩 13. Extending (Thresholds / Rules)

Add a tighter CPI rule (example):
```python
from atlasexplorer.reporting.thresholds import ThresholdRule, apply_thresholds

extra = [ThresholdRule(r'^CPI$', 'lower', green=0.9, yellow=1.5, description='Stricter CPI target')]
report = apply_thresholds(report, extra=extra)
```

You can also fork `DEFAULT_RULES` to adjust globally.

---

## 📘 14. Glossary
| Term | Meaning |
|------|---------|
| CPI | Cycles Per Instruction |
| Bond Success | Ratio of good load/store bonds over total bonds |
| Thread Balance % | Load skew between threads (lower ⇒ more balanced) |
| Mix % | Percentage of instructions executed on a unit class (ALU/FPU) |
| Baseline | Reference run used for comparison |

---

## 🤝 Contributing
1. Create feature branch: `git checkout -b feature/<name>`
2. Implement & add/adjust tests.
3. Run `pytest -q` until green.
4. Submit PR with concise description & screenshots (if UI/CLI impacts).

---

## 📄 License
Provided under the project’s LICENSE (see repository root). (Add details if missing.)

---

## ✅ Junior Developer Checklist
- [ ] Cloned repo & created virtual env
- [ ] Installed with `[reporting]` extra
- [ ] Configured credentials (`configure` command)
- [ ] Ran a sample experiment
- [ ] Generated a rich HTML report
- [ ] Compared against a baseline
- [ ] Read through derived metrics list
- [ ] Ran test suite successfully

You’re productive once all boxes are checked!

---

Need something not covered here? Open an issue or start a discussion.

