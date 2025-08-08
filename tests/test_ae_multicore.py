"""
Test: ATLAS Explorer Multicore Experiment

This test demonstrates how to run a multicore experiment using the ATLAS Explorer Python library.

Configuration:
    - Set the environment variable MIPS_ATLAS_CONFIG to '<apikey>:<channel>:<region>'
    - Or run 'uv run atlasexplorer/atlasexplorer.py configure' to set up your credentials interactively

Usage:
    python -m pytest -s tests/test_ae_multicore.py

This test will:
    - Create an AtlasExplorer instance using credentials from the environment
    - Create a new experiment in the 'myexperiments' directory
    - Add multiple workload ELF files
    - Set the core type
    - Run the experiment and check the total cycles
"""
from atlasexplorer import atlasexplorer
from dotenv import load_dotenv
import pytest
import locale
import os

load_dotenv()


@pytest.mark.skipif(not os.environ.get("MIPS_ATLAS_CONFIG"), reason="MIPS_ATLAS_CONFIG not set; skipping cloud-dependent test")
def test_multicore():
    locale.setlocale(locale.LC_ALL, "")
    # Get credentials from environment variable
    config_str = os.environ.get("MIPS_ATLAS_CONFIG", "")
    try:
        apikey, channel, region = config_str.split(":")
    except ValueError:
        raise RuntimeError("MIPS_ATLAS_CONFIG environment variable must be set as 'apikey:channel:region'")
    # Create an AtlasExplorer instance
    aeinst = atlasexplorer.AtlasExplorer(
        apikey,
        channel,
        region,
        verbose=True,
    )
    # Create a new experiment in 'myexperiments' directory
    experiment = atlasexplorer.Experiment("myexperiments", aeinst, verbose=True)
    # Add workloads to the experiment using absolute paths
    mandelbrot_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "resources", "mandelbrot_rv64_O0.elf"
        )
    )
    memcpy_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "resources", "memcpy_rv64.elf")
    )
    experiment.addWorkload(mandelbrot_path)
    experiment.addWorkload(memcpy_path)
    # Set the core type for the experiment
    experiment.setCore("I8500_(2_threads)")
    # Run the experiment
    experiment.run()
    # Get the total cycles and assert the expected value
    total_cycles = experiment.getSummary().getTotalCycles()
    print(f"Total Cycles: {total_cycles}")
    assert total_cycles == 257577, "Total Cycles should be 257577"
