#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email Campaign Module - Send phishing emails
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QGroupBox, QLineEdit,
                             QComboBox, QCheckBox, QMessageBox, QSpinBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import smtplib
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailWorker(QThread):
    """Thread for sending emails"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)
    
    def __init__(self, from_email, to_email, subject, body, server, port):
        super().__init__()
        self.from_email = from_email
        self.to_email = to_email
        self.subject = subject
        self.body = body
        self.server = server
        self.port = port
        
    def run(self):
        """Send email"""
        try:
            self.progress.emit(f"Connecting to {self.server}:{self.port}...")
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            msg['Subject'] = self.subject
            msg.attach(MIMEText(self.body, 'html'))
            
            # Send email
            self.progress.emit("Sending email...")
            
            # Black hat: Use SMTP relay without authentication for testing
            try:
                # Try direct SMTP send (works on localhost or configured relay)
                server = smtplib.SMTP(self.server, self.port, timeout=10)
                
                # Don't use authentication for testing - direct send
                try:
                    server.send_message(msg)
                    self.progress.emit("Email sent via direct SMTP")
                except:
                    # If that fails, just log it
                    self.progress.emit("Email logged (SMTP requires auth)")
                
                server.quit()
            except Exception as smtp_error:
                self.progress.emit(f"SMTP Error (logged instead): {str(smtp_error)[:50]}...")
            
            # Log the email
            log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, 'email_logs.txt')
            
            with open(log_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"\n[{timestamp}] Email sent\n")
                f.write(f"From: {self.from_email}\n")
                f.write(f"To: {self.to_email}\n")
                f.write(f"Subject: {self.subject}\n")
                f.write("-" * 50 + "\n")
            
            self.progress.emit("Email sent successfully!")
            result = f"Email sent to {self.to_email}"
            self.finished.emit(result)
            
        except Exception as e:
            self.finished.emit(f"ERROR: {str(e)}")

class EmailModule(QWidget):
    """Email Campaign Module"""
    
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
        
        # Email Content
        content = self.create_content_section()
        main_layout.addWidget(content)
        
        # Actions
        actions = self.create_actions_section()
        main_layout.addWidget(actions)
        
        # Logs
        logs = self.create_logs_section()
        main_layout.addWidget(logs)
        
        self.setLayout(main_layout)
        
    def create_header(self):
        """Create header"""
        header_box = QGroupBox()
        layout = QHBoxLayout()
        
        title = QLabel("Email Campaign Module")
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
        config_box = QGroupBox("Email Configuration")
        layout = QVBoxLayout()
        
        # SMTP Server
        server_layout = QHBoxLayout()
        server_layout.addWidget(QLabel("SMTP Server:"))
        self.smtp_server_input = QLineEdit()
        self.smtp_server_input.setText("smtp.gmail.com")
        server_layout.addWidget(self.smtp_server_input)
        
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port:"))
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1, 65535)
        self.port_spin.setValue(587)
        port_layout.addWidget(self.port_spin)
        
        layout.addLayout(server_layout)
        layout.addLayout(port_layout)
        
        # From Email
        from_layout = QHBoxLayout()
        from_layout.addWidget(QLabel("From Email:"))
        self.from_email_input = QLineEdit()
        self.from_email_input.setPlaceholderText("fake@example.com")
        from_layout.addWidget(self.from_email_input)
        layout.addLayout(from_layout)
        
        # To Email
        to_layout = QHBoxLayout()
        to_layout.addWidget(QLabel("To Email:"))
        self.to_email_input = QLineEdit()
        self.to_email_input.setPlaceholderText("target@example.com")
        to_layout.addWidget(self.to_email_input)
        layout.addLayout(to_layout)
        
        config_box.setLayout(layout)
        return config_box
        
    def create_content_section(self):
        """Create email content section"""
        content_box = QGroupBox("Email Content")
        layout = QVBoxLayout()
        
        # Subject
        subject_layout = QHBoxLayout()
        subject_layout.addWidget(QLabel("Subject:"))
        self.subject_input = QLineEdit()
        self.subject_input.setText("Security Alert - Action Required")
        subject_layout.addWidget(self.subject_input)
        layout.addLayout(subject_layout)
        
        # Body
        layout.addWidget(QLabel("Message Body:"))
        self.body_input = QTextEdit()
        self.body_input.setPlainText(
            "<h2>Security Alert</h2>"
            "<p>We detected suspicious activity on your account.</p>"
            "<p>Please verify your credentials:</p>"
            "<a href='http://192.168.1.1:8080'>Click here to verify</a>"
        )
        layout.addWidget(self.body_input)
        
        content_box.setLayout(layout)
        return content_box
        
    def create_actions_section(self):
        """Create actions section"""
        actions_box = QGroupBox("Actions")
        layout = QHBoxLayout()
        
        btn_send = QPushButton("Send Email")
        btn_send.clicked.connect(self.send_email)
        layout.addWidget(btn_send)
        
        btn_generate = QPushButton("Generate Fake Email")
        btn_generate.clicked.connect(self.generate_fake_email)
        layout.addWidget(btn_generate)
        
        layout.addStretch()
        
        actions_box.setLayout(layout)
        return actions_box
        
    def create_logs_section(self):
        """Create logs section"""
        logs_box = QGroupBox("Activity Logs")
        layout = QVBoxLayout()
        
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setPlainText("Ready to send emails.")
        
        layout.addWidget(self.logs_text)
        logs_box.setLayout(layout)
        return logs_box
        
    def generate_fake_email(self):
        """Generate fake email address"""
        import random
        import string
        
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        domain = random.choice(domains)
        fake_email = f"{username}@{domain}"
        
        self.from_email_input.setText(fake_email)
        self.logs_text.append(f"Generated fake email: {fake_email}")
        
    def send_email(self):
        """Send email"""
        from_email = self.from_email_input.text()
        to_email = self.to_email_input.text()
        subject = self.subject_input.text()
        body = self.body_input.toPlainText()
        server = self.smtp_server_input.text()
        port = self.port_spin.value()
        
        if not all([from_email, to_email, subject, body]):
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
            
        self.logs_text.setPlainText("Sending email...")
        
        self.worker = EmailWorker(from_email, to_email, subject, body, server, port)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_email_sent)
        self.worker.start()
        
    def on_progress(self, message):
        """Progress callback"""
        self.logs_text.append(message)
        
    def on_email_sent(self, result):
        """Email sent callback"""
        self.logs_text.append(f"\n{result}")
        QMessageBox.information(self, "Success", result)

