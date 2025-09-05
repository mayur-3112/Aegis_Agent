# agent.py - The Central Nervous System
# Architect: Mayur (You)

import argparse
import sys

# This is where we import the brilliant modules your team will build.
# The 'engine' package structure makes our code clean and professional.
from engine import config_engine
from engine import baseline_engine
from engine import integrity_engine

def main():
    """The main entry point and logic controller for the Aegis Core Engine."""

    # 1. The Command-Line Interface (CLI)
    # This is how users will interact with our tool. It must be professional and clear.
    parser = argparse.ArgumentParser(
        description="Aegis Core Engine: A high-performance File Integrity Monitor.",
        epilog="Example: python agent.py --check --config my_config.json"
    )
    parser.add_argument('--init', action='store_true', help='Initialize a new baseline.')
    parser.add_argument('--check', action='store_true', help='Perform an integrity check against the baseline.')
    parser.add_argument('--config', default='config.json', help='Path to the configuration file.')

    # If the user runs the script with no arguments, we should show them how to use it.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # 2. The Core Orchestration Logic
    # This is the "brain." It calls the right engines in the right order.
    print("--- Aegis Core Engine Initializing ---")

    if args.init:
        print("Mode: Initializing new baseline...")
        try:
            # Step A: Call Harshit's engine to discover files.
            files_to_scan = config_engine.get_file_list(args.config)
            
            # Step B: Pass that list to Keshav's engine to create the baseline.
            baseline = baseline_engine.create_baseline(files_to_scan)
            
            # For now, we just print a success message. Later, we'll save the baseline.
            print(f"Baseline generation complete. Found and hashed {len(baseline)} files.")

        except Exception as e:
            print(f"[FATAL] Error during initialization: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.check:
        print("Mode: Performing integrity check...")
        try:
            # This is a placeholder for the full check logic you'll build later.
            old_baseline = {}  # This will be loaded from a file.
            new_baseline = {}  # This will be generated fresh.
            
            # Step C: Pass the baselines to Chetan's engine to find the differences.
            results = integrity_engine.compare_baselines(old_baseline, new_baseline)
            
            # For now, we just print a success message. Later, we'll display the results.
            print("Integrity check complete.")

        except Exception as e:
            print(f"[FATAL] Error during check: {e}", file=sys.stderr)
            sys.exit(1)

    print("--- Aegis Core Engine Shutdown ---")

if __name__ == "__main__":
    main()
