#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich Hash Cracker"""

from rich.console import Console
from rich.progress import Progress
import hashlib

console = Console()

class HashCracker:
    def __init__(self):
        self.hash_functions = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256
        }
    
    def crack(self, target_hash, wordlist, hash_type='md5'):
        """Crack hash from wordlist"""
        console.print(f"[bold red]Cracking {hash_type.upper()} hash...[/bold red]")
        
        with open(wordlist, 'r') as f:
            words = f.readlines()
        
        with Progress() as progress:
            task = progress.add_task("Cracking...", total=len(words))
            
            for word in words:
                word = word.strip()
                hashed = self.hash_functions[hash_type](word.encode()).hexdigest()
                
                if hashed == target_hash:
                    console.print(f"[green]✓ Found: {word}[/green]")
                    return word
                
                progress.advance(task)
        
        console.print("[red]Hash not found in wordlist[/red]")

if __name__ == "__main__":
    cracker = HashCracker()
    console.print("[yellow]Hash cracker tool[/yellow]")

