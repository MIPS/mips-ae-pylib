from __future__ import annotations
import argparse, sys
from .parser import parse_summary_json
from .derive import apply_derivations
from .thresholds import apply_thresholds
from .render_cli import render_kpis, render_category_tables, render_legend
from .export import export_json, export_markdown, export_html, export_rich_html, export_zip

def main(argv=None):
    parser = argparse.ArgumentParser(prog='atlasexplorer-report', description='Atlas Explorer Reporting CLI')
    parser.add_argument('summary_json', help='Path to summary.json')
    parser.add_argument('--baseline', metavar='PATH', help='Baseline summary.json for comparison')
    parser.add_argument('--percent-delta', action='store_true', help='Show percent delta instead of absolute')
    parser.add_argument('--kpi-only', action='store_true', help='Show only KPI table')
    parser.add_argument('--categories', nargs='*', help='Filter categories')
    parser.add_argument('--export-json', metavar='PATH', help='Export full report model as JSON')
    parser.add_argument('--export-md', metavar='PATH', help='Export Markdown summary')
    parser.add_argument('--export-html', metavar='PATH', help='Export static HTML summary (basic)')
    parser.add_argument('--export-rich-html', metavar='PATH', help='Export richer HTML with charts')
    parser.add_argument('--export-zip', metavar='PATH', help='Export a zip bundle (json, md, html)')

    args = parser.parse_args(argv)
    report = parse_summary_json(args.summary_json)
    report = apply_derivations(report)
    report = apply_thresholds(report)
    baseline_values = None
    if args.baseline:
        base_report = parse_summary_json(args.baseline)
        base_report = apply_derivations(base_report)
        baseline_values = {m.name: m.value for m in base_report.metrics}
    render_kpis(report)
    if not args.kpi_only:
        render_category_tables(report, args.categories, baseline=baseline_values, show_percent=args.percent_delta)
        render_legend()

    # Exports
    if args.export_json:
        export_json(report, args.export_json)
    if args.export_md:
        export_markdown(report, args.export_md)
    if args.export_html:
        export_html(report, args.export_html)
    if args.export_rich_html:
        export_rich_html(report, args.export_rich_html)
    if args.export_zip:
        export_zip(report, args.export_zip, rich=True)

if __name__ == '__main__':  # pragma: no cover
    main()
