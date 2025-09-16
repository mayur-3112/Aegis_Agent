import os
import shutil
from blake3 import blake3
from dataclasses import dataclass, asdict

# --- The Professional Data Structure ---
# This is the "art." We are not just capturing a hash; we are capturing a
# complete, forensically valuable snapshot of each file's state.
@dataclass
class SnapshotEntry:
    """A dataclass to hold the state of a single file."""
    path: str
    hash: str
    size: int
    mtime: float

# --- The Engine, Forged to Our Architectural Contract ---
def create_baseline(file_list: list) -> dict:
    """
    Takes a list of files, creates a rich SnapshotEntry for each,
    and returns a dictionary of {filepath: SnapshotEntry}.

    This is the "Hybrid Engine." It combines artistic complexity with
    the disciplined purity of our architecture.

    Args:
        file_list (list): A list of absolute file paths from the Discovery Engine.

    Returns:
        dict: A dictionary of {filepath (str): SnapshotEntry (dataclass)}.
    """
    baseline = {}
    total_files = len(file_list)
    print(f"[*] Baseline Engine: Starting snapshot of {total_files} files...")

    for i, filepath in enumerate(file_list):
        try:
            # 1. Get file metadata (the rich data)
            stat_info = os.stat(filepath)
            size = stat_info.st_size
            mtime = stat_info.st_mtime

            # 2. Compute the BLAKE3 hash (the superior technology)
            hasher = blake3()
            with open(filepath, "rb") as f:
                while chunk := f.read(65536): # 64KB chunks
                    hasher.update(chunk)
            
            hex_hash = hasher.hexdigest()

            # 3. Create the masterpiece object
            entry = SnapshotEntry(path=filepath, hash=hex_hash, size=size, mtime=mtime)
            baseline[filepath] = entry
            
            # A simple progress indicator for the user
            print(f"  [{i+1}/{total_files}] Snapshotted: {os.path.basename(filepath)}", end='\r')

        except FileNotFoundError:
            print(f"\n[WARN] File not found during snapshot, skipping: {filepath}")
            continue
        except PermissionError:
            print(f"\n[WARN] Permission denied to read file, skipping: {filepath}")
            continue
        except Exception as e:
            print(f"\n[ERROR] An unexpected error occurred with {filepath}: {e}")
            continue

    print(f"\n[*] Baseline Engine: Snapshot complete. Successfully processed {len(baseline)} files.")
    return baseline

# --- The Built-in Test Harness ---
# This proves our masterpiece works in a controlled environment.
if __name__ == "__main__":
    print("--- [Aegis Hybrid Engine Test] ---")

    # 1. Create a temporary, controlled test environment
    TEST_DIR = "hybrid_engine_test_fs"
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR, exist_ok=True)

    test_file_1 = os.path.join(TEST_DIR, "document.pdf")
    test_file_2 = os.path.join(TEST_DIR, "config.yml")

    with open(test_file_1, "wb") as f:
        f.write(os.urandom(1024)) # 1KB of random data
    with open(test_file_2, "w") as f:
        f.write("key: value")

    print(f"Created temporary test files in: ./{TEST_DIR}")
    files_to_test = [test_file_1, test_file_2]

    # 2. Run the engine
    generated_baseline = create_baseline(files_to_test)

    # 3. Analyze the rich, complex results
    print("\n--- [Baseline Results] ---")
    if generated_baseline:
        for path, entry in generated_baseline.items():
            # We convert the dataclass to a dictionary for clean printing
            print(f"  [+] Path: {path}")
            print(f"      - Hash: {entry.hash[:16]}...")
            print(f"      - Size: {entry.size} bytes")
            print(f"      - MTime: {entry.mtime}")
    else:
        print("No baseline was generated.")

    print("\n--- [Expected Outcome Analysis] ---")
    assert len(generated_baseline) == len(files_to_test), "Test Failed: Did not process all files."
    assert isinstance(generated_baseline[test_file_1], SnapshotEntry), "Test Failed: Did not create SnapshotEntry object."
    print("All assertions passed. The masterpiece is functional.")

    # 4. Clean up the test environment
    shutil.rmtree(TEST_DIR)
    print("\n--- [Test Cleanup Complete] ---")

