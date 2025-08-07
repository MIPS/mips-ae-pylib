"""
ATLAS Explorer Multicore Experiment + Baseline Diff Report Example

This script runs a multicore experiment, then (optionally) compares the produced
summary.json against a provided baseline summary.json, generating a ZIP bundle
containing:
  - Raw parsed & derived metrics JSON
  - Markdown report
  - Rich HTML report (interactive)
  - Baseline vs new deltas in tables

Usage:
    uv run examples/ae_multicore_diff_report.py \
        --elf resources/mandelbrot_rv64_O0.elf resources/memcpy_rv64.elf \
        --channel development --core "I8500_(2_threads)" \
        --bundle-out diff_bundle.zip \
        --baseline "path/to/baseline/summary.json"

If --baseline is omitted, the bundle is still produced without deltas.

Note: Always quote paths to summary.json files (baseline or produced) because
experiment directory names may contain parentheses or spaces.
"""
import argparse
import locale
import os
import sys
import tempfile
import zipfile
from pathlib import Path
from dotenv import load_dotenv

from atlasexplorer.atlasexplorer import AtlasExplorer, Experiment
from atlasexplorer.reporting.parser import parse_summary_json
from atlasexplorer.reporting.derive import apply_derivations
from atlasexplorer.reporting.thresholds import apply_thresholds
from atlasexplorer.reporting.export import export_json, export_markdown, export_rich_html

# Load environment variables from .env file
load_dotenv()

def run_experiment(args) -> Path:
    aeinst = AtlasExplorer(
        args.apikey,
        args.channel,
        args.region,
        verbose=args.verbose,
    )
    experiment = Experiment(args.expdir, aeinst, verbose=args.verbose)
    for elf_path in args.elf:
        experiment.addWorkload(os.path.abspath(elf_path))
    experiment.setCore(args.core)
    experiment.run()
    # After run, summary path should exist inside experiment directory tree.
    # We locate the newest summary.json under the experiment directory.
    exp_path = Path(args.expdir)
    summary_candidates = list(exp_path.rglob('summary/summary.json'))
    if not summary_candidates:
        print("No summary.json found under experiment directory.", file=sys.stderr)
        sys.exit(2)
    # Pick the most recently modified summary file (in case multiple runs)
    summary_candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return summary_candidates[0]

def build_report(main_summary: Path, baseline_path: Path | None, bundle_out: Path):
    # Parse & derive for main report
    report = parse_summary_json(str(main_summary))
    report = apply_derivations(report)
    report = apply_thresholds(report)

    baseline_report = None
    if baseline_path:
        baseline_report = parse_summary_json(str(baseline_path))
        baseline_report = apply_derivations(baseline_report)

    # Prepare an output temp directory for individual artifacts before zipping
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        # Export raw JSON (includes derived metrics)
        json_path = tmpdir_path / 'report.json'
        export_json(report, json_path)
        # Markdown summary
        md_path = tmpdir_path / 'report.md'
        export_markdown(report, md_path)
        # Rich HTML (interactive)
        rich_path = tmpdir_path / 'report_rich.html'
        export_rich_html(report, rich_path)

        # If baseline provided, generate an additional markdown diff snippet
        if baseline_report:
            # Build a simple delta table (name, new, baseline, delta, percent)
            lines = ["# Baseline Comparison\n", "| Metric | New | Baseline | Δ | Δ% |", "|--------|----|----------|---|----|"]
            base_map = {m.name: m for m in baseline_report.metrics}
            for m in report.metrics:
                if m.name in base_map and m.value is not None and base_map[m.name].value is not None:
                    new_v = m.value
                    old_v = base_map[m.name].value
                    delta = new_v - old_v
                    pct = (delta / old_v * 100) if old_v not in (0, None) else float('inf')
                    lines.append(f"| {m.name} | {new_v:.4g} | {old_v:.4g} | {delta:+.4g} | {pct:+.2f}% |")
            (tmpdir_path / 'baseline_diff.md').write_text("\n".join(lines))
        # Create bundle (zip) including everything in temp directory (JSON, MD, rich HTML, optional baseline diff)
        with zipfile.ZipFile(bundle_out, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            for f in tmpdir_path.iterdir():
                zf.write(f, arcname=f.name)


def main():
    parser = argparse.ArgumentParser(description="Run multicore experiment and create diff reporting bundle.")
    parser.add_argument("--elf", required=True, nargs='+', help="Path(s) to ELF workload file(s). Multiple allowed.")
    parser.add_argument("--expdir", default="myexperiments", help="Experiment directory (default: myexperiments)")
    parser.add_argument("--core", default="I8500_(2_threads)", help="Core type (default: I8500_(2_threads))")
    parser.add_argument("--channel", default="development", help="Channel (default: development)")
    parser.add_argument("--apikey", help="Your ATLAS Explorer API key.")
    parser.add_argument("--region", help="Region")
    parser.add_argument("--baseline", help="Path to baseline summary.json (quoted)")
    parser.add_argument("--bundle-out", default="diff_bundle.zip", help="Output zip bundle path (default: diff_bundle.zip)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()

    # Configuration existence check
    config_env = os.environ.get("MIPS_ATLAS_CONFIG")
    home_dir = os.path.expanduser("~")
    config_file = os.path.join(home_dir, ".config", "mips", "atlaspy", "config.json")
    if not args.apikey and not config_env and not os.path.exists(config_file):
        print("Atlas Explorer configuration not found.\nRun 'uv run atlasexplorer/atlasexplorer.py configure' first.", file=sys.stderr)
        sys.exit(1)

    locale.setlocale(locale.LC_ALL, "")

    summary_path = run_experiment(args)
    print(f"Produced summary: {summary_path}")

    baseline_path = Path(args.baseline).resolve() if args.baseline else None
    bundle_out = Path(args.bundle_out).resolve()
    build_report(summary_path, baseline_path, bundle_out)
    print(f"Bundle written to: {bundle_out}")

if __name__ == "__main__":
    main()
