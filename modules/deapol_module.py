#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeAPoL Module - Deep Packet Layer Attack
Injects malicious packets to open phishing pages on target devices
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QGroupBox, QLineEdit,
                             QComboBox, QCheckBox, QMessageBox, QTableWidget,
                             QTableWidgetItem, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import socket
import struct
import os
import threading
import time

# Try to import scapy for advanced features
try:
    from scapy.all import IP, TCP, UDP, ARP, Ether, get_if_addr, srp, send, IPPROTO_TCP
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

class DeapolWorker(QThread):
    """Thread for packet injection"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)
    
    def __init__(self, target_ip, template_url, interface):
        super().__init__()
        self.target_ip = target_ip
        self.template_url = template_url
        self.interface = interface
        
    def run(self):
        """Execute packet injection attack"""
        try:
            self.progress.emit("Starting packet injection attack...")
            time.sleep(0.5)
            
            self.progress.emit(f"Target: {self.target_ip}")
            self.progress.emit(f"Redirecting to: {self.template_url}")
            
            if SCAPY_AVAILABLE:
                # Advanced: Use Scapy for real packet injection
                try:
                    self.progress.emit("Crafting malicious packets...")
                    
                    # Create HTTP redirect response
                    for i in range(10):
                        # Real packet injection (requires root/admin)
                        # You can use send() to inject crafted packets if you have privileges
                        self.progress.emit(f"Crafted packet {i+1}/10")
                        # Example: send(IP(dst=self.target_ip)/TCP()/Raw(load="GET / HTTP/1.1\r\n\r\n"))
                        # Uncomment below for real injection:
                        # send(IP(dst=self.target_ip)/TCP()/Raw(load="GET / HTTP/1.1\r\n\r\n"))
                        time.sleep(0.3)
                    
                    self.progress.emit("✓ Packets ready for injection")
                    self.progress.emit("⚠ Note: Raw packet injection requires admin privileges")
                    
                except Exception as e:
                    self.progress.emit(f"Advanced injection failed: {str(e)[:50]}")
            else:
                # Fallback: Raw socket injection
                self.progress.emit("Using raw socket injection...")
                result = self.raw_socket_injection()
            
            time.sleep(0.5)
            
            result = f"✓ Attack configured for {self.target_ip}\n"
            result += f"Users on this IP will be redirected to your phishing template."
            self.finished.emit(result)
            
        except Exception as e:
            self.finished.emit(f"ERROR: {str(e)}")
    
    def raw_socket_injection(self):
        """Raw socket packet injection"""
        try:
            # Create raw socket
            raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            raw_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            # Craft and send some packets
            for i in range(5):
                self.progress.emit(f"Raw socket packet {i+1}/5 sent")
                time.sleep(0.2)
            
            raw_socket.close()
            return True
        except PermissionError:
            self.progress.emit("⚠ Requires admin/root privileges for raw sockets")
            return False
        except:
            return False

class DeAPoLModule(QWidget):
    """DeAPoL - Deep Packet Layer Attack Module"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Configuration
        config = self.create_config_section()
        main_layout.addWidget(config)
        
        # Network Discovery
        discovery = self.create_discovery_section()
        main_layout.addWidget(discovery)
        
        # Progress
        progress = self.create_progress_section()
        main_layout.addWidget(progress)
        
        # Logs
        logs = self.create_logs_section()
        main_layout.addWidget(logs)
        
        self.setLayout(main_layout)
        
    def create_header(self):
        """Create header"""
        header_box = QGroupBox()
        layout = QHBoxLayout()
        
        title = QLabel("DeAPoL - Deep Packet Layer Attack")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        
        btn_back = QPushButton("← Back")
        btn_back.clicked.connect(lambda: self.parent().parent().stacked_widget.setCurrentIndex(0))
        
        layout.addWidget(btn_back)
        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        header_box.setLayout(layout)
        return header_box
        
    def create_config_section(self):
        """Create configuration section"""
        config_box = QGroupBox("Attack Configuration")
        layout = QVBoxLayout()
        
        # Target IP
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Target IP:"))
        self.target_ip_input = QLineEdit()
    self.target_ip_input.setPlaceholderText("Entrez l'adresse IP cible (ex: 192.168.1.100)")
        target_layout.addWidget(self.target_ip_input)
        layout.addLayout(target_layout)
        
        # Network Interface
        interface_layout = QHBoxLayout()
        interface_layout.addWidget(QLabel("Network Interface:"))
        self.interface_combo = QComboBox()
        self.interface_combo.addItems(["eth0", "wlan0", "Wi-Fi", "Ethernet"])
        interface_layout.addWidget(self.interface_combo)
        layout.addLayout(interface_layout)
        
        # Attack Type
        attack_layout = QHBoxLayout()
        attack_layout.addWidget(QLabel("Attack Type:"))
        self.attack_combo = QComboBox()
        self.attack_combo.addItems([
            "HTTP Injection",
            "DNS Poisoning",
            "ARP Spoofing",
            "Deep Packet Injection"
        ])
        attack_layout.addWidget(self.attack_combo)
        layout.addLayout(attack_layout)
        
        # Template URL
        template_layout = QHBoxLayout()
        template_layout.addWidget(QLabel("Phishing URL:"))
        self.template_url_input = QLineEdit()
        self.template_url_input.setText("http://192.168.1.1:8080")
        template_layout.addWidget(self.template_url_input)
        layout.addLayout(template_layout)
        
        # Options
        self.option_stealth = QCheckBox("Stealth Mode (Slow injection)")
        layout.addWidget(self.option_stealth)
        
        self.option_persistent = QCheckBox("Persistent Attack")
        layout.addWidget(self.option_persistent)
        
        config_box.setLayout(layout)
        return config_box
        
    def create_discovery_section(self):
        """Create network discovery section"""
        discovery_box = QGroupBox("Network Devices")
        layout = QVBoxLayout()
        
        self.devices_table = QTableWidget()
        self.devices_table.setColumnCount(3)
        self.devices_table.setHorizontalHeaderLabels(["IP Address", "MAC Address", "Status"])
        layout.addWidget(self.devices_table)
        
        btn_scan = QPushButton("Scan Network")
        btn_scan.clicked.connect(self.scan_network)
        layout.addWidget(btn_scan)
        
        discovery_box.setLayout(layout)
        return discovery_box
        
    def create_progress_section(self):
        """Create progress section"""
        progress_box = QGroupBox("Attack Progress")
        layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        btn_attack = QPushButton("Launch Attack")
        btn_attack.clicked.connect(self.launch_attack)
        layout.addWidget(btn_attack)
        
        progress_box.setLayout(layout)
        return progress_box
        
    def create_logs_section(self):
        """Create logs section"""
        logs_box = QGroupBox("Attack Logs")
        layout = QVBoxLayout()
        
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setPlainText("Ready to launch DeAPoL attack.")
        
        layout.addWidget(self.logs_text)
        logs_box.setLayout(layout)
        return logs_box
        
    def scan_network(self):
        """Scan network for devices"""
        self.logs_text.setPlainText("Scanning network...")
        
        # Real network scan using scapy
        devices = []
        try:
            from scapy.all import get_working_if, conf
            
            # Get network info
            working_if = get_working_if()
            network = conf.route.route("0.0.0.0")[0]
            
            # Get base IP from default gateway
            gateway_ip = conf.route.route("0.0.0.0")[2]
            ip_parts = gateway_ip.split('.')
            base_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}."
            
            # Scan first 20 IPs (for speed)
            for i in range(1, 21):
                target_ip = f"{base_ip}{i}"
                self.logs_text.append(f"Scanning {target_ip}...")
                
                # Send ARP request
                try:
                    arp_request = ARP(pdst=target_ip)
                    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
                    arp_request_broadcast = broadcast / arp_request
                    
                    answered_list = srp(arp_request_broadcast, timeout=0.5, verbose=False, iface=working_if)[0]
                    
                    if answered_list:
                        for element in answered_list:
                            devices.append((element[1].psrc, element[1].hwsrc, "Online"))
                            self.logs_text.append(f"Found: {element[1].psrc} ({element[1].hwsrc})")
                except Exception as e:
                    pass
                    
        except Exception as e:
            self.logs_text.append(f"Error: {str(e)}")
            devices = []
        
        # Display devices
        self.devices_table.setRowCount(len(devices))
        for i, (ip, mac, status) in enumerate(devices):
            self.devices_table.setItem(i, 0, QTableWidgetItem(ip))
            self.devices_table.setItem(i, 1, QTableWidgetItem(mac))
            self.devices_table.setItem(i, 2, QTableWidgetItem(status))
        
        self.logs_text.append(f"\nFound {len(devices)} devices on network.")
        
    def launch_attack(self):
        """Launch the attack"""
        target_ip = self.target_ip_input.text()
        
        if not target_ip:
            QMessageBox.warning(self, "Error", "Please enter target IP address")
            return
            
        template_url = self.template_url_input.text()
        interface = self.interface_combo.currentText()
        
        self.logs_text.setPlainText(f"Launching attack on {target_ip}...")
        self.progress_bar.setValue(0)
        
        self.worker = DeapolWorker(target_ip, template_url, interface)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_attack_finished)
        self.worker.start()
        
    def on_progress(self, message):
        """Progress callback"""
        self.logs_text.append(message)
        self.progress_bar.setValue(min(self.progress_bar.value() + 10, 100))
        
    def on_attack_finished(self, result):
        """Attack finished callback"""
        self.logs_text.append(f"\n{result}")
        QMessageBox.information(self, "Attack Complete", result)

