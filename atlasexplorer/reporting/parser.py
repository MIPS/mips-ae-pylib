from __future__ import annotations
from .models import RawMetric, Metric, SummaryReportModel, ReportMetadata, SimInfo, THREAD_RE
from typing import List, Dict, Any
import json, re, os

CATEGORY_RULES = [
    (re.compile(r'^(Total Cycles|Total Instructions|IPC|CPI)'), 'core_summary'),
    (re.compile(r'Thread \d'), 'thread_summary'),
    (re.compile(r'(Mispredict|Prediction|ROB Flush)'), 'branch'),
    (re.compile(r'^ICache|^TLB '), 'icache_frontend'),
    (re.compile(r'Level 1 Data Cache|Translation Lookaside Buffer|VTLB|L2TLB'), 'data_mem'),
    (re.compile(r'Bond(ed|ing)|Misaligned Bonded|Good .*Bond|Bad .*Bond|Percentage of Good'), 'bonding'),
    (re.compile(r'Instructions Executed on ALU|Instrution Executed on FPU'), 'execution_mix'),
    (re.compile(r'Stall|Replays'), 'stalls'),
]

def categorize(name: str) -> str:
    for pattern, cat in CATEGORY_RULES:
        if pattern.search(name):
            return cat
    return 'other'


def parse_summary_json(path: str) -> SummaryReportModel:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path) as f:
        data = json.load(f)

    stats = data.get('Statistics', {}).get('Summary Performance Report', {})
    ordered = set(stats.get('ordered_keys', []))
    metrics: List[Metric] = []
    for key, payload in stats.items():
        if key == 'ordered_keys':
            continue
        if not isinstance(payload, dict) or 'val' not in payload:
            continue
        raw = RawMetric(name=key, **payload)
        thread = None
        m = THREAD_RE.search(key)
        if m:
            thread = int(m.group(1))
        metrics.append(Metric(
            name=key,
            value=raw.numeric_value,
            raw_value=raw.raw_value,
            description=raw.desc,
            category=categorize(key),
            thread=thread
        ))

    siminfo_raw = data.get('siminfo', {})
    metadata_raw = data.get('report_metadata', {})
    report = SummaryReportModel(metrics=metrics,
                                siminfo=SimInfo(**siminfo_raw) if siminfo_raw else None,
                                metadata=ReportMetadata(**metadata_raw) if metadata_raw else None)
    return report
