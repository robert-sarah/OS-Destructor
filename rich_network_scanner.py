#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rich Network Scanner - Professional Network Discovery
Advanced network scanning with Rich console
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

console = Console()

class RichNetworkScanner:
    def __init__(self):
        self.active_hosts = []
        
    def scan_port(self, host, port, timeout=1):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return port if result == 0 else None
        except Exception:
            return None
            
    def scan_host(self, host, ports, progress):
        """Scan a host for open ports"""
        open_ports = []
        task = progress.add_task(f"[cyan]Scanning {host}...", total=len(ports))
        
        for port in ports:
            result = self.scan_port(host, port)
            if result:
                open_ports.append(port)
            progress.update(task, advance=1)
        
        if open_ports:
            self.active_hosts.append((host, open_ports))
        
        return host, open_ports
        
    def scan_network(self, network, common_ports=[22, 23, 25, 53, 80, 110, 443, 8080]):
        """Scan entire network"""
        console.print(Panel.fit(
            "[bold green]Rich Network Scanner[/bold green]\n"
            f"Scanning network: {network}",
            border_style="green"
        ))
        
        try:
            network_obj = ipaddress.ip_network(network, strict=False)
        except ValueError:
            console.print(f"[red]Invalid network: {network}[/red]")
            return
        
        with Progress(console=console) as progress:
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = []
                
                for host in network_obj.hosts():
                    future = executor.submit(self.scan_host, str(host), common_ports, progress)
                    futures.append(future)
                
                for future in as_completed(futures):
                    try:
                        host, ports = future.result()
                    except Exception as e:
                        pass
        
        # Display results
        self.display_results()
        
    def display_results(self):
        """Display scan results"""
        if not self.active_hosts:
            console.print("[yellow]No active hosts found[/yellow]")
            return
            
        table = Table(title="Active Hosts")
        table.add_column("IP Address", style="cyan")
        table.add_column("Open Ports", style="magenta")
        
        for host, ports in self.active_hosts:
            ports_str = ", ".join(map(str, ports))
            table.add_row(host, ports_str)
        
        console.print(table)
        console.print(f"\n[green]✓ Found {len(self.active_hosts)} active hosts[/green]")

if __name__ == "__main__":
    console.print(Panel.fit(
        "[bold cyan]Rich Network Scanner[/bold cyan]\n"
        "Professional network discovery tool"
    ))
    
    scanner = RichNetworkScanner()
    scanner.scan_network("192.168.1.0/24")

