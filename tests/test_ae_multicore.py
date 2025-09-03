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
from atlasexplorer import AtlasExplorer, Experiment
from dotenv import load_dotenv
import locale
import os

load_dotenv()


def test_multicore():
    locale.setlocale(locale.LC_ALL, "")
    # Get credentials from environment variable
    config_str = os.environ.get("MIPS_ATLAS_CONFIG", "")
    try:
        apikey, channel, region = config_str.split(":")
    except ValueError:
        raise RuntimeError("MIPS_ATLAS_CONFIG environment variable must be set as 'apikey:channel:region'")
    # Create an AtlasExplorer instance
    try:
        aeinst = AtlasExplorer(
            apikey,
            channel,
            region,
            verbose=True,
        )
    except SystemExit:
        raise RuntimeError("AtlasExplorer configuration failed. Check your credentials and try again.")

    # Check if gateway is properly configured
    if not hasattr(aeinst.config, 'gateway') or aeinst.config.gateway is None:
        raise RuntimeError("Atlas Explorer gateway configuration failed. This usually means there's an issue with the API service or your configuration.")

    # Create an Experiment object to manage the experiment
    experiment = Experiment("myexperiments", aeinst, verbose=True)
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
    summary = experiment.getSummary()
    assert summary is not None, "Experiment summary should not be None - experiment may have failed"
    total_cycles = summary.getTotalCycles()
    print(f"Total Cycles: {total_cycles}")
    
    # Assert cycles are within reasonable range (allow for minor simulation variations)
    expected_cycles = 257577
    tolerance = 100  # Allow ±100 cycles for service variations
    assert abs(total_cycles - expected_cycles) <= tolerance, \
        f"Total Cycles should be around {expected_cycles} (±{tolerance}), got {total_cycles}"
