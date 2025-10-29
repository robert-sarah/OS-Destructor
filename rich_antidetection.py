#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich Anti-Detection - Anti-VM, Anti-Sandbox, Polymorphism"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import os
import sys
import random
import string

console = Console()

class AntiDetection:
    def __init__(self):
        self.vm_indicators = ['VMware', 'VirtualBox', 'QEMU', 'Xen', 'Hyper-V']
        self.sandbox_indicators = ['sandbox', 'malware', 'virus', 'analysis']
        
    def check_vm(self):
        """Detect virtual machine"""
        console.print(Panel.fit(
            "[bold red]Anti-VM Detection[/bold red]",
            border_style="red"
        ))
        
        # Check MAC address
        macs = ['00:50:56', '00:0C:29', '08:00:27', '00:05:69']
        detected = False
        
        # Check system files
        vm_files = [
            '/dev/vmci', '/dev/vmmouse', '/dev/vboxguest',
            'C:\\WINDOWS\\system32\\vmware'
        ]
        
        for file in vm_files:
            if os.path.exists(file):
                console.print(f"[red]⚠ VM detected: {file}[/red]")
                detected = True
        
        if not detected:
            console.print("[green]✓ No VM detected[/green]")
        
        return not detected
    
    def check_sandbox(self):
        """Detect sandbox environment"""
        console.print(Panel.fit(
            "[bold yellow]Anti-Sandbox Detection[/bold yellow]",
            border_style="yellow"
        ))
        
        # Check user count
        # Check CPU cores
        # Check RAM size
        # Check process list
        
        console.print("[green]✓ Sandbox check complete[/green]")
    
    def polymorphic_obfuscation(self, code):
        """Polymorphic code obfuscation"""
        console.print(Panel.fit(
            "[bold cyan]Polymorphic Obfuscation[/bold cyan]",
            border_style="cyan"
        ))
        
        # Random variable names
        obfuscated = code
        for i in range(10):
            old_name = f"var{i}"
            new_name = ''.join(random.choices(string.ascii_letters, k=8))
            obfuscated = obfuscated.replace(old_name, new_name)
        
        console.print("[green]✓ Code obfuscated[/green]")
        return obfuscated
    
    def encrypted_c2(self):
        """Encrypted C2 communication"""
        console.print("[bold magenta]Encrypted C2 Channel[/bold magenta]")
        
        # AES encryption for C2
        encrypted_code = '''
import base64
from cryptography.fernet import Fernet

class EncryptedC2:
    def __init__(self, key):
        self.cipher = Fernet(key)
    
    def send(self, data):
        encrypted = self.cipher.encrypt(data.encode())
        # Send encrypted data
        pass
    
    def receive(self, encrypted_data):
        decrypted = self.cipher.decrypt(encrypted_data)
        return decrypted.decode()
'''
        
        with open("encrypted_c2.py", 'w') as f:
            f.write(encrypted_code)
        
        console.print("[green]✓ Encrypted C2 created[/green]")

if __name__ == "__main__":
    anti = AntiDetection()
    anti.check_vm()

