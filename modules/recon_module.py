#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de reconnaissance
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QGroupBox, QLineEdit,
                             QComboBox, QTreeWidget, QTreeWidgetItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

class ReconWorker(QThread):
    """Thread de travail pour la reconnaissance"""
    finished = pyqtSignal(str, dict)
    
    def __init__(self, target, mode):
        super().__init__()
        self.target = target
        self.mode = mode
        
    def run(self):
        """Exécute la reconnaissance"""
        import time
        time.sleep(2)
        
        results = {
            "IP": self.target,
            "Ports": "80, 443, 22",
            "Technologies": "Apache 2.4, PHP 7.4",
            "Subdomains": "www, mail, ftp"
        }
        
        self.finished.emit(self.target, results)

class ReconModule(QWidget):
    """Module de reconnaissance"""
    
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
        
        self.setLayout(main_layout)
        
    def create_header(self):
        """Crée l'en-tête du module"""
        header_box = QGroupBox()
        layout = QHBoxLayout()
        
        title = QLabel("Module Reconnaissance")
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
        config_box = QGroupBox("Configuration de la reconnaissance")
        layout = QVBoxLayout()
        
        # Cible
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Cible:"))
        self.target_input = QLineEdit()
    self.target_input.setPlaceholderText("Entrez le domaine ou l'adresse IP cible")
        target_layout.addWidget(self.target_input)
        layout.addLayout(target_layout)
        
        # Mode
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Mode:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Scan de base",
            "Scan complet",
            "Scan furtif",
            "Scan agressif"
        ])
        mode_layout.addWidget(self.mode_combo)
        layout.addLayout(mode_layout)
        
        # Bouton
        btn_scan = QPushButton("Lancer le scan")
        btn_scan.clicked.connect(self.start_scan)
        layout.addWidget(btn_scan)
        
        config_box.setLayout(layout)
        return config_box
        
    def create_results_section(self):
        """Crée la section des résultats"""
        results_box = QGroupBox("Résultats")
        layout = QVBoxLayout()
        
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(["Information", "Valeur"])
        layout.addWidget(self.results_tree)
        
        results_box.setLayout(layout)
        return results_box
        
    def start_scan(self):
        """Démarre le scan de reconnaissance"""
        target = self.target_input.text()
        
        if not target:
            self.clear_results()
            return
            
        mode = self.mode_combo.currentText()
        
        self.clear_results()
        self.results_tree.addTopLevelItem(
            QTreeWidgetItem(["Statut", f"Scan en cours... {target}"]))
        
        self.worker = ReconWorker(target, mode)
        self.worker.finished.connect(self.on_scan_finished)
        self.worker.start()
        
    def clear_results(self):
        """Efface les résultats"""
        self.results_tree.clear()
        
    def on_scan_finished(self, target, results):
        """Callback de scan terminé"""
        self.results_tree.clear()
        
        root = QTreeWidgetItem([f"Cible: {target}", ""])
        self.results_tree.addTopLevelItem(root)
        
        for key, value in results.items():
            item = QTreeWidgetItem([key, value])
            root.addChild(item)
            
        self.results_tree.expandAll()

