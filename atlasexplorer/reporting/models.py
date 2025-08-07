from __future__ import annotations
from typing import Optional, List, Union, Literal
from pydantic import BaseModel, Field, validator
import re

class RawMetric(BaseModel):
    name: str
    desc: Optional[str] = None
    vis: Optional[int] = None
    raw_value: Union[int, float, str, None] = Field(alias='val', default=None)

    @property
    def numeric_value(self) -> Optional[float]:
        if isinstance(self.raw_value, (int, float)):
            return float(self.raw_value)
        try:
            if isinstance(self.raw_value, str):
                if self.raw_value.lower() in {"inf", "+inf", "infinity"}:
                    return None
                return float(self.raw_value)
        except Exception:
            return None
        return None

THREAD_RE = re.compile(r"Thread (\d+)")

class Metric(BaseModel):
    name: str
    value: Optional[float]
    raw_value: Union[int, float, str, None]
    description: Optional[str] = None
    category: str
    thread: Optional[int] = None
    unit: Optional[str] = None
    derived: bool = False
    formula: Optional[str] = None
    status: Optional[Literal['green','yellow','red','na']] = None
    notes: List[str] = []

class ReportMetadata(BaseModel):
    arch: Optional[str] = None
    report_format: Optional[str] = None

class SimInfo(BaseModel):
    name: Optional[str] = None
    sim_version: Optional[str] = None
    sparta_version: Optional[str] = None
    json_report_version: Optional[str] = None
    reproduction: Optional[str] = None

class SummaryReportModel(BaseModel):
    metrics: List[Metric]
    metadata: Optional[ReportMetadata] = None
    siminfo: Optional[SimInfo] = None

    def get_metric(self, name: str) -> Optional[Metric]:
        for m in self.metrics:
            if m.name == name:
                return m
        return None

    def to_dict(self):
        return self.model_dump()
