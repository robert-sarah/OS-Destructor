#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Security Testing Framework - Application principale
Un outil professionnel de test de sécurité basé sur PyQt5
"""

import sys
import os

# Créer les dossiers nécessaires
from utils.file_manager import create_directories
create_directories()

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QTabWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont

# Import des modules de l'application
from modules.main_window import MainWindow
from modules.phishing_module import PhishingModule
from modules.cloning_module import CloningModule
from modules.recon_module import ReconModule
from modules.payload_module import PayloadModule
from modules.webattack_module import WebAttackModule
from modules.deapol_module import DeAPoLModule
from modules.email_module import EmailModule
from modules.osint_module import OSINTModule
from modules.setoolkit_module import SEToolkitModule
from modules.ml_blackhat_module import MLBlackHatModule

class SecurityFramework(QMainWindow):
    """Application principale du framework de sécurité"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Security Testing Framework - v1.0")
        self.setGeometry(100, 100, 1400, 900)
        
        # Création du widget empilé pour les différentes vues
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Création des modules
        self.main_window = MainWindow(self)
        self.phishing_module = PhishingModule(self)
        self.cloning_module = CloningModule(self)
        self.recon_module = ReconModule(self)
        self.payload_module = PayloadModule(self)
        self.webattack_module = WebAttackModule(self)
        self.deapol_module = DeAPoLModule(self)
        self.email_module = EmailModule(self)
        self.osint_module = OSINTModule(self)
        self.setoolkit_module = SEToolkitModule(self)
        self.ml_blackhat_module = MLBlackHatModule(self)
        
        # Ajout des widgets au stack
        self.stacked_widget.addWidget(self.main_window)
        self.stacked_widget.addWidget(self.phishing_module)
        self.stacked_widget.addWidget(self.cloning_module)
        self.stacked_widget.addWidget(self.recon_module)
        self.stacked_widget.addWidget(self.payload_module)
        self.stacked_widget.addWidget(self.webattack_module)
        self.stacked_widget.addWidget(self.deapol_module)
        self.stacked_widget.addWidget(self.email_module)
        self.stacked_widget.addWidget(self.osint_module)
        self.stacked_widget.addWidget(self.setoolkit_module)
        self.stacked_widget.addWidget(self.ml_blackhat_module)
        
        # Connexion des signaux de navigation
        self.main_window.navigate.connect(self.switch_module)
        
        # Affichage de la fenêtre principale
        self.stacked_widget.setCurrentWidget(self.main_window)
        
    def switch_module(self, module_name):
        """Change de module selon la navigation"""
        module_map = {
            'main': 0,
            'phishing': 1,
            'cloning': 2,
            'recon': 3,
            'payload': 4,
            'webattack': 5,
            'deapol': 6,
            'email': 7,
            'osint': 8,
            'setoolkit': 9,
            'ml_blackhat': 10
        }
        
        if module_name in module_map:
            index = module_map[module_name]
            self.stacked_widget.setCurrentIndex(index)
            
def main():
    """Point d'entrée de l'application"""
    app = QApplication(sys.argv)
    
    # Configuration de l'application
    app.setStyle('Fusion')
    
    # Création et affichage de la fenêtre principale
    window = SecurityFramework()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

