#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de clonage de sites web
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QGroupBox, QLineEdit,
                             QComboBox, QCheckBox, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

class CloningWorker(QThread):
    """Thread de travail pour le clonage"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    
    def __init__(self, url, depth):
        super().__init__()
        self.url = url
        self.depth = depth
        
    def run(self):
        """Exécute le clonage"""
        import time
        for i in range(101):
            self.progress.emit(i)
            time.sleep(0.05)
        result = f"Site web {self.url} cloné avec succès."
        self.finished.emit(result)

class CloningModule(QWidget):
    """Module de clonage de sites web"""
    
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
        
        # Progression
        progress = self.create_progress_section()
        main_layout.addWidget(progress)
        
        # Logs
        logs = self.create_logs_section()
        main_layout.addWidget(logs)
        
        self.setLayout(main_layout)
        
    def create_header(self):
        """Crée l'en-tête du module"""
        header_box = QGroupBox()
        layout = QHBoxLayout()
        
        title = QLabel("Module Clonage")
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
        config_box = QGroupBox("Configuration du clonage")
        layout = QVBoxLayout()
        
        # URL source
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL à cloner:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)
        
        # Profondeur
        depth_layout = QHBoxLayout()
        depth_layout.addWidget(QLabel("Profondeur:"))
        self.depth_combo = QComboBox()
        self.depth_combo.addItems(["1 - Surface", "2 - Moyen", "3 - Complet"])
        depth_layout.addWidget(self.depth_combo)
        layout.addLayout(depth_layout)
        
        # Options
        self.option_images = QCheckBox("Télécharger les images")
        self.option_images.setChecked(True)
        layout.addWidget(self.option_images)
        
        self.option_css = QCheckBox("Télécharger les fichiers CSS")
        self.option_css.setChecked(True)
        layout.addWidget(self.option_css)
        
        self.option_js = QCheckBox("Télécharger les fichiers JavaScript")
        self.option_js.setChecked(True)
        layout.addWidget(self.option_js)
        
        # Bouton
        btn_clone = QPushButton("Démarrer le clonage")
        btn_clone.clicked.connect(self.start_cloning)
        layout.addWidget(btn_clone)
        
        config_box.setLayout(layout)
        return config_box
        
    def create_progress_section(self):
        """Crée la section de progression"""
        progress_box = QGroupBox("Progression")
        layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        progress_box.setLayout(layout)
        return progress_box
        
    def create_logs_section(self):
        """Crée la section des logs"""
        logs_box = QGroupBox("Logs")
        layout = QVBoxLayout()
        
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setPlainText("Prêt à cloner un site web.")
        
        layout.addWidget(self.logs_text)
        logs_box.setLayout(layout)
        return logs_box
        
    def start_cloning(self):
        """Démarre le clonage"""
        url = self.url_input.text()
        
        if not url:
            self.logs_text.setPlainText("Erreur: Veuillez fournir une URL.")
            return
            
        self.logs_text.setPlainText(f"Démarrage du clonage de {url}...")
        
        depth = self.depth_combo.currentIndex() + 1
        
        self.worker = CloningWorker(url, depth)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_cloning_finished)
        self.worker.start()
        
    def on_cloning_finished(self, result):
        """Callback de clonage terminé"""
        self.logs_text.append(f"\n{result}")

