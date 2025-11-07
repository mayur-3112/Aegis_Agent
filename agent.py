# agent.py - The Central Nervous System (Enhanced Professional Edition)
# Architect: Mayur
# Version: 2.0 - Production Grade with Rich Reporting

import argparse
import sys
import json
from dataclasses import asdict
from pathlib import Path

# Core Engine Imports
from engine import config_engine
from engine import baseline_engine
from engine import integrity_engine

# Rich Reporting Imports
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich import box

# Initialize Rich Console
console = Console()


def print_banner():
    """Display professional Aegis banner with system info"""
    banner = """
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║         █████╗ ███████╗ ██████╗ ██╗███████╗         ║
║        ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝         ║
║        ███████║█████╗  ██║  ███╗██║███████╗         ║
║        ██╔══██║██╔══╝  ██║   ██║██║╚════██║         ║
║        ██║  ██║███████╗╚██████╔╝██║███████║         ║
║        ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝         ║
║                                                       ║
║         Core Engine v2.0 - Production Edition         ║
║       File Integrity Monitoring System (BLAKE3)       ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")
    console.print("    [dim]High-Performance Cryptographic Integrity Engine[/dim]\n")


def save_baseline(filepath: str, data: dict):
    """Saves the baseline dictionary to a JSON file with rich feedback"""
    serializable_data = {path: asdict(entry) for path, entry in data.items()}
    
    try:
        with console.status(f"[bold cyan]Writing baseline to disk...", spinner="dots"):
            with open(filepath, 'w') as f:
                json.dump(serializable_data, f, indent=4)
        
        file_size = Path(filepath).stat().st_size
        console.print(f"[bold green]✓[/bold green] Baseline saved successfully")
        console.print(f"  [dim]Location:[/dim] [yellow]{filepath}[/yellow]")
        console.print(f"  [dim]Size:[/dim] [cyan]{file_size:,}[/cyan] bytes\n")
        
    except IOError as e:
        console.print(f"[bold red]✗[/bold red] Failed to write baseline: {e}", style="red")
        raise Exception(f"Failed to write baseline to {filepath}: {e}")


def load_baseline(filepath: str) -> dict:
    """Loads the baseline dictionary from a JSON file with validation"""
    try:
        if not Path(filepath).exists():
            return {}
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        console.print(f"[bold green]✓[/bold green] Loaded baseline from [yellow]{filepath}[/yellow]")
        console.print(f"  [dim]Files tracked:[/dim] [cyan]{len(data):,}[/cyan]\n")
        return data
        
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        console.print(f"[bold red]✗[/bold red] Corrupted baseline file: {e}", style="red")
        raise Exception(f"Failed to parse baseline file {filepath}: {e}")


def report_integrity_results(results: dict, output_file: str = "integrity_report.json"):
    """Display rich, color-coded integrity check results"""
    
    modified = results.get('MODIFIED', [])
    created = results.get('CREATED', [])
    deleted = results.get('DELETED', [])
    
    total_changes = len(modified) + len(created) + len(deleted)
    
    # Save detailed JSON report for forensics
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    console.print("\n" + "=" * 60)
    
    # System Status Summary
    if total_changes == 0:
        status_panel = Panel(
            "[bold green]✓ SYSTEM SECURE[/bold green]\n\n"
            "No unauthorized changes detected.\n"
            "All monitored files match the baseline.",
            title="[bold]Integrity Check Results[/bold]",
            border_style="green",
            box=box.DOUBLE
        )
        console.print(status_panel)
        console.print(f"\n[dim]Detailed report saved to: {output_file}[/dim]\n")
        return True
    
    # Security breach detected
    status_panel = Panel(
        f"[bold red]⚠️  SECURITY ALERT[/bold red]\n\n"
        f"[yellow]{total_changes}[/yellow] unauthorized changes detected!\n"
        f"Immediate investigation required.",
        title="[bold red]Integrity Violation Detected[/bold red]",
        border_style="red",
        box=box.DOUBLE
    )
    console.print(status_panel)
    console.print()
    
    # Modified Files Table (CRITICAL SEVERITY)
    if modified:
        table = Table(
            title="🔴 MODIFIED FILES - CRITICAL SEVERITY",
            box=box.ROUNDED,
            style="red",
            title_style="bold red"
        )
        table.add_column("File Path", style="yellow", no_wrap=False)
        table.add_column("Status", justify="center", style="red bold")
        table.add_column("Severity", justify="center", style="red bold")
        
        for path in modified:
            table.add_row(path, "MODIFIED", "CRITICAL")
        
        console.print(table)
        console.print()
    
    # Created Files Table (WARNING SEVERITY)
    if created:
        table = Table(
            title="🟡 CREATED FILES - WARNING",
            box=box.ROUNDED,
            style="yellow",
            title_style="bold yellow"
        )
        table.add_column("File Path", style="cyan", no_wrap=False)
        table.add_column("Status", justify="center", style="yellow bold")
        table.add_column("Severity", justify="center", style="yellow bold")
        
        for path in created:
            table.add_row(path, "NEW FILE", "WARNING")
        
        console.print(table)
        console.print()
    
    # Deleted Files Table (WARNING SEVERITY)
    if deleted:
        table = Table(
            title="🟠 DELETED FILES - WARNING",
            box=box.ROUNDED,
            style="orange3",
            title_style="bold orange3"
        )
        table.add_column("File Path", style="magenta", no_wrap=False)
        table.add_column("Status", justify="center", style="orange3 bold")
        table.add_column("Severity", justify="center", style="orange3 bold")
        
        for path in deleted:
            table.add_row(path, "DELETED", "WARNING")
        
        console.print(table)
        console.print()
    
    # Summary Statistics
    summary_table = Table(box=box.SIMPLE, show_header=False)
    summary_table.add_column("Metric", style="bold")
    summary_table.add_column("Count", justify="right")
    
    summary_table.add_row("Total Changes", f"[bold red]{total_changes}[/bold red]")
    summary_table.add_row("Modified Files", f"[red]{len(modified)}[/red]")
    summary_table.add_row("Created Files", f"[yellow]{len(created)}[/yellow]")
    summary_table.add_row("Deleted Files", f"[orange3]{len(deleted)}[/orange3]")
    
    console.print(Panel(summary_table, title="[bold]Change Summary[/bold]", border_style="cyan"))
    console.print(f"\n[dim]📄 Detailed forensic report: {output_file}[/dim]\n")
    
    return False


def main():
    """The main entry point and logic controller for the Aegis Core Engine"""
    
    parser = argparse.ArgumentParser(
        description="Aegis Core Engine v2.0: Professional File Integrity Monitoring System",
        epilog="Example: python agent.py --check --config config.json",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--init',
        action='store_true',
        help='Initialize a new baseline snapshot of monitored files'
    )
    
    parser.add_argument(
        '--check',
        action='store_true',
        help='Perform integrity check against existing baseline'
    )
    
    parser.add_argument(
        '--config',
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )
    
    parser.add_argument(
        '--baseline',
        default='baseline.json',
        help='Path to baseline file (default: baseline.json)'
    )
    
    parser.add_argument(
        '--output',
        default='integrity_report.json',
        help='Path to integrity report output (default: integrity_report.json)'
    )
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        print_banner()
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    args = parser.parse_args()
    
    # Display banner
    print_banner()
    
    # BASELINE INITIALIZATION MODE
    if args.init:
        console.print(f"[bold cyan]━━━ BASELINE INITIALIZATION MODE ━━━[/bold cyan]\n")
        console.print(f"[bold]Configuration:[/bold] [yellow]{args.config}[/yellow]")
        console.print(f"[bold]Baseline Output:[/bold] [yellow]{args.baseline}[/yellow]\n")
        
        try:
            # Step 1: Discovery Phase
            with console.status("[bold cyan]Running discovery engine...", spinner="dots"):
                files_to_scan = config_engine.get_file_list(args.config)
            
            if not files_to_scan:
                console.print("[bold red]✗[/bold red] No files found to scan. Check your config.", style="red")
                sys.exit(1)
            
            console.print(f"[bold green]✓[/bold green] Discovery complete: [cyan]{len(files_to_scan):,}[/cyan] files found\n")
            
            # Step 2: Baseline Creation Phase
            console.print("[bold cyan]Starting cryptographic snapshot...[/bold cyan]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                
                task = progress.add_task(
                    "[cyan]Hashing files with BLAKE3...",
                    total=len(files_to_scan)
                )
                
                # Create baseline (wrapped for progress visualization)
                baseline = baseline_engine.create_baseline(files_to_scan)
                progress.update(task, completed=len(files_to_scan))
            
            console.print(f"\n[bold green]✓[/bold green] Baseline creation complete: [cyan]{len(baseline):,}[/cyan] files hashed\n")
            
            # Step 3: Save Baseline
            save_baseline(args.baseline, baseline)
            
            # Success Summary
            success_panel = Panel(
                f"[bold green]Baseline initialization successful![/bold green]\n\n"
                f"Files processed: [cyan]{len(baseline):,}[/cyan]\n"
                f"Cryptographic algorithm: [yellow]BLAKE3[/yellow]\n"
                f"Baseline stored: [yellow]{args.baseline}[/yellow]",
                title="[bold]✓ Initialization Complete[/bold]",
                border_style="green"
            )
            console.print(success_panel)
            
        except Exception as e:
            console.print(f"\n[bold red]✗ FATAL ERROR[/bold red]: {e}", style="red")
            console.print("[dim]Check configuration and file permissions.[/dim]")
            sys.exit(1)
    
    # INTEGRITY CHECK MODE
    elif args.check:
        console.print(f"[bold cyan]━━━ INTEGRITY CHECK MODE ━━━[/bold cyan]\n")
        console.print(f"[bold]Configuration:[/bold] [yellow]{args.config}[/yellow]")
        console.print(f"[bold]Baseline Reference:[/bold] [yellow]{args.baseline}[/yellow]\n")
        
        try:
            # Step 1: Load existing baseline
            old_baseline = load_baseline(args.baseline)
            
            if not old_baseline:
                console.print(
                    f"[bold red]✗[/bold red] Baseline file '{args.baseline}' not found or empty.",
                    style="red"
                )
                console.print("[yellow]→[/yellow] Run with [cyan]--init[/cyan] first to create a baseline.\n")
                sys.exit(1)
            
            # Step 2: Discovery Phase
            with console.status("[bold cyan]Running discovery engine...", spinner="dots"):
                files_to_scan = config_engine.get_file_list(args.config)
            
            console.print(f"[bold green]✓[/bold green] Discovery complete: [cyan]{len(files_to_scan):,}[/cyan] files found\n")
            
            # Step 3: Create Fresh Snapshot
            console.print("[bold cyan]Creating fresh cryptographic snapshot...[/bold cyan]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                
                task = progress.add_task(
                    "[cyan]Hashing files with BLAKE3...",
                    total=len(files_to_scan)
                )
                
                new_baseline_raw = baseline_engine.create_baseline(files_to_scan)
                progress.update(task, completed=len(files_to_scan))
            
            console.print(f"\n[bold green]✓[/bold green] Fresh snapshot complete: [cyan]{len(new_baseline_raw):,}[/cyan] files hashed\n")
            
            # Step 4: Serialize for comparison
            new_baseline = {path: asdict(entry) for path, entry in new_baseline_raw.items()}
            
            # Step 5: Integrity Comparison
            console.print("[bold cyan]Analyzing integrity violations...[/bold cyan]")
            
            with console.status("[bold cyan]Comparing baselines...", spinner="dots"):
                results = integrity_engine.compare_baselines(old_baseline, new_baseline)
            
            # Step 6: Display Rich Report
            is_secure = report_integrity_results(results, args.output)
            
            # Exit with appropriate code
            sys.exit(0 if is_secure else 1)
            
        except Exception as e:
            console.print(f"\n[bold red]✗ FATAL ERROR[/bold red]: {e}", style="red")
            console.print("[dim]Check baseline file and permissions.[/dim]")
            sys.exit(1)
    
    console.print("[bold cyan]━━━ Aegis Core Engine Shutdown ━━━[/bold cyan]\n")


if __name__ == "__main__":
    main()
