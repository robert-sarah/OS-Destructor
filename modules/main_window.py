#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de la fenêtre principale
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QGroupBox, QGridLayout)
from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QFont, QPalette, QColor
import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class MainWindow(QWidget):
    """Fenêtre principale avec menu de navigation"""
    
    navigate = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        main_layout = QVBoxLayout()
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Welcome section
        welcome = self.create_welcome_section()
        main_layout.addWidget(welcome)
        
        # Available modules
        modules = self.create_modules_section()
        main_layout.addWidget(modules)
        
        # Logs/Console
        console = self.create_console_section()
        main_layout.addWidget(console)
        
        self.setLayout(main_layout)
        
    def create_header(self):
        """Crée l'en-tête de l'application"""
        header_box = QGroupBox()
        header_layout = QVBoxLayout()
        
        title = QLabel("Security Testing Framework")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Professional Security Testing Framework")
        subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_box.setLayout(header_layout)
        
        return header_box
        
    def create_welcome_section(self):
        """Create welcome section"""
        welcome_box = QGroupBox("Welcome")
        welcome_layout = QVBoxLayout()
        
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(100)
        welcome_msg = """
        <h3>Welcome to Security Testing Framework</h3>
        <p>This tool is designed for cybersecurity professionals and pentesters.</p>
        <p><b>⚠️ Use this framework ONLY on systems you own or have authorization to test.</b></p>
        <p>Select a module below to begin.</p>
        """
        info_text.setHtml(welcome_msg)
        welcome_layout.addWidget(info_text)
        welcome_box.setLayout(welcome_layout)
        
        return welcome_box
        
    def create_modules_section(self):
        """Create available modules section"""
        modules_box = QGroupBox("Available Modules")
        modules_layout = QGridLayout()
        
        # Module Phishing
        btn_phishing = QPushButton("Module Phishing")
        btn_phishing.setMinimumHeight(60)
        btn_phishing.clicked.connect(lambda: self.navigate.emit('phishing'))
        modules_layout.addWidget(btn_phishing, 0, 0)
        
        # Module Clonage
        btn_cloning = QPushButton("Module Clonage")
        btn_cloning.setMinimumHeight(60)
        btn_cloning.clicked.connect(lambda: self.navigate.emit('cloning'))
        modules_layout.addWidget(btn_cloning, 0, 1)
        
        # Module Reconnaissance
        btn_recon = QPushButton("Module Reconnaissance")
        btn_recon.setMinimumHeight(60)
        btn_recon.clicked.connect(lambda: self.navigate.emit('recon'))
        modules_layout.addWidget(btn_recon, 1, 0)
        
        # Module Payloads
        btn_payload = QPushButton("Module Payloads")
        btn_payload.setMinimumHeight(60)
        btn_payload.clicked.connect(lambda: self.navigate.emit('payload'))
        modules_layout.addWidget(btn_payload, 1, 1)
        
        # Module Attaques Web
        btn_webattack = QPushButton("Module Attaques Web")
        btn_webattack.setMinimumHeight(60)
        btn_webattack.clicked.connect(lambda: self.navigate.emit('webattack'))
        modules_layout.addWidget(btn_webattack, 2, 0)
        
        # Module DeAPoL
        btn_deapol = QPushButton("DeAPoL - Network Attack")
        btn_deapol.setMinimumHeight(60)
        btn_deapol.clicked.connect(lambda: self.navigate.emit('deapol'))
        modules_layout.addWidget(btn_deapol, 2, 1)
        
        # Module Email Campaign
        btn_email = QPushButton("Email Campaign")
        btn_email.setMinimumHeight(60)
        btn_email.clicked.connect(lambda: self.navigate.emit('email'))
        modules_layout.addWidget(btn_email, 3, 0)
        
        # Module OSINT
        btn_osint = QPushButton("OSINT Intelligence")
        btn_osint.setMinimumHeight(60)
        btn_osint.clicked.connect(lambda: self.navigate.emit('osint'))
        modules_layout.addWidget(btn_osint, 3, 1)
        
        # Module SEToolkit
        btn_setoolkit = QPushButton("SEToolkit Advanced")
        btn_setoolkit.setMinimumHeight(60)
        btn_setoolkit.clicked.connect(lambda: self.navigate.emit('setoolkit'))
        modules_layout.addWidget(btn_setoolkit, 4, 0)
        
        # Module ML Black Hat
        btn_ml = QPushButton("ML Black Hat AI")
        btn_ml.setMinimumHeight(60)
        btn_ml.clicked.connect(lambda: self.navigate.emit('ml_blackhat'))
        modules_layout.addWidget(btn_ml, 4, 1)
        
        modules_box.setLayout(modules_layout)
        return modules_box
        
    def create_console_section(self):
        """Create console section"""
        console_box = QGroupBox("Console")
        console_layout = QVBoxLayout()
        
        self.console_text = QTextEdit()
        self.console_text.setReadOnly(True)
        self.console_text.setMaximumHeight(120)
        
        # Initial log
        self.log_message("Console initialized. Application ready.")
        
        console_layout.addWidget(self.console_text)
        console_box.setLayout(console_layout)
        
        return console_box
        
    def log_message(self, message):
        """Add message to console with rich formatting"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.console_text.append(formatted_message)
        
        # Also log to Rich console
        try:
            console = Console()
            console.print(f"[dim][{timestamp}][/] {message}")
        except:
            pass

