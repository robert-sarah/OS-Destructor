# Security Testing Framework

Un framework professionnel de test de sécurité basé sur PyQt5, offrant une interface graphique moderne et intuitive pour les tests de sécurité autorisés.

## ⚠️ Avertissement Important

Cet outil est conçu **uniquement** pour :
- Les tests de sécurité autorisés
- Les évaluations de vulnérabilités avec permission écrite
- Les environnements de laboratoire contrôlés
- La formation en cybersécurité

**L'utilisation non autorisée de ce logiciel est illégale et peut entraîner de graves conséquences pénales.**

## 🚀 Features

### Module Phishing
- **Templates HTML réels** de haute qualité pour:
  - Gmail
  - Facebook
  - LinkedIn
  - Microsoft
  - PayPal
  - Amazon
- Serveur Flask intégré avec capture de données
- Redirection personnalisable (par défaut vers Google.com)
- Système de logs automatique des informations capturées
- Ouverture automatique du navigateur
- Interface intuitive avec démarrage/arrêt du serveur

### Module Clonage
- Clonage complet de sites web
- Téléchargement des ressources (images, CSS, JS)
- Configuration de la profondeur de clonage
- Suivi de progression

### Module OSINT Intelligence
- Target email enumeration
- Domain information gathering (WHOIS)
- DNS record analysis
- Email breach checking
- Social media discovery
- Export results functionality

### Module DeAPoL (Deep Packet Layer Attack)
- Network packet injection
- Device scanning (ARP scan)
- Deep packet injection attacks
- Open phishing pages on target devices
- Interface selection
- Stealth and persistent mode

### Module Email Campaign
- Send phishing emails with templates
- Generate fake email addresses
- SMTP server configuration
- HTML email support
- Activity logging
- Mailer integration

### SEToolkit Advanced Module
- Credential Harvester
- Java Applet Attack
- USB HID Attack
- Web Jacking Attack
- Mass Mailer Attack
- Multiple attack vectors

### Module Reconnaissance
- Scan de ports
- Détection de technologies
- Découverte de sous-domaines
- Analyse de vulnérabilités

### Module Payloads
- Génération de payloads personnalisés
- Support multi-OS (Linux, Windows, macOS)
- Encodage Base64
- Gestion du presse-papiers

### Module Attaques Web
- Tests SQL Injection
- Détection XSS
- Analyse CSRF
- Tests Clickjacking
- Exploitation de uploads de fichiers

## 📋 Prérequis

- Python 3.7 ou supérieur
- Windows 10/11, Linux ou macOS
- PyQt5

## 🔧 Installation

1. Clonez ce repository :
```bash
git clone https://github.com/robert-sarah/OS-Destructor.git
cd AI
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```



## 🎮 Utilisation

Lancez l'application :
```bash
python main.py
```

Ou sous Windows, double-cliquez sur `run.bat`

### Comment utiliser le Module Phishing

1. Sélectionnez le template souhaité (Gmail, Facebook, etc.)
2. Configurez l'URL de redirection (par défaut: google.com)
3. Cochez "Ouvrir automatiquement le navigateur" si désiré
4. Cliquez sur "Démarrer le serveur"
5. Le serveur démarrera sur http://127.0.0.1:8080
6. Les données saisies seront capturées automatiquement
7. Les utilisateurs seront redirigés vers Google.com après soumission
8. Consultez les logs capturés avec le bouton "Voir les logs"

**Les données capturées sont enregistrées dans :** `logs/captured_data.txt`

## 📁 Structure du Projet

```
.
├── main.py                      # Point d'entrée de l'application
├── modules/
│   ├── __init__.py
│   ├── main_window.py           # Fenêtre principale
│   ├── phishing_module.py       # Module phishing avec serveur Flask
│   ├── cloning_module.py        # Module clonage
│   ├── recon_module.py          # Module reconnaissance
│   ├── payload_module.py        # Module payloads
│   └── webattack_module.py      # Module attaques web
├── templates/                   # Templates HTML de phishing
│   ├── __init__.py
│   ├── gmail.html
│   ├── facebook.html
│   ├── linkedin.html
│   ├── microsoft.html
│   ├── paypal.html
│   └── amazon.html
├── logs/                        # Logs des données capturées (généré)
│   └── captured_data.txt
├── requirements.txt             # Dépendances Python
├── run.bat                      # Script de lancement Windows
└── README.md                    # Documentation
```

## 🎨 Interface

L'interface offre :
- Navigation intuitive entre modules
- Console intégrée pour les logs
- Visualisation des résultats en temps réel
- Configuration avancée pour chaque module

## 🔐 Sécurité

- Utilisez uniquement sur des systèmes de test
- Ne stockez pas de données sensibles
- Respectez toujours les lois locales sur la cybersécurité
- Obtenez une autorisation écrite avant tout test

## 🛠️ Développement

Pour contribuer au projet :
1. Forkez le repository
2. Créez une branche pour votre fonctionnalité
3. Commitez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 🆕 Améliorations par rapport à SE Toolkit

- ✅ Interface graphique moderne et intuitive (PyQt5)
- ✅ Templates HTML professionnels et réalistes
- ✅ Redirection automatique personnalisable
- ✅ Capture et logging automatique des données
- ✅ Architecture modulaire et extensible
- ✅ Plus de modules intégrés (6 modules au total)
- ✅ Pas besoin de ligne de commande
- ✅ Threading pour performances optimales

## 📝 License

Ce projet est fourni à des fins éducatives uniquement.

## 👥 Auteur

Développé pour la communauté de cybersécurité.

## 📞 Support

Pour toute question ou problème, veuillez ouvrir une issue sur GitHub.

---

**Rappel : Cet outil doit être utilisé de manière responsable et légale uniquement.**

