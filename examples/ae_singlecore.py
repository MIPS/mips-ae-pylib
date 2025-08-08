"""
ATLAS Explorer Single Core Experiment Example

This script demonstrates how to run a single core experiment using the ATLAS Explorer Python library.

Usage:
    uv run examples/ae_singlecore.py --elf resources/mandelbrot_rv64_O0.elf --channel development --core I8500_(1_thread)

Arguments:
    --elf      Path to the ELF workload file.
    --expdir   Directory to store experiment results (default: myexperiments)
    --core     Core type to use for the experiment (default: I8500_(1_thread))
    --channel  Channel name (default: development)
    --apikey   Your ATLAS Explorer API key (optional if configured)
    --region   Region name (optional if configured)
    --verbose  Enable verbose output for debugging

Configuration:
    You must configure your API key, channel, and region before running experiments.
    - Use 'uv run atlasexplorer/atlasexplorer.py configure' for interactive setup
    - Or set the environment variable: export MIPS_ATLAS_CONFIG=<apikey>:<channel>:<region>

Example:
    uv run examples/ae_singlecore.py --elf resources/mandelbrot_rv64_O0.elf --channel development --core I8500_(1_thread)

"""
import argparse
import locale
import os
import sys
from pathlib import Path
from atlasexplorer.atlasexplorer import AtlasExplorer, Experiment
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Run a single core experiment with ATLAS Explorer.")
    parser.add_argument("--elf", required=True, help="Path to the ELF workload file.")
    parser.add_argument("--expdir", default="myexperiments", help="Experiment directory (default: myexperiments)")
    parser.add_argument("--core", default="I8500_(1_thread)", help="Core type (default: I8500_(1_thread)")
    parser.add_argument("--channel", default="development", help="Channel (default: development)")
    parser.add_argument("--apikey", help="Your ATLAS Explorer API key.")
    parser.add_argument("--region", help="Region")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    parser.add_argument(
        "--export",
        choices=["json", "markdown", "html", "rich-html", "zip"],
        help="Export a report after the run in the given format.",
    )
    parser.add_argument(
        "--out",
        help=(
            "Output path for the exported report. If omitted, a sensible filename is created next to summary.json."
        ),
    )
    args = parser.parse_args()

    # Check for configuration: ENV, config file, or CLI args
    config_env = os.environ.get("MIPS_ATLAS_CONFIG")
    home_dir = os.path.expanduser("~")
    config_file = os.path.join(home_dir, ".config", "mips", "atlaspy", "config.json")
    if not args.apikey and not config_env and not os.path.exists(config_file):
        print("Atlas Explorer configuration not found.")
        print("Please run 'uv run atlasexplorer/atlasexplorer.py configure' before using this script.")
        sys.exit(1)

    # Set locale for pretty printing numbers
    locale.setlocale(locale.LC_ALL, "")

    # Create an AtlasExplorer instance
    # You can pass apikey, channel, region directly, or rely on config/env
    aeinst = AtlasExplorer(
        args.apikey,
        args.channel,
        args.region,
        verbose=args.verbose,
    )

    # Create an Experiment object to manage the experiment
    experiment = Experiment(args.expdir, aeinst, verbose=args.verbose)

    # Add the ELF workload file to the experiment
    experiment.addWorkload(args.elf)

    # Set the core type for the experiment
    experiment.setCore(args.core)

    # Run the experiment (this will upload, execute, and download results)
    experiment.run()

    # Locate newest summary.json produced by the just-run experiment
    exp_path = Path(args.expdir)
    summary_candidates = list(exp_path.rglob("summary/summary.json"))
    if not summary_candidates:
        print("No summary.json found under experiment directory.", file=sys.stderr)
        sys.exit(2)
    summary_candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    summary_path = summary_candidates[0]
    print(f"Produced summary: {summary_path}")

    # Export report if requested
    if args.export:
        # Lazy import reporting modules to keep examples usable without extras
        try:
            from atlasexplorer.reporting.parser import parse_summary_json
            from atlasexplorer.reporting.derive import apply_derivations
            from atlasexplorer.reporting.thresholds import apply_thresholds
            from atlasexplorer.reporting.export import (
                export_json,
                export_markdown,
                export_html,
                export_rich_html,
                export_zip,
            )
        except Exception as e:
            print(
                "Reporting extras not installed. Install with 'uv pip install -e .[reporting]' to use --export.",
                file=sys.stderr,
            )
            sys.exit(3)

        report = parse_summary_json(str(summary_path))
        report = apply_derivations(report)
        report = apply_thresholds(report)

        # Determine output path
        default_dir = summary_path.parent
        if args.export == "json":
            default_name = "report.json"
        elif args.export == "markdown":
            default_name = "report.md"
        elif args.export == "html":
            default_name = "report.html"
        elif args.export == "rich-html":
            default_name = "report_rich.html"
        else:  # zip
            default_name = "report_bundle.zip"
        out_path = Path(args.out) if args.out else (default_dir / default_name)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if args.export == "json":
            export_json(report, str(out_path))
        elif args.export == "markdown":
            export_markdown(report, str(out_path))
        elif args.export == "html":
            export_html(report, str(out_path))
        elif args.export == "rich-html":
            export_rich_html(report, str(out_path))
        elif args.export == "zip":
            export_zip(report, str(out_path), rich=True)
        print(f"Export written to: {out_path}")

    # Optionally still show a quick KPI
    # Print total cycles (preserve original example behavior)
    if not args.export:
        try:
            total_cycles = experiment.getSummary().getTotalCycles()
            print(f"Total Cycles: {total_cycles}")
        except Exception:
            pass
    else:
        try:
            total_cycles_metric = next((m for m in report.metrics if m.name == "Total Cycles Consumed"), None)
            if total_cycles_metric is not None and total_cycles_metric.value is not None:
                print(f"Total Cycles: {total_cycles_metric.value}")
        except Exception:
            pass

if __name__ == "__main__":
    main()
