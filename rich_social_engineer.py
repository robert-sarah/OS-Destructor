#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich Social Engineering Toolkit"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class SocialEngineer:
    def generate_email(self, template="business"):
        """Generate spear-phishing email"""
        console.print(Panel.fit(
            "[bold red]Spear-Phishing Email Generator[/bold red]",
            border_style="red"
        ))
        
        templates = {
            'business': '''
Subject: Urgent: Company Security Update Required

Dear Employee,

Our IT department has detected suspicious activity on your account.
Please verify your credentials immediately:

[LINK TO FAKE LOGIN PAGE]

This is mandatory to prevent account suspension.

IT Security Team
            ''',
            'personal': '''
Subject: Your Account Has Been Compromised

Hi there,

We detected someone tried to access your account from a new location.
Please confirm it was you by clicking here:

[PHISHING LINK]

If you didn't log in, secure your account immediately.

Security Team
            '''
        }
        
        email = templates.get(template, templates['business'])
        console.print(email)
        
        with open("phishing_email.txt", 'w') as f:
            f.write(email)
        
        console.print("[green]✓ Email saved[/green]")
    
    def usb_drop_attack(self):
        """USB drop attack payload"""
        console.print("[bold cyan]USB Drop Attack[/bold cyan]")
        
        payload = '''
# Autorun.inf for USB auto-execution
[Autorun]
Open=malware.exe
Icon=malware.exe
Action=Click here to open
Label=USB Storage
'''
        
        with open("autorun.inf", 'w') as f:
            f.write(payload)
        
        console.print("[green]✓ USB payload created[/green]")
    
    def qr_code_phishing(self):
        """Generate QR code phishing"""
        console.print("[bold yellow]QR Code Phishing[/bold yellow]")
        console.print("[yellow]Generate QR code linking to malicious site[/yellow]")
        
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data('https://evil-site.com/login')
        qr.make(fit=True)
        
        console.print("[green]✓ QR code generated[/green]")

if __name__ == "__main__":
    se = SocialEngineer()
    se.generate_email()

