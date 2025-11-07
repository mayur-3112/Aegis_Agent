from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from typing import Dict, List
import json

console = Console()

def print_banner():
    """Display professional Aegis banner"""
    banner = """
    ╔═══════════════════════════════════════════╗
    ║         AEGIS CORE ENGINE v1.0            ║
    ║    File Integrity Monitoring System       ║
    ║         BLAKE3 Performance Edition        ║
    ╚═══════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")

def report_baseline_creation(total_files: int, baseline_path: str):
    """Professional baseline creation report"""
    console.print(f"\n[bold green]✓[/bold green] Baseline created successfully")
    console.print(f"   Files processed: [cyan]{total_files}[/cyan]")
    console.print(f"   Saved to: [yellow]{baseline_path}[/yellow]\n")

def report_integrity_check(results: Dict[str, List[str]]) -> bool:
    """Rich visual integrity check report with severity indicators"""
    
    modified = results.get('MODIFIED', [])
    created = results.get('CREATED', [])
    deleted = results.get('DELETED', [])
    
    total_changes = len(modified) + len(created) + len(deleted)
    
    if total_changes == 0:
        console.print(Panel(
            "[bold green]✓ SYSTEM SECURE[/bold green]\n\nNo unauthorized changes detected.",
            title="Integrity Check Results",
            border_style="green"
        ))
        return True
    
    # Security breach detected
    console.print(Panel(
        f"[bold red]⚠ SECURITY ALERT[/bold red]\n\n{total_changes} unauthorized changes detected!",
        title="Integrity Check Results",
        border_style="red"
    ))
    
    # Modified files (CRITICAL)
    if modified:
        table = Table(title="Modified Files (CRITICAL)", style="red")
        table.add_column("Path", style="yellow")
        table.add_column("Status", style="red bold")
        for path in modified:
            table.add_row(path, "MODIFIED")
        console.print(table)
    
    # Created files (WARNING)
    if created:
        table = Table(title="Created Files (WARNING)", style="yellow")
        table.add_column("Path", style="cyan")
        table.add_column("Status", style="yellow bold")
        for path in created:
            table.add_row(path, "NEW FILE")
        console.print(table)
    
    # Deleted files (WARNING)
    if deleted:
        table = Table(title="Deleted Files (WARNING)", style="orange3")
        table.add_column("Path", style="magenta")
        table.add_column("Status", style="orange3 bold")
        for path in deleted:
            table.add_row(path, "DELETED")
        console.print(table)
    
    return False

def display_progress(total: int, description: str = "Processing"):
    """Return progress bar context manager"""
    return Progress().task(total=total, description=description)
