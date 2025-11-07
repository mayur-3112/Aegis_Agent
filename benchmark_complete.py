#!/usr/bin/env python3
"""
Aegis Complete Benchmark Suite
Generates IEEE-ready performance graphs and data
"""

import os
import time
import json
import hashlib
import shutil
from pathlib import Path
from blake3 import blake3
import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

console = Console()


def generate_test_files(base_dir: str, count: int, size_kb: int):
    """Generate test files for benchmarking"""
    os.makedirs(base_dir, exist_ok=True)
    files = []
    for i in range(count):
        filepath = os.path.join(base_dir, f"test_{i}.bin")
        with open(filepath, 'wb') as f:
            f.write(os.urandom(size_kb * 1024))
        files.append(filepath)
    return files


def benchmark_hash_function(files: list, hash_func, name: str):
    """Benchmark hash function"""
    start = time.perf_counter()
    
    for filepath in files:
        hasher = hash_func()
        with open(filepath, 'rb') as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        _ = hasher.hexdigest()
    
    return time.perf_counter() - start


def run_comprehensive_benchmark():
    """Run complete benchmark suite"""
    
    console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]  AEGIS PERFORMANCE BENCHMARK SUITE[/bold cyan]")
    console.print("[bold cyan]  BLAKE3 vs SHA-256 Analysis[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")
    
    scenarios = [
        {"count": 100, "size_kb": 10, "label": "100 files × 10KB"},
        {"count": 500, "size_kb": 10, "label": "500 files × 10KB"},
        {"count": 1000, "size_kb": 10, "label": "1K files × 10KB"},
        {"count": 100, "size_kb": 1024, "label": "100 files × 1MB"},
        {"count": 500, "size_kb": 1024, "label": "500 files × 1MB"},
    ]
    
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        
        task = progress.add_task("[cyan]Running benchmarks...", total=len(scenarios))
        
        for scenario in scenarios:
            console.print(f"\n[bold]Scenario:[/bold] {scenario['label']}")
            
            # Generate files
            test_dir = f"_benchmark_{scenario['count']}_{scenario['size_kb']}"
            files = generate_test_files(test_dir, scenario['count'], scenario['size_kb'])
            
            # Benchmark BLAKE3
            console.print("  Testing BLAKE3...", end=" ")
            blake3_time = benchmark_hash_function(files, blake3, "BLAKE3")
            console.print(f"[cyan]{blake3_time:.4f}s[/cyan]")
            
            # Benchmark SHA-256
            console.print("  Testing SHA-256...", end=" ")
            sha256_time = benchmark_hash_function(files, hashlib.sha256, "SHA256")
            console.print(f"[yellow]{sha256_time:.4f}s[/yellow]")
            
            # Calculate metrics
            speedup = sha256_time / blake3_time
            throughput_blake3 = (scenario['count'] * scenario['size_kb']) / blake3_time
            throughput_sha256 = (scenario['count'] * scenario['size_kb']) / sha256_time
            
            console.print(f"  [bold green]Speedup: {speedup:.2f}x[/bold green]")
            
            results.append({
                "scenario": scenario['label'],
                "file_count": scenario['count'],
                "file_size_kb": scenario['size_kb'],
                "blake3_time": round(blake3_time, 4),
                "sha256_time": round(sha256_time, 4),
                "speedup": round(speedup, 2),
                "throughput_blake3_kbps": round(throughput_blake3, 2),
                "throughput_sha256_kbps": round(throughput_sha256, 2)
            })
            
            # Cleanup
            shutil.rmtree(test_dir)
            progress.update(task, advance=1)
    
    # Save results
    with open('benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    console.print("\n[green]✓[/green] Benchmark complete: [yellow]benchmark_results.json[/yellow]")
    
    # Generate graphs
    generate_publication_graphs(results)
    
    return results


def generate_publication_graphs(results):
    """Generate IEEE-quality graphs"""
    
    console.print("\n[cyan]Generating publication-ready graphs...[/cyan]")
    
    scenarios = [r['scenario'] for r in results]
    blake3_times = [r['blake3_time'] for r in results]
    sha256_times = [r['sha256_time'] for r in results]
    speedups = [r['speedup'] for r in results]
    
    # Create figure with 2x2 subplots
    fig = plt.figure(figsize=(16, 12))
    
    # Plot 1: Performance Comparison
    ax1 = plt.subplot(2, 2, 1)
    x = np.arange(len(scenarios))
    width = 0.35
    
    ax1.bar(x - width/2, blake3_times, width, label='BLAKE3', color='#00d4aa', alpha=0.8)
    ax1.bar(x + width/2, sha256_times, width, label='SHA-256', color='#ff6b6b', alpha=0.8)
    ax1.set_xlabel('Test Scenario', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
    ax1.set_title('Hash Function Performance Comparison', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenarios, rotation=45, ha='right')
    ax1.legend(fontsize=10)
    ax1.grid(axis='y', alpha=0.3)
    
    # Plot 2: Speedup Analysis
    ax2 = plt.subplot(2, 2, 2)
    ax2.bar(scenarios, speedups, color='#4ecdc4', alpha=0.8)
    ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='Baseline (SHA-256)')
    ax2.set_xlabel('Test Scenario', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Speedup Factor (x)', fontsize=12, fontweight='bold')
    ax2.set_title('BLAKE3 Performance Advantage', fontsize=14, fontweight='bold')
    ax2.set_xticklabels(scenarios, rotation=45, ha='right')
    ax2.legend(fontsize=10)
    ax2.grid(axis='y', alpha=0.3)
    
    # Plot 3: Throughput Comparison
    ax3 = plt.subplot(2, 2, 3)
    throughput_blake3 = [r['throughput_blake3_kbps'] for r in results]
    throughput_sha256 = [r['throughput_sha256_kbps'] for r in results]
    
    ax3.plot(scenarios, throughput_blake3, marker='o', linewidth=2, markersize=8, label='BLAKE3', color='#00d4aa')
    ax3.plot(scenarios, throughput_sha256, marker='s', linewidth=2, markersize=8, label='SHA-256', color='#ff6b6b')
    ax3.set_xlabel('Test Scenario', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Throughput (KB/s)', fontsize=12, fontweight='bold')
    ax3.set_title('Throughput Analysis', fontsize=14, fontweight='bold')
    ax3.set_xticklabels(scenarios, rotation=45, ha='right')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Efficiency Ratio
    ax4 = plt.subplot(2, 2, 4)
    efficiency = [(b/s)*100 for b, s in zip(blake3_times, sha256_times)]
    
    ax4.bar(scenarios, efficiency, color='#9b59b6', alpha=0.8)
    ax4.axhline(y=100, color='red', linestyle='--', linewidth=2, label='100% (Equal Performance)')
    ax4.set_xlabel('Test Scenario', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Efficiency (%)', fontsize=12, fontweight='bold')
    ax4.set_title('BLAKE3 Efficiency Ratio', fontsize=14, fontweight='bold')
    ax4.set_xticklabels(scenarios, rotation=45, ha='right')
    ax4.legend(fontsize=10)
    ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('benchmark_results.png', dpi=300, bbox_inches='tight')
    console.print("[green]✓[/green] Graphs saved: [yellow]benchmark_results.png[/yellow]")
    
    # Generate summary table image
    generate_summary_table(results)


def generate_summary_table(results):
    """Generate summary statistics table"""
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.axis('tight')
    ax.axis('off')
    
    # Prepare table data
    table_data = [["Scenario", "BLAKE3 (s)", "SHA-256 (s)", "Speedup", "Throughput Gain"]]
    
    for r in results:
        throughput_gain = ((r['throughput_blake3_kbps'] - r['throughput_sha256_kbps']) / r['throughput_sha256_kbps']) * 100
        table_data.append([
            r['scenario'],
            f"{r['blake3_time']:.4f}",
            f"{r['sha256_time']:.4f}",
            f"{r['speedup']:.2f}x",
            f"+{throughput_gain:.1f}%"
        ])
    
    # Calculate averages
    avg_blake3 = np.mean([r['blake3_time'] for r in results])
    avg_sha256 = np.mean([r['sha256_time'] for r in results])
    avg_speedup = np.mean([r['speedup'] for r in results])
    
    table_data.append([
        "AVERAGE",
        f"{avg_blake3:.4f}",
        f"{avg_sha256:.4f}",
        f"{avg_speedup:.2f}x",
        "---"
    ])
    
    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                     colWidths=[0.3, 0.15, 0.15, 0.15, 0.15])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style header
    for i in range(5):
        table[(0, i)].set_facecolor('#667eea')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Style average row
    for i in range(5):
        table[(len(table_data)-1, i)].set_facecolor('#f0f0f0')
        table[(len(table_data)-1, i)].set_text_props(weight='bold')
    
    plt.title('Aegis Benchmark Summary - BLAKE3 vs SHA-256', fontsize=16, fontweight='bold', pad=20)
    plt.savefig('benchmark_summary_table.png', dpi=300, bbox_inches='tight')
    console.print("[green]✓[/green] Summary table: [yellow]benchmark_summary_table.png[/yellow]")


if __name__ == "__main__":
    results = run_comprehensive_benchmark()
    console.print("\n[bold green]═══════════════════════════════════════[/bold green]")
    console.print("[bold green]  BENCHMARK COMPLETE[/bold green]")
    console.print("[bold green]═══════════════════════════════════════[/bold green]")
