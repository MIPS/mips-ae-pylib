from atlasexplorer.reporting.parser import parse_summary_json
from atlasexplorer.reporting.derive import apply_derivations
from atlasexplorer.reporting.thresholds import apply_thresholds

import json, tempfile, textwrap

def make_summary(tmp_path):
    data = {
        "Statistics": {
            "Summary Performance Report": {
                "Total Cycles Consumed": {"val": 1000, "desc": "cycles"},
                "Total Instructions Retired (All Threads)": {"val": 500, "desc": "inst"},
                "Total Number of Mispredicts": {"val": 5, "desc": "mis"},
                "Total Number of Predictions": {"val": 505, "desc": "pred"},
                # Cache stats for miss rate
                "ICache Hits": {"val": 950, "desc": "hits"},
                "ICache Misses": {"val": 50, "desc": "miss"},
                "Level 1 Data Cache hits": {"val": 900, "desc": "hits"},
                "Level 1 Data Cache Misses": {"val": 100, "desc": "miss"},
                "Data Translation Lookaside Buffer (DTLB) Hits": {"val": 999, "desc": "hits"},
                "Data Translation Lookaside Buffer (DTLB) Misses": {"val": 1, "desc": "miss"},
                # Bond success
                "Number of Good Load Bonds": {"val": 95, "desc": "good"},
                "Number of Bad Load Bonds": {"val": 5, "desc": "bad"},
                "Number of Good Store Bonds": {"val": 96, "desc": "good"},
                "Number of Bad Store Bonds": {"val": 4, "desc": "bad"},
                # Thread instructions
                "Instructions Retired Thread 0": {"val": 260, "desc": "inst"},
                "Instructions Retired Thread 1": {"val": 240, "desc": "inst"},
                # Instruction mix ALU/FPU (typo preserved from derive deps name for FPU)
                "Instructions Executed on ALU 0": {"val": 200, "desc": "inst"},
                "Instructions Executed on ALU 1": {"val": 180, "desc": "inst"},
                "Instrution Executed on FPU 0": {"val": 70, "desc": "inst"},
                "Instrution Executed on FPU 1": {"val": 50, "desc": "inst"},
            }
        },
        "report_metadata": {"arch": "I8500", "report_format": "json"},
        "siminfo": {"name": "Sim", "sim_version": "v1"}
    }
    p = tmp_path / 'summary.json'
    p.write_text(json.dumps(data))
    return p

def test_parse_and_derive(tmp_path):
    path = make_summary(tmp_path)
    report = parse_summary_json(str(path))
    assert report.get_metric("Total Cycles Consumed").value == 1000
    report = apply_derivations(report)
    report = apply_thresholds(report)
    # CPI
    cpi = report.get_metric("CPI")
    assert cpi is not None and abs(cpi.value - 2.0) < 1e-9
    # Branch accuracy
    ba = report.get_metric("Branch Prediction Accuracy %")
    assert ba is not None and abs(ba.value - ((1 - (5/505))*100)) < 1e-9
    # Cache miss rates
    ic_miss = report.get_metric("ICache Miss Rate %")
    assert ic_miss is not None and abs(ic_miss.value - (50/1000*100)) < 1e-9
    dc_miss = report.get_metric("DCache Miss Rate %")
    assert dc_miss is not None and abs(dc_miss.value - (100/1000*100)) < 1e-9
    dtlb_miss = report.get_metric("DTLB Miss Rate %")
    assert dtlb_miss is not None and abs(dtlb_miss.value - (1/1000*100)) < 1e-9
    # Bond success
    lb = report.get_metric("Load Bond Success %")
    assert lb is not None and abs(lb.value - (95/100*100)) < 1e-9
    sb = report.get_metric("Store Bond Success %")
    assert sb is not None and abs(sb.value - (96/100*100)) < 1e-9
    # Thread balance (abs(260-240)/avg(250) *100 = 20/250*100 = 8%)
    tb = report.get_metric("Thread Balance %")
    assert tb is not None and abs(tb.value - 8.0) < 1e-9
    # Instruction mix
    alu_mix = report.get_metric("ALU Instruction Mix %")
    assert alu_mix is not None and abs(alu_mix.value - ((200+180)/(200+180+70+50)*100)) < 1e-9
    fpu_mix = report.get_metric("FPU Instruction Mix %")
    assert fpu_mix is not None and abs(fpu_mix.value - ((70+50)/(200+180+70+50)*100)) < 1e-9
    # Threshold statuses spot check
    assert lb.status == 'green'  # 95%
    assert ic_miss.status == 'green'  # 5%
    assert tb.status == 'yellow'  # 8% with green<=5 yellow<=15
