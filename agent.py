# agent.py
# This script creates a baseline of file hashes for our Aegis Agent project.
# It's the first step for our file integrity monitor.

import os
import hashlib
import json
import logging

# Set up logging so we can see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def get_hash(file_path):
    """
    Calculates the SHA-256 hash for a given file.
    It reads the file in chunks to handle large files efficiently.
    """
    try:
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(4096)  # read in 4KB chunks
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logging.error(f"Error hashing {file_path}: {e}")
        return None

def build_baseline(target_dir, output_file='ba    """
    Scans a directory and creates a JSON file with file hashes.
    """
   logging.info(f"Starting to build baseline or: {target_dir}")
    
    hashes = {}

    if not os.path.isdir(target_dir):
        logging.error(f"Directory not found: {target_        return
    # Walk through the entire directory tree
    for root, _, files in os.walk(target_dir):
        for file           file_path = os.path.joioot, file)
            
            # Skip the baseline file itself to avoid a circular hash
         if file_path == os.path.join(taroutput_file):
                continue
                
     file_hash = get_hash(file_path
            
            if file_hash:
            # Store the path relatve to the monitored directory
                relative_path = os.path.relpath(file_path, target_dir)
\# agent.py - The Central Nervous System
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
    # This is how users will interact with our tool. It must be professional and clear.
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
    # This is the "brain." It calls the right engines in the right order.
    print("--- Aegis Core Engine Initializing ---")

    if args.init:
        print(f"Mode: Initializing new baseline using '{args.config}'...")
        try:
            # Step A: Call Harshit's engine to discover files.
            files_to_scan = config_engine.get_file_list(args.config)
            
            # Step B: Pass that list to Keshav's engine to create the baseline.
            baseline = baseline_engine.create_baseline(files_to_scan)
            
            # Step C: Save the generated baseline to disk.
            save_baseline(args.baseline, baseline)
            
            print(f"Baseline generation complete. Found and hashed {len(baseline)} files.")
            print(f"Baseline successfully saved to '{args.baseline}'.")

        except Exception as e:
            print(f"[FATAL] Error during initialization: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.check:
        print(f"Mode: Performing integrity check against '{args.baseline}'...")
        try:
            # Step A: Load the "source of truth" from disk.
            old_baseline = load_baseline(args.baseline)
            if not old_baseline:
                raise Exception(f"Baseline file '{args.baseline}' not found or is empty. Please run with --init first.")

            # Step B: Generate a fresh baseline to compare against.
            files_to_scan = config_engine.get_file_list(args.config)
            new_baseline = baseline_engine.create_baseline(files_to_scan)

            # Step C: Pass the baselines to Chetan's engine to find the differences.
            results = integrity_engine.compare_baselines(old_baseline, new_baseline)

            # Step D: TODO: Pass the results to Harshit's reporting module.
            # For now, we will just print the results to prove the flow works.
            print("--- Integrity Check Results ---")
            print(json.dumps(results, indent=2))
            print("-----------------------------")

        except Exception as e:
            print(f"[FATAL] Error during check: {e}", file=sys.stderr)
            sys.exit(1)

    print("--- Aegis Core Engine Shutdown ---")

if __name__ == "__main__":
    main()

