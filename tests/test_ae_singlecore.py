"""
Test: ATLAS Explorer Single Core Experiment

This test demonstrates how to run a single core experiment using the ATLAS Explorer Python library.

Configuration:
    - Set the environment variable MIPS_ATLAS_CONFIG to '<apikey>:<channel>:<region>'
    - Or run 'uv run atlasexplorer/atlasexplorer.py configure' to set up your credentials interactively

Usage:
    python -m pytest -s tests/test_ae_singlecore.py

This test will:
    - Create an AtlasExplorer instance using credentials from the environment
    - Create a new experiment in the 'myexperiments' directory
    - Add a workload ELF file
    - Set the core type
    - Run the experiment and check the total cycles
"""
from atlasexplorer.atlasexplorer import AtlasExplorer, Experiment
import locale
import os
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.skipif(not os.environ.get("MIPS_ATLAS_CONFIG"), reason="MIPS_ATLAS_CONFIG not set; skipping cloud-dependent test")
def test_singlecore():
    locale.setlocale(locale.LC_ALL, "")
    # Get credentials from environment variable
    config_str = os.environ.get("MIPS_ATLAS_CONFIG", "")
    try:
        apikey, channel, region = config_str.split(":")
    except ValueError:
        raise RuntimeError("MIPS_ATLAS_CONFIG environment variable must be set as 'apikey:channel:region'")
    # Create an AtlasExplorer instance
    aeinst = AtlasExplorer(
        apikey,
        channel,
        region,
        verbose=True,
    )
    # Create a new experiment in 'myexperiments' directory
    experiment = Experiment("myexperiments", aeinst, verbose=True)
    # Add a workload to the experiment
    experiment.addWorkload("resources/mandelbrot_rv64_O0.elf")
    # experiment.addWorkload("resources/memcpy_rv64.elf")  # You can add more workloads if needed
    # Set the core type for the experiment
    experiment.setCore("I8500_(1_thread)")
    # Run the experiment
    experiment.run()
    # Get the total cycles and assert the expected value
    total_cycles = experiment.getSummary().getTotalCycles()
    assert total_cycles == 253629, "Total Cycles should be 253629"
