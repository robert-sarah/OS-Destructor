#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Security Testing Framework - Rich Console Main
All modules are Rich console based (except ML which uses PyQt5)
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Prompt
from rich.progress import Progress
import sys
import os
import subprocess
import platform

console = Console()

# Cross-platform compatibility
IS_LINUX = platform.system() == 'Linux'
IS_WINDOWS = platform.system() == 'Windows'

class SecurityFramework:
    """Main framework menu"""
    
    def __init__(self):
        self.modules = {
            '1': ('Rich Keylogger', 'rich_keylogger.py', lambda: self.run_file('rich_keylogger.py')),
            '2': ('Rich Voicelogger', 'rich_voicelogger.py', lambda: self.run_file('rich_voicelogger.py')),
            '3': ('Rich Network Scanner', 'rich_network_scanner.py', lambda: self.run_file('rich_network_scanner.py')),
            '4': ('Rich Password Cracker', 'rich_password_cracker.py', lambda: self.run_file('rich_password_cracker.py')),
            '5': ('Rich Packet Sniffer', 'rich_packet_sniffer.py', lambda: self.run_file('rich_packet_sniffer.py')),
            '6': ('Android RAT', 'andro_rat.py', lambda: self.run_file('andro_rat.py')),
            '7': ('FaT RAT', 'fat_rat.py', lambda: self.run_file('fat_rat.py')),
            '8': ('Web Crawler', 'rich_web_crawler.py', lambda: self.run_file('rich_web_crawler.py')),
            '9': ('Hash Cracker', 'rich_hash_cracker.py', lambda: self.run_file('rich_hash_cracker.py')),
            '10': ('SQL Injection', 'rich_sql_injection.py', lambda: self.run_file('rich_sql_injection.py')),
            '11': ('XSS Fuzzer', 'rich_xss_fuzzer.py', lambda: self.run_file('rich_xss_fuzzer.py')),
            '12': ('DDoS Tool', 'rich_ddos.py', lambda: self.run_file('rich_ddos.py')),
            '13': ('WiFi Cracker Basic', 'rich_wifi_cracker.py', lambda: self.run_file('rich_wifi_cracker.py')),
            '13a': ('WiFi Advanced Attacks', 'rich_wifi_advanced.py', lambda: self.run_file('rich_wifi_advanced.py')),
            '14': ('Exploit Generator', 'rich_exploit_gen.py', lambda: self.run_file('rich_exploit_gen.py')),
            '15': ('Rootkit Hider', 'rich_rootkit.py', lambda: self.run_file('rich_rootkit.py')),
            '16': ('C2 Encrypted Server', 'rich_c2_server.py', lambda: self.run_file('rich_c2_server.py')),
            '17': ('Privilege Escalation', 'rich_privesc.py', lambda: self.run_file('rich_privesc.py')),
            '18': ('MITM Attack', 'rich_mitm.py', lambda: self.run_file('rich_mitm.py')),
            '19': ('Social Engineering', 'rich_social_engineer.py', lambda: self.run_file('rich_social_engineer.py')),
            '20': ('Post Exploitation', 'rich_post_exploit.py', lambda: self.run_file('rich_post_exploit.py')),
            '21': ('Mobile RAT Advanced', 'rich_mobile_rat.py', lambda: self.run_file('rich_mobile_rat.py')),
            '22': ('File Encrypter', 'rich_file_encrypter.py', lambda: self.run_file('rich_file_encrypter.py')),
            '23': ('Persistence Advanced', 'rich_persistence_advanced.py', lambda: self.run_file('rich_persistence_advanced.py')),
            '24': ('Steganography', 'rich_steganography.py', lambda: self.run_file('rich_steganography.py')),
            '25': ('Browser Hijacker', 'rich_browser_hijacker.py', lambda: self.run_file('rich_browser_hijacker.py')),
            '26': ('Advanced Malware Gen', 'rich_advanced_malware.py', lambda: self.run_file('rich_advanced_malware.py')),
            '27': ('WiFi ML AI Chat', 'rich_wifi_ml_ai.py', lambda: self.run_file('rich_wifi_ml_ai.py')),
            '28': ('Super Malware Gen', 'rich_super_malware.py', lambda: self.run_file('rich_super_malware.py')),
            '29': ('WiFi Radio Signal AI', 'rich_wifi_ml.py', lambda: self.run_file('rich_wifi_ml.py')),
            '30': ('ML Black Hat AI (GUI)', 'main.py', lambda: self.run_file('main.py'))
        }
        
    def show_menu(self):
        """Display main menu"""
        console.clear()
        # Platform detection
        platform_name = platform.system()
        
        console.print(Panel.fit(
            f"[bold cyan]╔═══════════════════════════════════╗[/bold cyan]\n"
            f"[bold cyan]║[/bold cyan]  [bold yellow]Security Testing Framework[/bold yellow]  [bold cyan]║[/bold cyan]\n"
            f"[bold cyan]║[/bold cyan]      [bold green]Rich Console Edition[/bold green]      [bold cyan]║[/bold cyan]\n"
            f"[bold cyan]║[/bold cyan]   [bold magenta]Platform: {platform_name}[/bold magenta]   [bold cyan]║[/bold cyan]\n"
            f"[bold cyan]╚═══════════════════════════════════╝[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        ))
        
        table = Table(title="Available Modules", box=box.DOUBLE, border_style="cyan")
        table.add_column("No.", style="cyan", width=4)
        table.add_column("Module", style="yellow")
        table.add_column("Description", style="green")
        
        descriptions = {
            '1': 'Professional keylogging tool',
            '2': 'Audio recording tool',
            '3': 'Network discovery and scanning',
            '4': 'Brute force password cracking',
            '5': 'Packet capture and analysis',
            '6': 'Android Remote Access Tool',
            '7': 'Advanced Fat RAT - Multi-platform',
            '8': 'Web crawler and scraper',
            '9': 'Advanced hash cracking (MD5, SHA, etc)',
            '10': 'SQL injection vulnerability scanner',
            '11': 'XSS vulnerability fuzzer',
            '12': 'DDoS attack tool',
            '13': 'WiFi password cracking',
            '13a': 'Advanced WiFi attacks (Evil Twin, WPS, KRACK)',
            '14': 'Exploit payload generator',
            '15': 'Rootkit - Process hiding',
            '16': 'Encrypted C2 server (SSL/TLS)',
            '17': 'Privilege escalation exploits',
            '18': 'Man-in-the-Middle attack',
            '19': 'Social engineering toolkit',
            '20': 'Post-exploitation & pivoting',
            '21': 'Advanced Mobile RAT',
            '22': 'File encryption (Ransomware-style)',
            '23': 'Advanced persistence mechanisms',
            '24': 'Steganography (hide data in images)',
            '25': 'Browser hijacking & modification',
            '26': 'Advanced malware generator',
            '27': 'WiFi ML AI - Chat interface with AI',
            '28': 'Super Malware - Multi-platform advanced',
            '29': 'WiFi Radio Signal Analysis - Predict passwords from signals',
            '30': 'ML Black Hat AI (GUI interface)'
        }
        
        for num, (name, _, _) in self.modules.items():
            table.add_row(num, name, descriptions.get(num, ''))
        
        console.print(table)
        console.print()
        
    def run_module(self, choice):
        """Run selected module"""
        if choice not in self.modules:
            console.print("[red]Invalid choice![/red]")
            return
        
        module_name, filename, runner = self.modules[choice]
        
        # Run the module
        try:
            runner()
        except KeyboardInterrupt:
            console.print("\n[yellow]Module interrupted[/yellow]")
        except Exception as e:
            console.print(f"[red]Error running module: {e}[/red]")
    
    def run_file(self, filename):
        """Run a Python file - Cross-platform"""
        if not os.path.exists(filename):
            console.print(f"[red]Module {filename} not found![/red]")
            console.print(f"[yellow]Creating {filename}...[/yellow]")
            return
        
        console.print(f"\n[bold green]Starting module...[/bold green]\n")
        
        # Cross-platform Python command
        if IS_LINUX:
            os.system(f'python3 {filename}')
        else:
            os.system(f'python {filename}')
    
    def main_loop(self):
        """Main application loop"""
        while True:
            self.show_menu()
            
            choice = Prompt.ask(
                "\n[bold cyan]Select module[/bold cyan]",
                choices=[str(i) for i in range(1, 31)] + ['13a'] + ['q', 'Q'],
                default='q'
            )
            
            if choice.lower() == 'q':
                console.print("\n[bold yellow]Exiting...[/bold yellow]")
                break
            
            self.run_module(choice)
            
            input("\nPress ENTER to return to menu...")

def main():
    framework = SecurityFramework()
    framework.main_loop()

if __name__ == '__main__':
    main()

