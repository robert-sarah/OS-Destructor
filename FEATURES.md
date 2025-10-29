# Fonctionnalités Avancées

## 🎯 Module Phishing Avancé

### Fonctionnalités Implémentées

#### ✅ Templates Professionnels
- **6 templates HTML réalistes** :
  - Gmail avec design Google authentique
  - Facebook avec interface moderne
  - LinkedIn professionnel
  - Microsoft Account
  - PayPal sécurisé
  - Amazon commerce

#### ✅ Serveur Flask Intégré
- Serveur web local sur `http://127.0.0.1:8080`
- Gestion d'état avec threads séparés
- Démarrage/arrêt dynamique
- Aucun redémarrage nécessaire

#### ✅ Capture de Données
- Capture automatique des identifiants
- Logging horodaté dans `logs/captured_data.txt`
- Format structuré avec timestamps
- Pas de limite de captures

#### ✅ Redirection Intelligente
- URL de redirection personnalisable
- Par défaut : Google.com (looks legit)
- Support de n'importe quelle URL
- Configuration à la volée

#### ✅ Interface Utilisateur
- Bouton démarrage/arrêt du serveur
- Visualisation des logs capturés
- Ouverture automatique du navigateur
- Feedback visuel en temps réel

## 🔧 Architecture Technique

### Threading
- `PhishingServer(QThread)` : Serveur Flask dans un thread séparé
- Non-bloquant pour l'interface PyQt5
- Gestion propre de l'arrêt du serveur

### Structure des Templates
```
templates/
├── gmail.html      # Google Gmail
├── facebook.html   # Facebook
├── linkedin.html   # LinkedIn
├── microsoft.html  # Microsoft Account
├── paypal.html     # PayPal
└── amazon.html     # Amazon
```

Chaque template :
- Design responsive
- CSS inline (pas de dépendances)
- Formulaires fonctionnels
- Redirection post-soumission

### Flux de Données

1. **Utilisateur sélectionne un template**
2. **Serveur démarre sur port 8080**
3. **Template HTML servi**
4. **Utilisateur saisit ses identifiants**
5. **POST vers /capture**
6. **Données enregistrées dans logs/**
7. **Redirection vers URL configurée**

## 📊 Format des Logs

```text
[2024-01-15 14:30:25] Template: Gmail
Email: user@example.com
Password: secret123
--------------------------------------------------
[2024-01-15 14:32:10] Template: Facebook
Email: test@facebook.com
Password: pass456
--------------------------------------------------
```

## 🚀 Utilisation Rapide

### Démarrage Rapide
1. Lancez l'application
2. Allez dans "Module Phishing"
3. Choisissez un template
4. Cliquez "Démarrer le serveur"
5. Testez sur http://127.0.0.1:8080

### Configuration Avancée

**URL de redirection personnalisée** :
- Google.com (par défaut)
- Page de connexion légitime
- Page d'erreur "essayez de vous reconnecter"

**Sans navigation automatique** :
- Décochez "Ouvrir auto"
- Démarrer le serveur manuellement
- Partager le lien

### Consulter les Logs

Cliquez sur "Voir les logs" pour :
- Afficher toutes les captures
- Identifier les soumissions
- Extraire les données

## 🔒 Sécurité et Éthique

### Bonnes Pratiques
- ✅ Utiliser uniquement sur systèmes autorisés
- ✅ Obtenir permission écrite
- ✅ Tester en environnement isolé
- ✅ Supprimer les logs après tests
- ✅ Respecter les lois locales

### Ce à quoi Faire Attention
- ⚠️ Ne jamais utiliser sur systèmes de production sans autorisation
- ⚠️ Ne pas partager les données capturées
- ⚠️ Respecter la vie privée
- ⚠️ Se limiter au périmètre de test autorisé

## 🛠️ Dépannage

### Le serveur ne démarre pas
```bash
pip install flask
```

### Port 8080 déjà utilisé
Modifier le port dans `phishing_module.py` ligne 80 :
```python
app.run(host='127.0.0.1', port=8081, ...)
```

### Templates non trouvés
Vérifier que le dossier `templates/` existe et contient les fichiers HTML

### Logs non créés
Le dossier `logs/` est créé automatiquement au démarrage

## 🎨 Personnalisation

### Ajouter un Nouveau Template

1. Créer `templates/votretemplate.html`
2. Inclure un formulaire vers `/capture`
3. Ajouter dans `phishing_module.py` :
```python
template_map = {
    ...
    'VotreTemplate': 'votretemplate.html'
}
```

### Modifier l'Apparence

Éditez directement les fichiers HTML dans `templates/` :
- CSS inline modifiable
- Aucune recompilation nécessaire
- Relancez le serveur après modification

## 📈 Améliorations Futures

- [ ] Support SSL/HTTPS
- [ ] Email automatique des captures
- [ ] Dashboard des statistiques
- [ ] Multiple redirections aléatoires
- [ ] Cloaking par IP
- [ ] Templates de type "typosquatting"
- [ ] Génération de noms de domaine similaires
- [ ] Support de macros Word/Excel
- [ ] Attaques spear phishing ciblées

---

**Rappel** : Cet outil est uniquement à des fins éducatives et de tests autorisés.

