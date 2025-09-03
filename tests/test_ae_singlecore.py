"""
Test module for single core ATLAS Explorer experiments.

This test module validates the functionality of single core experiments
using the ATLAS Explorer Python library.
"""

import json
import os
import pytest
import shutil
import tempfile
from unittest.mock import Mock, patch
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from atlasexplorer import AtlasExplorer, Experiment


def test_singlecore():
    locale.setlocale(locale.LC_ALL, "")
    # Get credentials from environment variable
    import os
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
    summary = experiment.getSummary()
    assert summary is not None, "Experiment summary should not be None - experiment may have failed"
    total_cycles = summary.getTotalCycles()
    print(f"Total Cycles: {total_cycles}")
    
    # Assert cycles are within reasonable range (allow for minor simulation variations)
    expected_cycles = 253629
    tolerance = 100  # Allow ±100 cycles for service variations
    assert abs(total_cycles - expected_cycles) <= tolerance, \
        f"Total Cycles should be around {expected_cycles} (±{tolerance}), got {total_cycles}"
