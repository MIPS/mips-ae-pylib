"""
ATLAS Explorer Multicore Experiment Example

This script demonstrates how to run a multicore experiment using the ATLAS Explorer Python library.

Usage:
    uv run examples/ae_multicore.py --elf resources/mandelbrot_rv64_O0.elf resources/memcpy_rv64.elf --channel development --core I8500_(2_threads)

Arguments:
    --elf      Path(s) to ELF workload file(s). You can specify multiple files separated by spaces.
    --expdir   Directory to store experiment results (default: myexperiments)
    --core     Core type to use for the experiment (default: I8500_(2_threads))
    --channel  Channel name (default: development)
    --apikey   Your ATLAS Explorer API key (optional if configured)
    --region   Region name (optional if configured)
    --verbose  Enable verbose output for debugging

Configuration:
    You must configure your API key, channel, and region before running experiments.
    - Use 'uv run atlasexplorer/atlasexplorer.py configure' for interactive setup
    - Or set the environment variable: export MIPS_ATLAS_CONFIG=<apikey>:<channel>:<region>

Example:
    uv run examples/ae_multicore.py --elf resources/mandelbrot_rv64_O0.elf resources/memcpy_rv64.elf --channel development --core I8500_(2_threads)

"""
import argparse
import locale
import os
import sys
from dotenv import load_dotenv
from atlasexplorer import AtlasExplorer, Experiment

# Load environment variables from .env file
load_dotenv()

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Run a multicore experiment with ATLAS Explorer.")
    parser.add_argument("--elf", required=True, nargs='+', help="Path(s) to ELF workload file(s). Multiple allowed.")
    parser.add_argument("--expdir", default="myexperiments", help="Experiment directory (default: myexperiments)")
    parser.add_argument("--core", default="I8500_(2_threads)", help="Core type (default: I8500_(2_threads)")
    parser.add_argument("--channel", default="development", help="Channel (default: development)")
    parser.add_argument("--apikey", help="Your ATLAS Explorer API key.")
    parser.add_argument("--region", help="Region")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()

    # Check for configuration: ENV, config file, or CLI args
    config_env = os.environ.get("MIPS_ATLAS_CONFIG")
    home_dir = os.path.expanduser("~")
    config_file = os.path.join(home_dir, ".config", "mips", "atlaspy", "config.json")
    if not args.apikey and not config_env and not os.path.exists(config_file):
        print("Atlas Explorer configuration not found.")
        print("Please run 'uv run atlasexplorer/atlasexplorer.py configure' before using this script.")
        sys.exit(1)

    # Set locale for pretty printing numbers
    locale.setlocale(locale.LC_ALL, "")

    # Create an AtlasExplorer instance
    # You can pass apikey, channel, region directly, or rely on config/env
    try:
        aeinst = AtlasExplorer(
            args.apikey,
            args.channel,
            args.region,
            verbose=args.verbose,
        )
    except SystemExit:
        # AtlasExplorer exits if configuration is missing
        sys.exit(1)

    # Check if gateway is properly configured
    if not hasattr(aeinst.config, 'gateway') or aeinst.config.gateway is None:
        print("Error: Atlas Explorer gateway configuration failed.")
        print("This usually means there's an issue with the API service or your configuration.")
        print("Please run 'uv run atlasexplorer/atlasexplorer.py configure' to reconfigure your settings.")
        sys.exit(1)

    # Create an Experiment object to manage the experiment
    experiment = Experiment(args.expdir, aeinst, verbose=args.verbose)

    # Add each ELF workload file to the experiment
    for elf_path in args.elf:
        experiment.addWorkload(os.path.abspath(elf_path))

    # Set the core type for the experiment
    experiment.setCore(args.core)

    # Run the experiment (this will upload, execute, and download results)
    experiment.run()

    # Get and print the total cycles from the experiment summary
    summary = experiment.getSummary()
    if summary is not None:
        total_cycles = summary.getTotalCycles()
        print(f"Total Cycles: {total_cycles}")
    else:
        print("No summary report available - experiment may have failed or ELF files may be invalid")

if __name__ == "__main__":
    main()
