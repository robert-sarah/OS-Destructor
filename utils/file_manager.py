#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de fichiers et dossiers
"""

import os

def create_directories():
    """Crée les dossiers nécessaires s'ils n'existent pas"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    directories = [
        'logs',
        'cloned_sites',
        'phishing_templates',
        'payloads',
        'results'
    ]
    
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        # Créer un fichier .gitkeep pour Git
        gitkeep = os.path.join(dir_path, '.gitkeep')
        if not os.path.exists(gitkeep):
            with open(gitkeep, 'w') as f:
                f.write('')

if __name__ == '__main__':
    create_directories()

