#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de génération de payloads
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QGroupBox, QLineEdit,
                             QComboBox, QCheckBox, QSpinBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import base64

class PayloadWorker(QThread):
    """Thread de travail pour la génération de payloads"""
    finished = pyqtSignal(str)
    
    def __init__(self, payload_type, host, port):
        super().__init__()
        self.payload_type = payload_type
        self.host = host
        self.port = port
        
    def run(self):
        """Génère le payload"""
        import time
        time.sleep(1)
        
        payload = f"payload_{self.payload_type}_{self.host}_{self.port}"
        encoded = base64.b64encode(payload.encode()).decode()
        
        result = f"Payload {self.payload_type} généré:\n{encoded}"
        self.finished.emit(result)
    payload = f"payload_{self.payload_type}_{self.host}_{self.port}"
    encoded = base64.b64encode(payload.encode()).decode()
    result = f"Payload {self.payload_type} généré:\n{encoded}"
    self.finished.emit(result)

class PayloadModule(QWidget):
    """Module de génération de payloads"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        main_layout = QVBoxLayout()
        
        # En-tête
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Configuration
        config = self.create_config_section()
        main_layout.addWidget(config)
        
        # Sortie
        output = self.create_output_section()
        main_layout.addWidget(output)
        
        # Actions
        actions = self.create_actions_section()
        main_layout.addWidget(actions)
        
        self.setLayout(main_layout)
        
    def create_header(self):
        """Crée l'en-tête du module"""
        header_box = QGroupBox()
        layout = QHBoxLayout()
        
        title = QLabel("Module Payloads")
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
        """Crée la section de configuration"""
        config_box = QGroupBox("Configuration du payload")
        layout = QVBoxLayout()
        
        # Type de payload
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Reverse Shell",
            "Bind Shell",
            "Meterpreter",
            "Web Shell"
        ])
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # Host
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("Host:"))
        self.host_input = QLineEdit()
        self.host_input.setText("192.168.1.100")
        host_layout.addWidget(self.host_input)
        layout.addLayout(host_layout)
        
        # Port
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port:"))
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1, 65535)
        self.port_spin.setValue(4444)
        port_layout.addWidget(self.port_spin)
        layout.addLayout(port_layout)
        
        # Système d'exploitation
        os_layout = QHBoxLayout()
        os_layout.addWidget(QLabel("OS:"))
        self.os_combo = QComboBox()
        self.os_combo.addItems(["Linux", "Windows", "macOS"])
        os_layout.addWidget(self.os_combo)
        layout.addLayout(os_layout)
        
        config_box.setLayout(layout)
        return config_box
        
    def create_output_section(self):
        """Crée la section de sortie"""
        output_box = QGroupBox("Payload généré")
        layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlainText("Aucun payload généré pour le moment.")
        
        layout.addWidget(self.output_text)
        output_box.setLayout(layout)
        return output_box
        
    def create_actions_section(self):
        """Crée la section des actions"""
        actions_box = QGroupBox("Actions")
        layout = QHBoxLayout()
        
        btn_generate = QPushButton("Générer le payload")
        btn_generate.clicked.connect(self.generate_payload)
        layout.addWidget(btn_generate)
        
        btn_copy = QPushButton("Copier")
        btn_copy.clicked.connect(self.copy_payload)
        layout.addWidget(btn_copy)
        
        btn_encode = QPushButton("Encoder")
        btn_encode.clicked.connect(self.encode_payload)
        layout.addWidget(btn_encode)
        
        layout.addStretch()
        
        actions_box.setLayout(layout)
        return actions_box
        
    def generate_payload(self):
        """Génère le payload"""
        payload_type = self.type_combo.currentText()
        host = self.host_input.text()
        port = self.port_spin.value()
        
        self.output_text.setPlainText("Génération en cours...")
        
        self.worker = PayloadWorker(payload_type, host, port)
        self.worker.finished.connect(self.on_payload_generated)
        self.worker.start()
        
    def on_payload_generated(self, result):
        """Callback de payload généré"""
        self.output_text.setPlainText(result)
        
    def copy_payload(self):
        """Copie le payload dans le presse-papiers"""
        from PyQt5.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_text.toPlainText())
        self.output_text.setPlainText(self.output_text.toPlainText() + "\n\n[✓] Copié dans le presse-papiers!")
        
    def encode_payload(self):
        """Encode le payload"""
        current_text = self.output_text.toPlainText()
        if current_text and "généré:" in current_text:
            encoded = base64.b64encode(current_text.encode()).decode()
            self.output_text.setPlainText(f"Encodé (Base64):\n{encoded}")

