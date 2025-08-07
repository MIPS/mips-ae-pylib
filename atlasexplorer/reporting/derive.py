from __future__ import annotations
from .models import SummaryReportModel, Metric
from typing import Dict, Callable, List

# Registry of derived metric functions: name -> (dependencies, func)
DERIVED: Dict[str, Dict] = {}

def derived_metric(name: str, deps: List[str], formula: str):
    def decorator(fn: Callable):
        DERIVED[name] = {"deps": deps, "fn": fn, "formula": formula}
        return fn
    return decorator

@derived_metric("CPI", ["Total Cycles Consumed", "Total Instructions Retired (All Threads)"], "cycles / instructions")
def derive_cpi(values):
    cycles, instr = values
    if cycles and instr and instr != 0:
        return cycles / instr
    return None

@derived_metric("Branch Prediction Accuracy %", ["Total Number of Mispredicts", "Total Number of Predictions"], "(1 - mispredicts/predictions)*100")
def derive_branch_acc(values):
    mis, total = values
    if total and total != 0:
        return (1 - (mis / total)) * 100
    return None

@derived_metric("ICache Miss Rate %", ["ICache Hits", "ICache Misses"], "(misses/(hits+misses))*100")
def derive_ic_miss(values):
    hits, misses = values
    denom = hits + misses if hits is not None and misses is not None else None
    if denom and denom != 0:
        return (misses / denom) * 100
    return None

@derived_metric("DCache Miss Rate %", ["Level 1 Data Cache hits", "Level 1 Data Cache Misses"], "(misses/(hits+misses))*100")
def derive_dc_miss(values):
    hits, misses = values
    denom = hits + misses if hits is not None and misses is not None else None
    if denom and denom != 0:
        return (misses / denom) * 100
    return None

@derived_metric("DTLB Miss Rate %", ["Data Translation Lookaside Buffer (DTLB) Hits", "Data Translation Lookaside Buffer (DTLB) Misses"], "(misses/(hits+misses))*100")
def derive_dtlb_miss(values):
    hits, misses = values
    denom = hits + misses if hits is not None and misses is not None else None
    if denom and denom != 0:
        return (misses / denom) * 100
    return None

@derived_metric("Load Bond Success %", ["Number of Good Load Bonds", "Number of Bad Load Bonds"], "good/(good+bad)*100")
def derive_load_bond(values):
    good, bad = values
    denom = good + bad if good is not None and bad is not None else None
    if denom and denom != 0:
        return (good / denom) * 100
    return None

@derived_metric("Store Bond Success %", ["Number of Good Store Bonds", "Number of Bad Store Bonds"], "good/(good+bad)*100")
def derive_store_bond(values):
    good, bad = values
    denom = good + bad if good is not None and bad is not None else None
    if denom and denom != 0:
        return (good / denom) * 100
    return None

@derived_metric("Thread Balance %", ["Instructions Retired Thread 0", "Instructions Retired Thread 1"], "(max-min)/avg*100")
def derive_thread_balance(values):
    a, b = values
    if a is None or b is None:
        return None
    avg = (a + b) / 2
    if avg == 0:
        return None
    return (abs(a - b) / avg) * 100

@derived_metric("ALU Instruction Mix %", ["Instructions Executed on ALU 0", "Instructions Executed on ALU 1", "Instrution Executed on FPU 0", "Instrution Executed on FPU 1"], "(alu_total/total)*100")
def derive_alu_mix(values):
    alu0, alu1, fpu0, fpu1 = values
    if None in values:
        return None
    total = alu0 + alu1 + fpu0 + fpu1
    if total == 0:
        return None
    return ((alu0 + alu1) / total) * 100

@derived_metric("FPU Instruction Mix %", ["Instructions Executed on ALU 0", "Instructions Executed on ALU 1", "Instrution Executed on FPU 0", "Instrution Executed on FPU 1"], "(fpu_total/total)*100")
def derive_fpu_mix(values):
    alu0, alu1, fpu0, fpu1 = values
    if None in values:
        return None
    total = alu0 + alu1 + fpu0 + fpu1
    if total == 0:
        return None
    return ((fpu0 + fpu1) / total) * 100


def apply_derivations(report: SummaryReportModel) -> SummaryReportModel:
    name_to_metric = {m.name: m for m in report.metrics}
    new_metrics: List[Metric] = []
    for name, spec in DERIVED.items():
        deps = spec['deps']
        vals = []
        missing = False
        for d in deps:
            if d not in name_to_metric or name_to_metric[d].value is None:
                missing = True
                break
            vals.append(name_to_metric[d].value)
        if missing:
            continue
        try:
            value = spec['fn'](vals)
        except Exception:
            value = None
        new_metrics.append(Metric(
            name=name,
            value=value,
            raw_value=value,
            description=f"Derived metric: {spec['formula']}",
            category='derived',
            derived=True,
            formula=spec['formula']
        ))
    report.metrics.extend(new_metrics)
    return report
