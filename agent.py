# agent.py - The Central Nervous System
# Architect: Mayur

import argparse
import sys
import json

# This is where we import the brilliant modules your team will build.
# The 'engine' package structure makes our code clean and professional.
from engine import config_engine
from engine import baseline_engine
from engine import integrity_engine

def save_baseline(filepath: str, data: dict):
    """Saves the baseline dictionary to a JSON file."""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        # This is professional error handling, crucial for a security tool.
        raise Exception(f"Failed to write baseline to {filepath}: {e}")

def load_baseline(filepath: str) -> dict:
    """Loads the baseline dictionary from a JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # It's not an error if the baseline doesn't exist yet for a check.
        # The main logic will handle this case.
        return {}
    except json.JSONDecodeError as e:
        # This prevents a crash if the file is manually corrupted.
        raise Exception(f"Failed to parse baseline file {filepath}: {e}")

def main():
    """The main entry point and logic controller for the Aegis Core Engine."""

    # 1. The Command-Line Interface (CLI)
    parser = argparse.ArgumentParser(
        description="Aegis Core Engine: A high-performance File Integrity Monitor.",
        epilog="Example: python agent.py --check --config my_config.json"
    )
    parser.add_argument('--init', action='store_true', help='Initialize a new baseline.')
    parser.add_argument('--check', action='store_true', help='Perform an integrity check against the baseline.')
    parser.add_argument('--config', default='config.json', help='Path to the configuration file.')
    parser.add_argument('--baseline', default='baseline.json', help='Path to the baseline file.')

    # If the user runs the script with no arguments, we must show them how to use it.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # 2. The Core Orchestration Logic
    print("--- Aegis Core Engine Initializing ---")

    if args.init:
        print(f"Mode: Initializing new baseline using '{args.config}'...")
        try:
            files_to_scan = config_engine.get_file_list(args.config)
            baseline = baseline_engine.create_baseline(files_to_scan)
            save_baseline(args.baseline, baseline)
            print(f"Baseline generation complete. Found and hashed {len(baseline)} files.")
            print(f"Baseline successfully saved to '{args.baseline}'.")

        except Exception as e:
            print(f"[FATAL] Error during initialization: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.check:
        print(f"Mode: Performing integrity check against '{args.baseline}'...")
        try:
            old_baseline = load_baseline(args.baseline)
            if not old_baseline:
                raise Exception(f"Baseline file '{args.baseline}' not found or is empty. Please run with --init first.")

            files_to_scan = config_engine.get_file_list(args.config)
            new_baseline = baseline_engine.create_baseline(files_to_scan)
            results = integrity_engine.compare_baselines(old_baseline, new_baseline)

            # TODO: Pass the results to Harshit's reporting module.
            print("--- Integrity Check Results ---")
            print(json.dumps(results, indent=2))
            print("-----------------------------")

        except Exception as e:
            print(f"[FATAL] Error during check: {e}", file=sys.stderr)
            sys.exit(1)

    print("--- Aegis Core Engine Shutdown ---")

if __name__ == "__main__":
    main()

# agent.py - The Central Nervous System
# Architect: Mayur

import argparse
import sys
import json

# This is where we import the brilliant modules your team will build.
from engine import config_engine
from engine import baseline_engine
from engine import integrity_engine

def save_baseline(filepath: str, data: dict):
    """Saves the baseline dictionary to a JSON file."""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        raise Exception(f"Failed to write baseline to {filepath}: {e}")

def load_baseline(filepath: str) -> dict:
    """Loads the baseline dictionary from a JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse baseline file {filepath}: {e}")

def main():
    """The main entry point and logic controller for the Aegis Core Engine."""

    parser = argparse.ArgumentParser(
        description="Aegis Core Engine: A high-performance File Integrity Monitor.",
        epilog="Example: python agent.py --check --config my_config.json"
    )
    parser.add_argument('--init', action='store_true', help='Initialize a new baseline.')
    parser.add_argument('--check', action='store_true', help='Perform an integrity check against the baseline.')
    parser.add_argument('--config', default='config.json', help='Path to the configuration file.')
    parser.add_argument('--baseline', default='baseline.json', help='Path to the baseline file.')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    print("--- Aegis Core Engine Initializing ---")

    if args.init:
        print(f"Mode: Initializing new baseline using '{args.config}'...")
        try:
            files_to_scan = config_engine.get_file_list(args.config)
            baseline = baseline_engine.create_baseline(files_to_scan)
            save_baseline(args.baseline, baseline)
            print(f"Baseline generation complete. Found and hashed {len(baseline)} files.")
            print(f"Baseline successfully saved to '{args.baseline}'.")

        except Exception as e:
            print(f"[FATAL] Error during initialization: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.check:
        print(f"Mode: Performing integrity check against '{args.baseline}'...")
        try:
            old_baseline = load_baseline(args.baseline)
            if not old_baseline:
                raise Exception(f"Baseline file '{args.baseline}' not found or is empty. Please run with --init first.")

            files_to_scan = config_engine.get_file_list(args.config)
            new_baseline = baseline_engine.create_baseline(files_to_scan)
            results = integrity_engine.compare_baselines(old_baseline, new_baseline)

            # TODO: Pass the results to Harshit's reporting module.
            print("--- Integrity Check Results ---")
            print(json.dumps(results, indent=2))
            print("-----------------------------")

        except Exception as e:
            print(f"[FATAL] Error during check: {e}", file=sys.stderr)
            sys.exit(1)

    print("--- Aegis Core Engine Shutdown ---")

if __name__ == "__main__":
    main()
