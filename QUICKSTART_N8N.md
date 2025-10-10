# 🚀 Démarrage Rapide n8n

Guide ultra-rapide pour lancer n8n en 10 minutes.

## Option 1 : Docker (Recommandé)

### Prérequis
- Docker installé sur votre machine

### Étapes

**1. Cloner le repo**
```bash
git clone https://github.com/TincoPierre/systeme-automatisation-contenu-ia.git
cd systeme-automatisation-contenu-ia
```

**2. Configurer l'environnement**
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer et changer le mot de passe
nano .env
# ou
code .env
```

**3. Démarrer n8n**
```bash
docker-compose up -d
```

**4. Accéder à n8n**
- Ouvrir http://localhost:5678
- User: `admin`
- Password: celui défini dans `.env`

**5. Importer le workflow**
- Dans n8n : Workflows → Import from File
- Sélectionner `workflow_publication_auto.json`

**6. Configurer les credentials**
- Settings → Credentials
- Ajouter :
  - OpenAI API
  - Google Sheets
  - LinkedIn
  - (Optionnel) Twitter

**7. Tester**
- Ouvrir le workflow
- Cliquer sur "Execute Workflow"
- Vérifier que tout fonctionne

**8. Activer**
- Toggle "Active" en haut à droite
- C'est parti ! 🎉

---

## Option 2 : npm (Local)

### Prérequis
- Node.js 18+ installé

### Étapes

**1. Installer n8n**
```bash
npm install -g n8n
```

**2. Démarrer n8n**
```bash
n8n start
```

**3. Accéder à n8n**
- Ouvrir http://localhost:5678
- Créer un compte

**4. Suivre les étapes 5-8 de l'Option 1**

---

## Option 3 : Railway (Cloud)

### Prérequis
- Compte Railway (gratuit)

### Étapes

**1. Créer un compte sur [railway.app](https://railway.app)**

**2. Déployer n8n**
- New Project → Deploy n8n
- Ou utiliser : https://railway.app/template/n8n

**3. Configurer les variables**
```
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=votre-mot-de-passe
GENERIC_TIMEZONE=Europe/Paris
```

**4. Accéder à n8n**
- Railway vous donne une URL (ex: n8n-production-xxxx.up.railway.app)
- Se connecter avec les identifiants définis

**5. Suivre les étapes 5-8 de l'Option 1**

---

## Checklist Post-Installation

- [ ] n8n accessible et connecté
- [ ] Workflow importé
- [ ] Credential OpenAI configurée
- [ ] Credential Google Sheets configurée
- [ ] Credential LinkedIn configurée
- [ ] Google Sheet "Calendrier_Editorial" accessible
- [ ] Test manuel réussi
- [ ] Workflow activé

---

## Commandes Utiles

### Docker

```bash
# Voir les logs
docker-compose logs -f n8n

# Arrêter n8n
docker-compose down

# Redémarrer n8n
docker-compose restart

# Mettre à jour n8n
docker-compose pull
docker-compose up -d
```

### npm

```bash
# Mettre à jour n8n
npm update -g n8n

# Voir la version
n8n --version
```

---

## Dépannage Rapide

### n8n ne démarre pas (Docker)

```bash
# Vérifier les logs
docker-compose logs n8n

# Vérifier que le port 5678 est libre
lsof -i :5678

# Redémarrer
docker-compose restart
```

### Impossible de se connecter

- Vérifier user/password dans `.env` ou docker-compose.yml
- Essayer en navigation privée (cache)
- Vérifier que n8n est bien démarré : `docker ps`

### Workflow ne s'exécute pas

- Vérifier qu'il est "Active"
- Vérifier le cron expression
- Consulter Executions pour voir les erreurs

---

## Prochaines Étapes

1. ✅ n8n installé et fonctionnel
2. ⏳ Lire le `guide_n8n.md` complet
3. ⏳ Configurer toutes les credentials
4. ⏳ Préparer 3 posts de test dans Google Sheet
5. ⏳ Tester le workflow manuellement
6. ⏳ Activer le workflow
7. ⏳ Monitorer les premières exécutions

---

## Support

- **Documentation complète :** `guide_n8n.md`
- **Workflow JSON :** `workflow_publication_auto.json`
- **Docker Compose :** `docker-compose.yml`

Bon automatisation ! 🎉
