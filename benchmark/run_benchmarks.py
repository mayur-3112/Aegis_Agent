import os
import time
import json
import hashlib
from pathlib import Path
from blake3 import blake3
import matplotlib.pyplot as plt
import numpy as np

def generate_test_files(base_dir: str, count: int, size_kb: int):
    """Generate test files for benchmarking"""
    os.makedirs(base_dir, exist_ok=True)
    for i in range(count):
        filepath = os.path.join(base_dir, f"test_{i}.bin")
        with open(filepath, 'wb') as f:
            f.write(os.urandom(size_kb * 1024))
    return [os.path.join(base_dir, f"test_{i}.bin") for i in range(count)]

def benchmark_hash_function(files: list, hash_func, name: str):
    """Benchmark a hash function on file list"""
    start = time.perf_counter()
    
    for filepath in files:
        hasher = hash_func()
        with open(filepath, 'rb') as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        _ = hasher.hexdigest() if name == "BLAKE3" else hasher.hexdigest()
    
    elapsed = time.perf_counter() - start
    return elapsed

def run_comprehensive_benchmark():
    """Run complete BLAKE3 vs SHA-256 benchmark"""
    
    scenarios = [
        {"count": 100, "size_kb": 10, "label": "100 files (10KB each)"},
        {"count": 1000, "size_kb": 10, "label": "1K files (10KB each)"},
        {"count": 100, "size_kb": 1024, "label": "100 files (1MB each)"},
        {"count": 1000, "size_kb": 1024, "label": "1K files (1MB each)"},
    ]
    
    results = []
    
    print("═══════════════════════════════════════")
    print("  AEGIS BENCHMARK: BLAKE3 vs SHA-256")
    print("═══════════════════════════════════════\n")
    
    for scenario in scenarios:
        print(f"Running: {scenario['label']}...")
        
        # Generate test files
        test_dir = f"benchmark_temp_{scenario['count']}_{scenario['size_kb']}"
        files = generate_test_files(test_dir, scenario['count'], scenario['size_kb'])
        
        # Benchmark BLAKE3
        blake3_time = benchmark_hash_function(files, blake3, "BLAKE3")
        
        # Benchmark SHA-256
        sha256_time = benchmark_hash_function(files, hashlib.sha256, "SHA256")
        
        # Calculate speedup
        speedup = sha256_time / blake3_time
        
        result = {
            "scenario": scenario['label'],
            "blake3_time": round(blake3_time, 4),
            "sha256_time": round(sha256_time, 4),
            "speedup": round(speedup, 2)
        }
        results.append(result)
        
        print(f"  BLAKE3: {blake3_time:.4f}s")
        print(f"  SHA256: {sha256_time:.4f}s")
        print(f"  Speedup: {speedup:.2f}x faster\n")
        
        # Cleanup
        import shutil
        shutil.rmtree(test_dir)
    
    # Save results
    with open('benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate graphs
    generate_benchmark_graphs(results)
    
    return results

def generate_benchmark_graphs(results):
    """Generate publication-ready performance graphs"""
    
    scenarios = [r['scenario'] for r in results]
    blake3_times = [r['blake3_time'] for r in results]
    sha256_times = [r['sha256_time'] for r in results]
    
    # Performance comparison bar chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    x = np.arange(len(scenarios))
    width = 0.35
    
    ax1.bar(x - width/2, blake3_times, width, label='BLAKE3', color='#00d4aa')
    ax1.bar(x + width/2, sha256_times, width, label='SHA-256', color='#ff6b6b')
    ax1.set_xlabel('Test Scenario', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
    ax1.set_title('Hash Function Performance Comparison', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenarios, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Speedup chart
    speedups = [r['speedup'] for r in results]
    ax2.bar(scenarios, speedups, color='#4ecdc4')
    ax2.axhline(y=1.0, color='red', linestyle='--', label='Baseline (SHA-256)')
    ax2.set_xlabel('Test Scenario', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Speedup Factor (x)', fontsize=12, fontweight='bold')
    ax2.set_title('BLAKE3 Performance Advantage', fontsize=14, fontweight='bold')
    ax2.set_xticklabels(scenarios, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('benchmark_results.png', dpi=300, bbox_inches='tight')
    print("✓ Graphs saved to: benchmark_results.png")

if __name__ == "__main__":
    run_comprehensive_benchmark()
