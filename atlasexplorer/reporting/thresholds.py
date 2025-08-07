from __future__ import annotations
from .models import SummaryReportModel
from typing import List, Optional, Literal
import re

class ThresholdRule:
    def __init__(self, pattern: str, direction: Literal['higher','lower'], green: float, yellow: float, description: str = ""):
        self.pattern = re.compile(pattern)
        self.direction = direction
        self.green = green
        self.yellow = yellow
        self.description = description

    def classify(self, value: Optional[float]) -> str:
        if value is None:
            return 'na'
        if self.direction == 'higher':
            if value >= self.green:
                return 'green'
            if value >= self.yellow:
                return 'yellow'
            return 'red'
        else:
            if value <= self.green:
                return 'green'
            if value <= self.yellow:
                return 'yellow'
            return 'red'

DEFAULT_RULES: List[ThresholdRule] = [
    ThresholdRule(r'^Branch Prediction Accuracy %$', 'higher', 97.0, 90.0),
    ThresholdRule(r'^ICache Miss Rate %$', 'lower', 5.0, 10.0),
    ThresholdRule(r'^DCache Miss Rate %$', 'lower', 5.0, 10.0),
    ThresholdRule(r'^DTLB Miss Rate %$', 'lower', 0.1, 0.5),
    ThresholdRule(r'^CPI$', 'lower', 1.0, 2.0),
    ThresholdRule(r'^Load Bond Success %$', 'higher', 95.0, 85.0),
    ThresholdRule(r'^Store Bond Success %$', 'higher', 95.0, 85.0),
    ThresholdRule(r'^Thread Balance %$', 'lower', 5.0, 15.0),
]

def apply_thresholds(report: SummaryReportModel, extra: List[ThresholdRule] | None = None):
    rules = DEFAULT_RULES + (extra or [])
    for m in report.metrics:
        for rule in rules:
            if rule.pattern.search(m.name):
                m.status = rule.classify(m.value)
                break
    return report
