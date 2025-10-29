#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FaT RAT - Remote Access Trojan (RAT) Multi-plateforme
"""

import sys
import os
import socket
import threading

class FatRat:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server = None
        self.clients = []

    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"[+] FaT RAT server started on {self.host}:{self.port}")
        while True:
            client, addr = self.server.accept()
            print(f"[+] Connection from {addr}")
            self.clients.append(client)
            threading.Thread(target=self.handle_client, args=(client, addr)).start()

    def handle_client(self, client, addr):
        try:
            while True:
                data = client.recv(4096)
                if not data:
                    break
                print(f"[DATA] {addr}: {data.decode(errors='ignore')}")
                # Echo back for demo
                client.sendall(b'ACK')
        except Exception as e:
            print(f"[!] Error with {addr}: {e}")
        finally:
            client.close()
            print(f"[-] Disconnected {addr}")

if __name__ == "__main__":
    rat = FatRat()
    try:
        rat.start_server()
    except KeyboardInterrupt:
        print("[!] Server stopped by user.")
        sys.exit(0)
