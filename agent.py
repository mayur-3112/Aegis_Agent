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

def build_baseline(target_dir, output_file='baseline.json'):
    """
    Scans a directory and creates a JSON file with file hashes.
    """
    logging.info(f"Starting to build baseline for: {target_dir}")
    
    hashes = {}
    
    if not os.path.isdir(target_dir):
        logging.error(f"Directory not found: {target_dir}")
        return

    # Walk through the entire directory tree
    for root, _, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip the baseline file itself to avoid a circular hash
            if file_path == os.path.join(target_dir, output_file):
                continue
                
            file_hash = get_hash(file_path)
            
            if file_hash:
                # Store the path relative to the monitored directory
                relative_path = os.path.relpath(file_path, target_dir)
                hashes[relative_path] = file_hash
                logging.info(f"Hashed: {relative_path}")

    # Write the collected hashes to the JSON file
    try:
        with open(output_file, 'w') as f:
            json.dump(hashes, f, indent=4)
        logging.info(f"Baseline finished. Saved to {output_file}")
    except Exception as e:
        logging.error(f"Failed to write baseline file: {e}")


if __name__ == "__main__":
    # The directory we want to monitor. Let's make one if it's not there.
    target_directory = "./monitored_files"

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        logging.info(f"Created new directory: {target_directory}")
        
    build_baseline(target_directory)
