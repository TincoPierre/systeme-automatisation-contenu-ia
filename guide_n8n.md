# Guide Complet n8n - Automatisation de Publication

## 🎯 Vue d'ensemble

Ce guide vous accompagne dans la mise en place de **n8n** pour automatiser complètement la génération et la publication de vos posts LinkedIn et X (Twitter).

## 📋 Table des matières

1. [Installation de n8n](#installation)
2. [Configuration initiale](#configuration)
3. [Import du workflow](#import-workflow)
4. [Configuration des credentials](#credentials)
5. [Test et activation](#test)
6. [Déploiement en production](#deploiement)
7. [Maintenance et monitoring](#maintenance)

---

## 1. Installation de n8n {#installation}

### Option A : Installation Locale (Développement)

**Prérequis :**
- Node.js 18+ installé
- npm ou pnpm

**Installation :**
```bash
# Via npm
npm install -g n8n

# Via pnpm (plus rapide)
pnpm install -g n8n

# Démarrer n8n
n8n start
```

**Accès :**
- Ouvrir http://localhost:5678
- Créer un compte (local uniquement)

---

### Option B : Docker (Recommandé pour production)

**Créer un fichier `docker-compose.yml` :**

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=votre-mot-de-passe-securise
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - WEBHOOK_URL=http://localhost:5678/
      - GENERIC_TIMEZONE=Europe/Paris
    volumes:
      - n8n_data:/home/node/.n8n
      - ./workflows:/home/node/.n8n/workflows

volumes:
  n8n_data:
```

**Démarrer :**
```bash
docker-compose up -d
```

**Accès :**
- http://localhost:5678
- User: admin
- Password: celui défini dans docker-compose.yml

---

### Option C : Railway (Déploiement Cloud Facile)

**Étapes :**

1. Créer un compte sur [railway.app](https://railway.app)
2. Cliquer sur "New Project" → "Deploy n8n"
3. Ou utiliser le template : https://railway.app/template/n8n

**Variables d'environnement à configurer :**
```
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=votre-mot-de-passe
GENERIC_TIMEZONE=Europe/Paris
```

**Coût :** ~5$/mois

---

### Option D : VPS (Hetzner, OVH, etc.)

**Sur un VPS Ubuntu :**

```bash
# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Installer Docker Compose
sudo apt install docker-compose -y

# Créer le dossier
mkdir ~/n8n && cd ~/n8n

# Créer docker-compose.yml (voir Option B)
nano docker-compose.yml

# Démarrer
docker-compose up -d

# Configurer Nginx (optionnel pour HTTPS)
# Voir section Déploiement
```

**Coût :** 3-5€/mois

---

## 2. Configuration Initiale {#configuration}

### Premier lancement

1. **Accéder à n8n** (http://localhost:5678)
2. **Créer un compte** (email + mot de passe)
3. **Explorer l'interface**
   - Workflows (vos automatisations)
   - Credentials (vos connexions API)
   - Executions (historique des exécutions)

### Configuration de base

**Settings → General :**
- **Timezone :** Europe/Paris
- **Date Format :** DD/MM/YYYY
- **Time Format :** 24h

---

## 3. Import du Workflow {#import-workflow}

### Méthode 1 : Import depuis fichier JSON

1. Télécharger `workflow_publication_auto.json` (fourni dans le repo)
2. Dans n8n, cliquer sur **"Workflows"** → **"Import from File"**
3. Sélectionner le fichier JSON
4. Le workflow apparaît dans votre liste

### Méthode 2 : Création manuelle

Si vous préférez créer le workflow vous-même, suivez la section "Architecture du Workflow" ci-dessous.

---

## 4. Configuration des Credentials {#credentials}

### A. OpenAI API

1. **Dans n8n :** Settings → Credentials → Add Credential
2. **Rechercher :** "OpenAI"
3. **Configurer :**
   - **API Key :** Votre clé OpenAI
   - **Organization ID :** (optionnel)
4. **Tester** et **Sauvegarder**

---

### B. Google Sheets

1. **Dans n8n :** Credentials → Add Credential → Google Sheets
2. **Méthode OAuth2 (Recommandée) :**
   - Cliquer sur "Connect my account"
   - Autoriser n8n à accéder à Google Sheets
   - Sélectionner votre compte Google

3. **Méthode Service Account (Alternative) :**
   - Créer un Service Account dans Google Cloud Console
   - Télécharger le fichier JSON
   - Copier le contenu dans n8n
   - Partager votre Google Sheet avec l'email du Service Account

---

### C. LinkedIn

1. **Créer une App LinkedIn :**
   - Aller sur https://www.linkedin.com/developers/apps
   - Créer une nouvelle app
   - Demander l'accès à "Sign In with LinkedIn" et "Share on LinkedIn"
   - Noter le **Client ID** et **Client Secret**

2. **Dans n8n :**
   - Credentials → Add Credential → LinkedIn OAuth2
   - **Client ID :** Votre Client ID
   - **Client Secret :** Votre Client Secret
   - **OAuth Redirect URL :** Copier l'URL fournie par n8n
   - Retourner dans votre app LinkedIn et ajouter cette URL dans "Authorized redirect URLs"
   - Cliquer sur "Connect my account" dans n8n

---

### D. Twitter / X (Optionnel pour l'instant)

**⚠️ Important :** L'API X nécessite un abonnement (Basic à 100$/mois).

**Alternative gratuite :** Utiliser Buffer ou poster manuellement.

**Si vous avez accès à l'API X :**

1. **Créer une App sur https://developer.twitter.com**
2. **Noter :**
   - API Key
   - API Secret Key
   - Access Token
   - Access Token Secret

3. **Dans n8n :**
   - Credentials → Add Credential → Twitter OAuth1
   - Remplir les informations

---

## 5. Architecture du Workflow {#architecture}

### Vue d'ensemble

```
┌──────────────────────────────────────────────────────────┐
│                  WORKFLOW n8n                             │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  1. [Schedule Trigger]                                   │
│     └─ Tous les jours à 8h30                            │
│                                                           │
│  2. [Google Sheets - Read]                              │
│     └─ Lire le calendrier éditorial                     │
│     └─ Filter: Statut = "Validé"                        │
│     └─ Filter: Date = Aujourd'hui                       │
│                                                           │
│  3. [IF Node]                                           │
│     └─ Des posts à publier ?                            │
│         ├─ OUI → Continuer                              │
│         └─ NON → Stop                                   │
│                                                           │
│  4. [Loop Over Items]                                   │
│     └─ Pour chaque post trouvé                          │
│                                                           │
│  5. [Set Variables]                                     │
│     └─ Extraire les données du post                     │
│                                                           │
│  6. [LinkedIn - Create Post]                            │
│     └─ Publier sur LinkedIn                             │
│                                                           │
│  7. [HTTP Request - Twitter] (Optionnel)                │
│     └─ Publier sur X via API                            │
│                                                           │
│  8. [Google Sheets - Update]                            │
│     └─ Mettre à jour le statut → "Publié"              │
│     └─ Ajouter date de publication                      │
│     └─ Ajouter URLs des posts                           │
│                                                           │
│  9. [Send Email/Slack]                                  │
│     └─ Notification de succès                           │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## 6. Configuration Détaillée des Nodes {#nodes-config}

### Node 1 : Schedule Trigger

**Configuration :**
- **Mode :** Cron
- **Cron Expression :** `30 8 * * *` (tous les jours à 8h30)
- **Timezone :** Europe/Paris

**Alternative (plus simple) :**
- **Mode :** Every Day
- **Hour :** 8
- **Minute :** 30

---

### Node 2 : Google Sheets - Read

**Configuration :**
- **Credential :** Votre credential Google Sheets
- **Operation :** Read
- **Document :** Sélectionner votre Calendrier_Editorial
- **Sheet :** Calendrier
- **Range :** A:O (toutes les colonnes)
- **Options :**
  - ✅ Read Row as Headers
  - ✅ Return All Matches

---

### Node 3 : Filter (Code Node)

**Type :** Code (JavaScript)

**Code :**
```javascript
// Filtrer les posts à publier aujourd'hui
const today = new Date().toISOString().split('T')[0]; // Format YYYY-MM-DD

const items = $input.all();
const filteredItems = [];

for (const item of items) {
  const statut = item.json.Statut;
  const datePublication = item.json['Date Publication'];
  
  // Vérifier si le post doit être publié aujourd'hui
  if (statut === 'Validé' && datePublication === today) {
    filteredItems.push(item);
  }
}

// Si aucun post à publier, retourner un item vide pour le IF
if (filteredItems.length === 0) {
  return [{ json: { hasItems: false } }];
}

// Sinon, retourner les posts filtrés
return filteredItems.map(item => ({
  json: { ...item.json, hasItems: true }
}));
```

---

### Node 4 : IF Node

**Configuration :**
- **Condition :** `{{ $json.hasItems }}` equals `true`
- **True :** Continuer vers Loop
- **False :** Stop (ou notification "Aucun post aujourd'hui")

---

### Node 5 : Set Variables

**Configuration :**
- **Keep Only Set :** false
- **Values to Set :**
  - `id` = `{{ $json.ID }}`
  - `type` = `{{ $json.Type }}`
  - `brouillon_linkedin` = `{{ $json['Brouillon LinkedIn'] }}`
  - `brouillon_twitter` = `{{ $json['Brouillon Twitter'] }}`
  - `row_number` = `{{ $json._row_number }}` (pour l'update)

---

### Node 6 : LinkedIn - Create Post

**Configuration :**
- **Credential :** Votre credential LinkedIn
- **Resource :** Post
- **Operation :** Create
- **Post As :** Person (ou Organization si vous publiez pour une page)
- **Text :** `{{ $json.brouillon_linkedin }}`
- **Visibility :** PUBLIC

**Options :**
- **Share Media :** Non (pour l'instant, texte uniquement)

---

### Node 7 : HTTP Request - Twitter (Optionnel)

**Configuration :**
- **Method :** POST
- **URL :** `https://api.twitter.com/2/tweets`
- **Authentication :** OAuth1
- **Credential :** Votre credential Twitter
- **Body :**
```json
{
  "text": "{{ $json.brouillon_twitter }}"
}
```

**Headers :**
- `Content-Type`: `application/json`

---

### Node 8 : Google Sheets - Update

**Configuration :**
- **Credential :** Votre credential Google Sheets
- **Operation :** Update
- **Document :** Calendrier_Editorial
- **Sheet :** Calendrier
- **Range :** Utiliser le row_number pour cibler la bonne ligne
- **Options :**
  - **Value Input Mode :** USER_ENTERED

**Colonnes à mettre à jour :**
- **Statut :** "Publié"
- **Date Publiée :** `{{ $now.format('yyyy-MM-dd HH:mm') }}`
- **URL LinkedIn :** `{{ $node["LinkedIn - Create Post"].json.url }}`
- **URL Twitter :** `{{ $node["HTTP Request - Twitter"].json.data.id }}`

---

### Node 9 : Send Email

**Configuration :**
- **Credential :** Gmail ou SMTP
- **To :** Votre email
- **Subject :** `✅ Posts publiés - {{ $now.format('dd/MM/yyyy') }}`
- **Text :**
```
Bonjour,

{{ $json.count }} post(s) ont été publiés avec succès aujourd'hui.

Détails :
- Type : {{ $json.type }}
- LinkedIn : {{ $json.url_linkedin }}

Bonne journée !
```

---

## 7. Test et Activation {#test}

### Test Manuel

1. **Préparer un post de test :**
   - Dans votre Google Sheet, créer une ligne avec :
     - Statut : "Validé"
     - Date Publication : Aujourd'hui
     - Brouillons remplis

2. **Dans n8n :**
   - Ouvrir votre workflow
   - Cliquer sur **"Execute Workflow"** (en haut à droite)
   - Observer l'exécution node par node

3. **Vérifier :**
   - Le post est publié sur LinkedIn
   - Le statut est mis à jour dans Google Sheet
   - Vous recevez l'email de confirmation

### Debugging

**Si un node échoue :**
- Cliquer sur le node rouge
- Lire l'erreur dans le panneau de droite
- Vérifier les credentials
- Vérifier les données d'entrée

**Logs :**
- Executions → Voir l'historique complet
- Chaque exécution est sauvegardée avec tous les détails

### Activation

Une fois les tests réussis :
1. Cliquer sur **"Active"** (toggle en haut à droite)
2. Le workflow s'exécutera automatiquement selon le schedule

---

## 8. Déploiement en Production {#deploiement}

### Option 1 : Railway (Le plus simple)

**Étapes :**
1. Créer un compte sur [railway.app](https://railway.app)
2. New Project → Deploy n8n
3. Configurer les variables d'environnement
4. Importer votre workflow (export/import JSON)
5. Configurer les credentials
6. Activer le workflow

**Coût :** ~5$/mois

---

### Option 2 : VPS avec Docker + Nginx + SSL

**1. Préparer le VPS :**
```bash
# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Installer Docker Compose
sudo apt install docker-compose -y

# Installer Nginx
sudo apt install nginx -y

# Installer Certbot (SSL)
sudo apt install certbot python3-certbot-nginx -y
```

**2. Créer `docker-compose.yml` :**
```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    restart: unless-stopped
    ports:
      - "127.0.0.1:5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - N8N_HOST=${N8N_DOMAIN}
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - NODE_ENV=production
      - WEBHOOK_URL=https://${N8N_DOMAIN}/
      - GENERIC_TIMEZONE=Europe/Paris
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
```

**3. Créer `.env` :**
```bash
N8N_PASSWORD=votre-mot-de-passe-securise
N8N_DOMAIN=n8n.votre-domaine.com
```

**4. Configurer Nginx :**
```nginx
# /etc/nginx/sites-available/n8n
server {
    listen 80;
    server_name n8n.votre-domaine.com;

    location / {
        proxy_pass http://localhost:5678;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**5. Activer et SSL :**
```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/n8n /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Obtenir le certificat SSL
sudo certbot --nginx -d n8n.votre-domaine.com

# Démarrer n8n
docker-compose up -d
```

**Coût :** 3-5€/mois (VPS)

---

## 9. Maintenance et Monitoring {#maintenance}

### Vérifications Régulières

**Quotidien (automatique) :**
- Email de confirmation après chaque publication
- Vérifier que le post est bien publié

**Hebdomadaire :**
- Consulter les Executions dans n8n
- Vérifier qu'il n'y a pas d'erreurs
- Valider les posts de la semaine suivante

**Mensuel :**
- Mettre à jour n8n si nouvelle version
- Vérifier l'espace disque (logs)
- Renouveler les tokens OAuth si nécessaire

### Mise à jour de n8n

**Docker :**
```bash
docker-compose pull
docker-compose up -d
```

**npm :**
```bash
npm update -g n8n
```

### Backup

**Exporter les workflows :**
1. Dans n8n : Workflows → Sélectionner → Download
2. Sauvegarder le JSON dans votre repo Git

**Backup de la base de données :**
```bash
# Si Docker
docker-compose exec n8n n8n export:workflow --all --output=/data/backup.json
docker cp n8n:/data/backup.json ./backup-$(date +%Y%m%d).json
```

---

## 10. Troubleshooting

### Problème : "Workflow ne s'exécute pas"

**Solutions :**
- Vérifier que le workflow est "Active"
- Vérifier le cron expression
- Consulter les Executions pour voir les erreurs

### Problème : "LinkedIn API error"

**Solutions :**
- Reconnecter votre credential LinkedIn
- Vérifier les permissions de l'app LinkedIn
- Vérifier que le token n'a pas expiré

### Problème : "Google Sheets not found"

**Solutions :**
- Vérifier que le Sheet est bien partagé avec le Service Account
- Vérifier le nom exact du document et de l'onglet
- Reconnecter la credential Google

### Problème : "Out of memory"

**Solutions :**
- Augmenter la RAM du VPS
- Limiter le nombre d'exécutions simultanées
- Nettoyer les anciens logs

---

## 11. Ressources

### Documentation
- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community](https://community.n8n.io/)
- [n8n GitHub](https://github.com/n8n-io/n8n)

### Tutoriels Vidéo
- [n8n YouTube Channel](https://www.youtube.com/c/n8nio)

### Templates
- [n8n Workflows](https://n8n.io/workflows/)

---

## 🎉 Conclusion

Vous avez maintenant un système complet avec n8n ! 

**Avantages :**
- ✅ Gratuit (self-hosted)
- ✅ Open source
- ✅ Contrôle total
- ✅ Facile à maintenir
- ✅ Scalable

**Prochaines étapes :**
1. Installer n8n (local ou Railway)
2. Importer le workflow
3. Configurer les credentials
4. Tester avec un post
5. Activer et profiter !

Bon automatisation ! 🚀
