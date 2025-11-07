#!/usr/bin/env python3
"""
Aegis Live Monitor - Real-time file integrity monitoring
Uses watchdog to detect changes instantly
"""

import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime

console = Console()


class AegisFileWatcher(FileSystemEventHandler):
    """Custom file system event handler"""
    
    def __init__(self):
        self.events = []
        self.max_events = 50
    
    def on_modified(self, event):
        if not event.is_directory:
            self.log_event("MODIFIED", event.src_path)
    
    def on_created(self, event):
        if not event.is_directory:
            self.log_event("CREATED", event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.log_event("DELETED", event.src_path)
    
    def log_event(self, event_type, filepath):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.events.append({
            'time': timestamp,
            'type': event_type,
            'file': Path(filepath).name,
            'path': filepath
        })
        
        # Keep only recent events
        if len(self.events) > self.max_events:
            self.events.pop(0)


def create_monitor_display(watcher: AegisFileWatcher, watched_dir: str) -> Panel:
    """Create live monitoring display"""
    
    # Event table
    table = Table(title="Recent File Events", box=box.ROUNDED, show_lines=True)
    table.add_column("Time", style="cyan", width=10)
    table.add_column("Event", style="yellow", width=12)
    table.add_column("File", style="green", width=30)
    table.add_column("Status", style="bold", width=15)
    
    # Add recent events (last 15)
    recent_events = watcher.events[-15:]
    
    if recent_events:
        for event in reversed(recent_events):
            event_type = event['type']
            
            if event_type == "MODIFIED":
                status = "[red]⚠ ALERT[/red]"
                style = "red"
            elif event_type == "CREATED":
                status = "[yellow]⚠ WARNING[/yellow]"
                style = "yellow"
            else:
                status = "[orange3]⚠ WARNING[/orange3]"
                style = "orange3"
            
            table.add_row(
                event['time'],
                f"[{style}]{event_type}[/{style}]",
                event['file'],
                status
            )
    else:
        table.add_row("--:--:--", "NO EVENTS", "Waiting for changes...", "[green]✓ SECURE[/green]")
    
    # Stats
    modified_count = sum(1 for e in watcher.events if e['type'] == 'MODIFIED')
    created_count = sum(1 for e in watcher.events if e['type'] == 'CREATED')
    deleted_count = sum(1 for e in watcher.events if e['type'] == 'DELETED')
    
    stats_text = f"""
[bold cyan]Aegis Live Monitor[/bold cyan]
[dim]Real-time File Integrity Monitoring[/dim]

[bold]Watched Directory:[/bold] [yellow]{watched_dir}[/yellow]
[bold]Total Events:[/bold] [cyan]{len(watcher.events)}[/cyan]

[bold red]Modified:[/bold red] {modified_count}
[bold yellow]Created:[/bold yellow] {created_count}
[bold orange3]Deleted:[/bold orange3] {deleted_count}

[dim]Press Ctrl+C to stop monitoring[/dim]
    """
    
    layout_content = stats_text + "\n\n" + table.__rich_console__(console, console.options)
    
    return Panel(
        table,
        title="[bold]🛡️  AEGIS LIVE MONITOR[/bold]",
        subtitle=f"[dim]Monitoring: {watched_dir}[/dim]",
        border_style="cyan",
        box=box.DOUBLE
    )


def start_live_monitoring(watch_dir: str = "./test_data"):
    """Start real-time file monitoring"""
    
    if not Path(watch_dir).exists():
        console.print(f"[red]Directory not found: {watch_dir}[/red]")
        return
    
    # Banner
    banner = Panel(
        "[bold cyan]AEGIS REAL-TIME MONITOR[/bold cyan]\n\n"
        "[yellow]⚡ Live file integrity monitoring active[/yellow]\n"
        "All file changes will be detected instantly",
        box=box.DOUBLE,
        border_style="cyan"
    )
    console.print(banner)
    console.print()
    
    # Setup watcher
    event_handler = AegisFileWatcher()
    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=True)
    observer.start()
    
    console.print(f"[green]✓[/green] Monitoring started: [yellow]{watch_dir}[/yellow]")
    console.print("[dim]Watching for file changes...\n[/dim]")
    
    try:
        with Live(create_monitor_display(event_handler, watch_dir), refresh_per_second=2, console=console) as live:
            while True:
                time.sleep(0.5)
                live.update(create_monitor_display(event_handler, watch_dir))
    
    except KeyboardInterrupt:
        observer.stop()
        console.print("\n\n[yellow]Monitoring stopped by user[/yellow]")
    
    observer.join()
    
    # Summary
    console.print(f"\n[bold cyan]Session Summary:[/bold cyan]")
    console.print(f"Total events captured: [cyan]{len(event_handler.events)}[/cyan]")


if __name__ == "__main__":
    import sys
    
    watch_directory = sys.argv[1] if len(sys.argv) > 1 else "./test_data"
    start_live_monitoring(watch_directory)
