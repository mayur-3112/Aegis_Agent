#!/usr/bin/env python3
"""
Aegis Core Engine - Live Visualization Dashboard
Shows real-time file hashing progress with rich animations
"""

import os
import time
import json
from pathlib import Path
from blake3 import blake3
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.tree import Tree
from rich import box

console = Console()


def create_file_tree(directory: str, max_depth: int = 2) -> Tree:
    """Create visual file tree"""
    tree = Tree(f"📁 [bold cyan]{directory}[/bold cyan]")
    
    def add_items(parent, path, depth=0):
        if depth >= max_depth:
            return
        try:
            items = sorted(Path(path).iterdir(), key=lambda x: (not x.is_file(), x.name))
            for item in items[:10]:  # Limit to 10 items
                if item.is_file():
                    size = item.stat().st_size
                    branch = parent.add(f"📄 {item.name} [dim]({size} bytes)[/dim]")
                elif item.is_dir():
                    branch = parent.add(f"📁 [cyan]{item.name}[/cyan]")
                    add_items(branch, item, depth + 1)
        except PermissionError:
            pass
    
    add_items(tree, directory)
    return tree


def animate_hashing_process(files: list, output_baseline: str = "baseline.json"):
    """
    Animated visualization of the hashing process
    Shows file tree, progress, and live stats
    """
    
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=7),
        Layout(name="body"),
        Layout(name="footer", size=5)
    )
    
    # Header
    header = Panel(
        "[bold cyan]AEGIS CORE ENGINE[/bold cyan]\n"
        "[dim]Real-Time Cryptographic Snapshot Visualization[/dim]",
        box=box.DOUBLE,
        style="cyan"
    )
    
    # Progress tracking
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
    )
    
    task = progress.add_task("[cyan]Hashing files with BLAKE3...", total=len(files))
    
    baseline = {}
    processed_files = []
    total_bytes = 0
    start_time = time.time()
    
    with Live(layout, refresh_per_second=10, console=console) as live:
        layout["header"].update(header)
        
        for i, filepath in enumerate(files):
            try:
                # Hash the file
                stat_info = os.stat(filepath)
                size = stat_info.st_size
                mtime = stat_info.st_mtime
                
                hasher = blake3()
                with open(filepath, 'rb') as f:
                    while chunk := f.read(65536):
                        hasher.update(chunk)
                
                hex_hash = hasher.hexdigest()
                
                # Store result
                baseline[filepath] = {
                    "path": filepath,
                    "hash": hex_hash,
                    "size": size,
                    "mtime": mtime
                }
                
                processed_files.append({
                    "name": os.path.basename(filepath),
                    "size": size,
                    "hash": hex_hash[:16] + "..."
                })
                
                total_bytes += size
                
                # Update progress
                progress.update(task, advance=1)
                
                # Create stats table
                elapsed = time.time() - start_time
                throughput = total_bytes / elapsed if elapsed > 0 else 0
                
                stats_table = Table(show_header=False, box=box.SIMPLE)
                stats_table.add_column("Metric", style="bold")
                stats_table.add_column("Value", style="cyan")
                
                stats_table.add_row("Files Processed", f"{i+1}/{len(files)}")
                stats_table.add_row("Total Data", f"{total_bytes:,} bytes")
                stats_table.add_row("Throughput", f"{throughput/1024:.2f} KB/s")
                stats_table.add_row("Elapsed Time", f"{elapsed:.2f}s")
                stats_table.add_row("Algorithm", "BLAKE3")
                
                # Recent files table
                recent_table = Table(title="Recently Hashed", box=box.ROUNDED)
                recent_table.add_column("File", style="yellow")
                recent_table.add_column("Size", justify="right", style="cyan")
                recent_table.add_column("Hash Preview", style="dim")
                
                for recent in processed_files[-5:]:
                    recent_table.add_row(
                        recent["name"],
                        f"{recent['size']:,}",
                        recent["hash"]
                    )
                
                # Update layout
                body_layout = Layout()
                body_layout.split_row(
                    Layout(Panel(stats_table, title="Statistics", border_style="green"), name="stats"),
                    Layout(Panel(recent_table, border_style="yellow"), name="recent")
                )
                
                layout["body"].update(body_layout)
                layout["footer"].update(progress)
                
                # Small delay for visualization
                time.sleep(0.05)
                
            except Exception as e:
                console.print(f"[red]Error processing {filepath}: {e}[/red]")
                continue
    
    # Save baseline
    with open(output_baseline, 'w') as f:
        json.dump(baseline, f, indent=2)
    
    # Final summary
    elapsed_total = time.time() - start_time
    
    summary = Panel(
        f"[bold green]✓ Baseline Creation Complete[/bold green]\n\n"
        f"Files processed: [cyan]{len(baseline)}[/cyan]\n"
        f"Total data hashed: [cyan]{total_bytes:,}[/cyan] bytes\n"
        f"Time elapsed: [cyan]{elapsed_total:.2f}[/cyan] seconds\n"
        f"Average throughput: [cyan]{(total_bytes/elapsed_total)/1024:.2f}[/cyan] KB/s\n"
        f"Baseline saved to: [yellow]{output_baseline}[/yellow]",
        title="[bold]Cryptographic Snapshot Summary[/bold]",
        border_style="green",
        box=box.DOUBLE
    )
    
    console.print("\n")
    console.print(summary)
    
    return baseline


def visualize_integrity_check(old_baseline: dict, new_baseline: dict):
    """
    Animated visualization of integrity comparison
    """
    
    console.print("\n[bold cyan]━━━ INTEGRITY ANALYSIS VISUALIZATION ━━━[/bold cyan]\n")
    
    with console.status("[bold cyan]Analyzing file integrity...", spinner="dots12"):
        time.sleep(1)  # Dramatic pause
        
        old_keys = set(old_baseline.keys())
        new_keys = set(new_baseline.keys())
        
        created = sorted(new_keys - old_keys)
        deleted = sorted(old_keys - new_keys)
        
        common_keys = old_keys & new_keys
        modified = sorted([
            k for k in common_keys
            if old_baseline[k].get('hash') != new_baseline[k].get('hash')
        ])
    
    # Create comparison visualization
    comparison_tree = Tree("🔍 [bold]Integrity Analysis Results[/bold]")
    
    if modified:
        mod_branch = comparison_tree.add("🔴 [bold red]MODIFIED FILES[/bold red]")
        for path in modified[:10]:
            mod_branch.add(f"[yellow]{path}[/yellow]")
        if len(modified) > 10:
            mod_branch.add(f"[dim]... and {len(modified)-10} more[/dim]")
    
    if created:
        create_branch = comparison_tree.add("🟢 [bold green]CREATED FILES[/bold green]")
        for path in created[:10]:
            create_branch.add(f"[cyan]{path}[/cyan]")
        if len(created) > 10:
            create_branch.add(f"[dim]... and {len(created)-10} more[/dim]")
    
    if deleted:
        del_branch = comparison_tree.add("🟠 [bold orange3]DELETED FILES[/bold orange3]")
        for path in deleted[:10]:
            del_branch.add(f"[magenta]{path}[/magenta]")
        if len(deleted) > 10:
            del_branch.add(f"[dim]... and {len(deleted)-10} more[/dim]")
    
    if not (modified or created or deleted):
        comparison_tree.add("✅ [bold green]All files match baseline - SYSTEM SECURE[/bold green]")
    
    console.print(comparison_tree)
    console.print()


if __name__ == "__main__":
    import sys
    from engine import config_engine
    
    console.print("[bold cyan]Aegis Visualizer - Interactive Demo[/bold cyan]\n")
    
    # Load config
    try:
        files = config_engine.get_file_list("config.json")
        
        if not files:
            console.print("[red]No files found. Check config.json[/red]")
            sys.exit(1)
        
        # Show file tree
        console.print(Panel(create_file_tree("./test_data"), title="Monitored Files", border_style="cyan"))
        console.print()
        
        # Animate hashing
        baseline = animate_hashing_process(files, "baseline_visual.json")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
