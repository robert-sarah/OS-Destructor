#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rich Packet Sniffer - Network Traffic Analysis
Professional packet sniffing with Rich console
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
import socket
import struct
from datetime import datetime

console = Console()

class RichPacketSniffer:
    def __init__(self):
        self.packet_count = 0
        self.start_time = datetime.now()
        self.packets = []
        
    def parse_ip_header(self, data):
        """Parse IP header"""
        version_ihl = data[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
        ip_header_length = ihl * 4
        
        ttl, protocol, src, dest = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
        
        return {
            'version': version,
            'ihl': ihl,
            'ttl': ttl,
            'protocol': protocol,
            'src': socket.inet_ntoa(src),
            'dest': socket.inet_ntoa(dest)
        }
        
    def get_protocol_name(self, protocol_num):
        """Get protocol name from number"""
        protocols = {
            1: 'ICMP',
            6: 'TCP',
            17: 'UDP'
        }
        return protocols.get(protocol_num, 'UNKNOWN')
        
    def create_table(self):
        """Create packet capture table"""
        table = Table(title="Packet Sniffer - Active Monitoring")
        table.add_column("Source IP", style="cyan")
        table.add_column("Dest IP", style="yellow")
        table.add_column("Protocol", style="green")
        table.add_column("Packets", style="magenta")
        
        # Add last 5 packets
        for packet in self.packets[-5:]:
            table.add_row(
                packet['src'],
                packet['dest'],
                packet['protocol'],
                str(self.packet_count)
            )
        
        return table
        
    def start(self):
        """Start packet sniffing"""
        console.print(Panel.fit(
            "[bold red]Rich Packet Sniffer[/bold red]\n"
            "Capturing network traffic...",
            border_style="red"
        ))
        
        # Create raw socket
        try:
            sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            sniffer.bind(('0.0.0.0', 0))
            sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        except PermissionError:
            console.print("[red]ERROR: Requires admin/root privileges[/red]")
            return
        
        with Live(self.create_table(), refresh_per_second=2) as live:
            try:
                while True:
                    data, addr = sniffer.recvfrom(65535)
                    
                    try:
                        ip_header = self.parse_ip_header(data[:20])
                        protocol = self.get_protocol_name(ip_header['protocol'])
                        
                        self.packets.append({
                            'src': ip_header['src'],
                            'dest': ip_header['dest'],
                            'protocol': protocol
                        })
                        
                        self.packet_count += 1
                        live.update(self.create_table())
                        
                    except struct.error:
                        pass
                        
            except KeyboardInterrupt:
                console.print("\n[green]Capture stopped[/green]")
        
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sniffer.close()
        
        console.print(f"\n[green]✓ Captured {self.packet_count} packets[/green]")

if __name__ == "__main__":
    console.print(Panel.fit(
        "[bold cyan]Rich Packet Sniffer[/bold cyan]\n"
        "Professional network monitoring tool\n"
        "[yellow]⚠ Requires admin privileges[/yellow]"
    ))
    
    sniffer = RichPacketSniffer()
    sniffer.start()

