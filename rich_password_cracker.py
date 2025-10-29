#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rich Password Cracker - Brute Force Tool
Professional password cracking with Rich console
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import hashlib
import itertools
import string
import time

console = Console()

class RichPasswordCracker:
    def __init__(self):
        self.attempts = 0
        self.start_time = None
        
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def brute_force(self, target_hash, max_length=4):
        """Brute force password"""
        self.start_time = time.time()
        
        console.print(Panel.fit(
            "[bold red]Rich Password Cracker[/bold red]\n"
            "Brute forcing password...",
            border_style="red"
        ))
        
        charset = string.ascii_lowercase + string.digits
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Cracking...", total=None)
            
            for length in range(1, max_length + 1):
                progress.update(task, description=f"[cyan]Trying length {length}...")
                
                for attempt in itertools.product(charset, repeat=length):
                    password = ''.join(attempt)
                    self.attempts += 1
                    
                    if self.hash_password(password) == target_hash:
                        elapsed = time.time() - self.start_time
                        self.display_result(password, elapsed)
                        return password
                    
                    if self.attempts % 1000 == 0:
                        progress.update(task, description=f"[cyan]Attempts: {self.attempts}...")
        
        console.print("[red]Password not found[/red]")
        return None
        
    def display_result(self, password, elapsed):
        """Display cracking result"""
        table = Table(title="Password Cracked!")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Password", password)
        table.add_row("Attempts", str(self.attempts))
        table.add_row("Time Elapsed", f"{elapsed:.2f} seconds")
        table.add_row("Speed", f"{self.attempts/elapsed:.0f} attempts/sec")
        
        console.print(table)
        console.print(f"\n[green]✓ Password found: {password}[/green]")

if __name__ == "__main__":
    console.print(Panel.fit(
        "[bold cyan]Rich Password Cracker[/bold cyan]\n"
        "Professional brute force tool"
    ))
    
    # Example: crack password "abc"
    target_hash = hashlib.sha256(b"abc").hexdigest()
    
    cracker = RichPasswordCracker()
    cracker.brute_force(target_hash, max_length=3)

