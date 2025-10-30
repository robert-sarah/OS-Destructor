#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT Module - Open Source Intelligence Gathering
Target email enumeration and information gathering
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QGroupBox, QLineEdit,
                             QComboBox, QCheckBox, QMessageBox, QTableWidget,
                             QTableWidgetItem, QTreeWidget, QTreeWidgetItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import requests
import re
import os
from datetime import datetime
import whois
import socket
import dns.resolver
from modules.ai_conscience import AIConscience
ai_conscience = AIConscience()

class OSINTWorker(QThread):
    """Thread for OSINT gathering"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)
    
    def __init__(self, target):
        super().__init__()
        self.target = target
        
    def run(self):
        """Execute OSINT gathering"""
        results = {}
        
        try:
            # Ajout de la conscience IA pour chaque étape
            self.progress.emit('[AI Conscience] : ' + ai_conscience.ask(f'Comment OSINT peut être plus furtif et black hat sur {self.target}?'))
            # Check if it's an email or domain
            if '@' in self.target:
                results['type'] = 'email'
                email_parts = self.target.split('@')
                domain = email_parts[1]
                self.progress.emit("Gathering email information...")
                self.progress.emit('[AI Conscience] : ' + ai_conscience.ask(f'Comment exploiter l’email {self.target} au maximum?'))
                results['email'] = self.target
                results['username'] = email_parts[0]
                results['domain'] = domain
                # Check if email exists (using Have I Been Pwned API)
                self.progress.emit("Checking if email is compromised...")
                self.progress.emit('[AI Conscience] : ' + ai_conscience.ask(f'Comment utiliser les failles de {self.target}?'))
                results['compromised'] = self.check_email_breach(self.target)
                # Domain information
                self.progress.emit("Gathering domain information...")
                self.progress.emit('[AI Conscience] : ' + ai_conscience.ask(f'Comment attaquer le domaine {domain}?'))
                domain_info = self.get_domain_info(domain)
                results.update(domain_info)
            else:
                results['type'] = 'domain'
                results['domain'] = self.target
                self.progress.emit("Gathering domain information...")
                self.progress.emit('[AI Conscience] : ' + ai_conscience.ask(f'Comment exploiter le domaine {self.target} au maximum?'))
                domain_info = self.get_domain_info(self.target)
                results.update(domain_info)
                self.progress.emit("Scanning for associated emails...")
                self.progress.emit('[AI Conscience] : ' + ai_conscience.ask(f'Comment utiliser les emails associés à {self.target}?'))
                results['emails'] = self.find_associated_emails(self.target)
            self.progress.emit("Analysis complete!")
            self.progress.emit('[AI Conscience] : ' + ai_conscience.ask(f'Quels sont les prochains steps black hat sur {self.target}?'))
            self.finished.emit(results)
        except Exception as e:
            self.finished.emit({'error': str(e)})
    
    def check_email_breach(self, email):
        """Check if email has been in a data breach"""
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {
                'hibp-api-key': 'your-api-key-here',  # Get from haveibeenpwned.com
                'user-agent': 'OSINT-Tool'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                breaches = response.json()
                return [breach['Name'] for breach in breaches]
            return []
        except:
            return ["Unable to check"]
    
    def get_domain_info(self, domain):
        """Get domain information"""
        info = {}
        
        try:
            # WHOIS lookup
            w = whois.whois(domain)
            info['registrar'] = w.registrar if hasattr(w, 'registrar') else 'Unknown'
            info['creation_date'] = str(w.creation_date[0]) if isinstance(w.creation_date, list) else str(w.creation_date) if w.creation_date else 'Unknown'
            info['expiration_date'] = str(w.expiration_date[0]) if isinstance(w.expiration_date, list) else str(w.expiration_date) if w.expiration_date else 'Unknown'
            
            # DNS records
            try:
                answers = dns.resolver.resolve(domain, 'A')
                info['ip_address'] = [str(rdata) for rdata in answers]
            except:
                info['ip_address'] = ['Unable to resolve']
                
            # MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                info['mx_records'] = [str(rdata) for rdata in mx_records]
            except:
                info['mx_records'] = []
                
        except Exception as e:
            info['error'] = str(e)
        
        return info
    
    def find_associated_emails(self, domain):
        """Find common email addresses for a domain"""
        common_prefixes = ['admin', 'info', 'contact', 'support', 'sales', 
                          'webmaster', 'postmaster', 'noreply', 'hello']
        
        emails = []
        for prefix in common_prefixes:
            emails.append(f"{prefix}@{domain}")
        
        return emails

class OSINTModule(QWidget):
    """OSINT Module"""
    
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
        
        # Results
        results = self.create_results_section()
        main_layout.addWidget(results)
        
        # Logs
        logs = self.create_logs_section()
        main_layout.addWidget(logs)
        
        self.setLayout(main_layout)
        
    def create_header(self):
        """Create header"""
        header_box = QGroupBox()
        layout = QHBoxLayout()
        
        title = QLabel("OSINT - Open Source Intelligence")
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
        config_box = QGroupBox("Target Information")
        layout = QVBoxLayout()
        
        # Target
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Target Email or Domain:"))
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Entrez l'email ou le domaine cible")
        target_layout.addWidget(self.target_input)
        layout.addLayout(target_layout)
        
        # Search Type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Search Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Auto Detect",
            "Email",
            "Domain",
            "Company",
            "Social Media"
        ])
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # Options
        self.option_deep = QCheckBox("Deep Scan (Slower but more thorough)")
        layout.addWidget(self.option_deep)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_search = QPushButton("Gather Intelligence")
        btn_search.clicked.connect(self.start_osint)
        btn_layout.addWidget(btn_search)
        
        btn_export = QPushButton("Export Results")
        btn_export.clicked.connect(self.export_results)
        btn_layout.addWidget(btn_export)
        
        layout.addLayout(btn_layout)
        
        config_box.setLayout(layout)
        return config_box
        
    def create_results_section(self):
        """Create results section"""
        results_box = QGroupBox("Intelligence Results")
        layout = QVBoxLayout()
        
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabel("Information")
        layout.addWidget(self.results_tree)
        
        results_box.setLayout(layout)
        return results_box
        
    def create_logs_section(self):
        """Create logs section"""
        logs_box = QGroupBox("Activity Logs")
        layout = QVBoxLayout()
        
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setMaximumHeight(100)
        self.logs_text.setPlainText("Ready to gather intelligence.")
        
        layout.addWidget(self.logs_text)
        logs_box.setLayout(layout)
        return logs_box
        
    def start_osint(self):
        """Start OSINT gathering"""
        target = self.target_input.text()
        
        if not target:
            QMessageBox.warning(self, "Error", "Please enter a target")
            return
            
        self.logs_text.setPlainText(f"Starting OSINT on: {target}")
        self.results_tree.clear()
        
        self.worker = OSINTWorker(target)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_osint_complete)
        self.worker.start()
        
    def on_progress(self, message):
        """Progress callback"""
        self.logs_text.append(message)
        
    def on_osint_complete(self, results):
        """OSINT complete callback"""
        self.logs_text.append("✓ OSINT gathering complete!")
        
        # Display results in tree
        root = QTreeWidgetItem([f"Target: {self.target_input.text()}"])
        self.results_tree.addTopLevelItem(root)
        
        for key, value in results.items():
            if isinstance(value, list):
                item = QTreeWidgetItem([f"{key}: {', '.join(map(str, value))}"])
            else:
                item = QTreeWidgetItem([f"{key}: {value}"])
            root.addChild(item)
        
        self.results_tree.expandAll()
        
    def export_results(self):
        """Export results to file"""
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(log_dir, f"osint_results_{timestamp}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("OSINT Results\n")
            f.write("=" * 50 + "\n\n")
            
            def traverse_item(item):
                f.write(item.text(0) + "\n")
                for i in range(item.childCount()):
                    traverse_item(item.child(i))
            
            for i in range(self.results_tree.topLevelItemCount()):
                traverse_item(self.results_tree.topLevelItem(i))
        
        self.logs_text.append(f"Results exported to: {filename}")

