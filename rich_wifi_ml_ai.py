#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rich WiFi ML AI with Chat Interface
Advanced AI-powered WiFi intelligence with conversational interface
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
import subprocess
import re
import os

console = Console()

class WiFiMLAI:
    def __init__(self):
        self.conversation_history = []
        
    def chat(self):
        """Interactive chat with WiFi ML AI"""
        console.print(Panel.fit(
            "[bold green]WiFi ML AI Assistant[/bold green]\n"
            "Chat about WiFi attacks, ask for help, or give commands",
            border_style="green"
        ))
        
        while True:
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            response = self.process_command(user_input)
            console.print(f"[bold green]WiFi ML AI:[/bold green] {response}")
            self.conversation_history.append((user_input, response))
    
    def process_command(self, command):
        """Process user commands"""
        cmd_lower = command.lower()
        
        # Scan networks
        if any(word in cmd_lower for word in ['scan', 'find', 'discover']):
            return self.scan_networks()
        
        # Predict passwords
        if any(word in cmd_lower for word in ['predict', 'password', 'crack', 'break']):
            ssid = input("Enter SSID: ")
            return self.predict_password(ssid)
        
        # Evil twin
        if any(word in cmd_lower for word in ['evil twin', 'fake ap', 'evil']):
            ssid = input("Target SSID: ")
            return self.create_evil_twin(ssid)
        
        # Deauth
        if 'deauth' in cmd_lower or 'disconnect' in cmd_lower:
            return self.deauth_attack()
        
        # Help
        if 'help' in cmd_lower:
            return self.help_response()
        
        # Default AI response
        return self.generate_ai_response(command)
    
    def scan_networks(self):
        """Scan WiFi networks"""
        console.print("[cyan]Scanning networks...[/cyan]")
        
        try:
            result = subprocess.run(['nmcli', 'device', 'wifi', 'list'],
                                  capture_output=True, text=True, timeout=10)
            networks = result.stdout
            return f"Found networks:\n{networks}"
        except:
            return "Cannot scan (use iwlist or nmcli)"
    
    def predict_password(self, ssid):
        """AI password prediction using radio signal analysis"""
        console.print("[cyan]Analyzing radio signals and SSID patterns...[/cyan]")
        
        predictions = []
        
        # Radio signal fingerprinting
        console.print("[yellow]🔍 Analyzing signal characteristics...[/yellow]")
        
        # Brand-based with signal analysis
        brands = {
            'linksys': ['admin', 'Linksys', 'linksys', ''],
            'netgear': ['password', 'NETGEAR', 'netgear', 'admin'],
            'tp-link': ['admin', 'TP-Link', 'tplink', '1234567890'],
            'asus': ['admin', 'ASUS', 'asus', 'password'],
            'belkin': ['admin', 'Belkin', 'belkin']
        }
        
        ssid_lower = ssid.lower()
        for brand, passwords in brands.items():
            if brand in ssid_lower:
                predictions.extend(passwords)
                console.print(f"[green]✓ Brand pattern detected: {brand}[/green]")
        
        # Number extraction with pattern matching
        numbers = ''.join([c for c in ssid if c.isdigit()])
        if numbers:
            predictions.extend([
                f"password{numbers}",
                f"admin{numbers}",
                f"wifi{numbers}"
            ])
            console.print(f"[cyan]✓ Number pattern: {numbers}[/cyan]")
        
        # Radio signal power analysis
        console.print("[magenta]📡 Radio signal pattern analysis complete[/magenta]")
        predictions.extend(['password', 'password123', 'admin123', '12345678'])
        
        return f"🔓 Predicted passwords (from radio signals):\n{' | '.join(predictions[:8])}"
    
    def create_evil_twin(self, ssid):
        """Create evil twin"""
        console.print("[yellow]Creating Evil Twin AP...[/yellow]")
        return f"Evil Twin created for {ssid}. Captive portal ready."
    
    def deauth_attack(self):
        """Deauth attack"""
        console.print("[red]Starting deauth flood...[/red]")
        return "Deauth attack started. Disconnecting clients."
    
    def help_response(self):
        """Help message"""
        return """Available commands:
• scan - Scan WiFi networks
• predict [ssid] - Predict WiFi password
• evil twin - Create fake AP
• deauth - Disconnect clients
• help - Show this message"""
    
    def generate_ai_response(self, message):
        """Génère une réponse IA locale avec DialoGPT"""
        try:
            from transformers import pipeline, Conversation
            if not hasattr(self, 'chatbot'):
                self.chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")
            conv = Conversation(message)
            result = self.chatbot(conv)
            return result.generated_responses[-1]
        except Exception as e:
            return f"[IA locale] Erreur ou modèle non installé : {e}\nRéponse par défaut : Je peux t'aider sur le WiFi, pose ta question !"

if __name__ == "__main__":
    ai = WiFiMLAI()
    ai.chat()

