#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module d'attaques web
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QGroupBox, QLineEdit,
                             QComboBox, QCheckBox, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

class AttackWorker(QThread):
    """Thread de travail pour les attaques"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)
    
    def __init__(self, target, attack_type):
        super().__init__()
        self.target = target
        self.attack_type = attack_type
        
    def run(self):
        """Exécute l'attaque"""
        import time
        
        self.progress.emit("Initialisation...")
        time.sleep(0.5)
        
        self.progress.emit(f"Exécution de {self.attack_type}...")
        time.sleep(1)
        
        self.progress.emit("Analyse des résultats...")
        time.sleep(0.5)
        
        result = f"Attaque {self.attack_type} terminée sur {self.target}"
        self.finished.emit(result)

class WebAttackModule(QWidget):
    """Module d'attaques web"""
    
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
        
        # Résultats
        results = self.create_results_section()
        main_layout.addWidget(results)
        
        # Logs
        logs = self.create_logs_section()
        main_layout.addWidget(logs)
        
        self.setLayout(main_layout)
        
    def create_header(self):
        """Crée l'en-tête du module"""
        header_box = QGroupBox()
        layout = QHBoxLayout()
        
        title = QLabel("Module Attaques Web")
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
        config_box = QGroupBox("Configuration de l'attaque")
        layout = QVBoxLayout()
        
        # URL cible
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL cible:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Entrez l'URL cible (ex: https://site.com/page)")
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)
        
        # Type d'attaque
        attack_layout = QHBoxLayout()
        attack_layout.addWidget(QLabel("Type d'attaque:"))
        self.attack_combo = QComboBox()
        self.attack_combo.addItems([
            "SQL Injection (Basic)",
            "XSS (Cross-Site Scripting)",
            "CSRF (Cross-Site Request Forgery)",
            "Clickjacking",
            "File Upload Exploit"
        ])
        attack_layout.addWidget(self.attack_combo)
        layout.addLayout(attack_layout)
        
        # Options
        self.option_verbose = QCheckBox("Mode verbeux")
        layout.addWidget(self.option_verbose)
        
        self.option_save = QCheckBox("Sauvegarder les résultats")
        layout.addWidget(self.option_save)
        
        # Bouton
        btn_attack = QPushButton("Lancer l'attaque")
        btn_attack.clicked.connect(self.start_attack)
        layout.addWidget(btn_attack)
        
        config_box.setLayout(layout)
        return config_box
        
    def create_results_section(self):
        """Crée la section des résultats"""
        results_box = QGroupBox("Résultats")
        layout = QVBoxLayout()
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Paramètre", "Valeur", "Vulnérable"])
        layout.addWidget(self.results_table)
        
        results_box.setLayout(layout)
        return results_box
        
    def create_logs_section(self):
        """Crée la section des logs"""
        logs_box = QGroupBox("Logs d'exécution")
        layout = QVBoxLayout()
        
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setMaximumHeight(150)
        self.logs_text.setPlainText("Prêt à exécuter une attaque.")
        
        layout.addWidget(self.logs_text)
        logs_box.setLayout(layout)
        return logs_box
        
    def start_attack(self):
        """Démarre l'attaque"""
        url = self.url_input.text()
        
        if not url:
            self.logs_text.setPlainText("Erreur: Veuillez fournir une URL.")
            return
            
        attack_type = self.attack_combo.currentText()
        
        self.logs_text.setPlainText(f"Démarrage de {attack_type} sur {url}")
        self.results_table.setRowCount(0)
        
        self.worker = AttackWorker(url, attack_type)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_attack_finished)
        self.worker.start()
        
    def on_progress(self, message):
        """Callback de progression"""
        self.logs_text.append(message)
        
    def on_attack_finished(self, result):
        """Callback d'attaque terminée"""
        self.logs_text.append(f"\n{result}")
        
        # Ajout de résultats factices
        self.results_table.setRowCount(3)
        
        test_cases = [
            ("param1", "test", "Non"),
            ("param2", "value", "Oui"),
            ("param3", "data", "Non")
        ]
        
        for i, (param, value, vuln) in enumerate(test_cases):
            self.results_table.setItem(i, 0, QTableWidgetItem(param))
            self.results_table.setItem(i, 1, QTableWidgetItem(value))
            self.results_table.setItem(i, 2, QTableWidgetItem(vuln))

