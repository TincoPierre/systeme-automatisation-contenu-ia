# Guide Complet : Airtable + n8n

## 🎯 Vue d'ensemble

Ce guide vous montre comment utiliser **Airtable** comme base de données pour votre calendrier éditorial, et **n8n** pour automatiser la publication.

**Avantages par rapport à Google Sheets :**
- ✅ Interface plus intuitive et moderne
- ✅ Configuration n8n plus simple (pas d'OAuth compliqué)
- ✅ Vues multiples (tableau, calendrier, kanban)
- ✅ API plus rapide et fiable
- ✅ Application mobile excellente
- ✅ Gratuit jusqu'à 1200 lignes

---

## 📋 Table des matières

1. [Configuration Airtable](#configuration-airtable)
2. [Structure de la base](#structure-base)
3. [Import des données](#import-donnees)
4. [Configuration n8n](#configuration-n8n)
5. [Workflow complet](#workflow-complet)
6. [Utilisation quotidienne](#utilisation)

---

## 1. Configuration Airtable {#configuration-airtable}

### Créer un compte Airtable

1. **Aller sur [airtable.com](https://airtable.com)**
2. **Sign up** (gratuit)
   - Email + mot de passe
   - Ou connexion Google
3. **Vérifier l'email**

### Créer une base (workspace)

1. **Cliquer sur "Create a base"**
2. **Choisir "Start from scratch"**
3. **Nommer la base :** "Calendrier Editorial IA"
4. **Choisir une icône et couleur** (optionnel)

---

## 2. Structure de la Base {#structure-base}

### Créer la table "Posts"

Par défaut, Airtable crée une table. Renommez-la en **"Posts"**.

### Colonnes à créer

Cliquer sur **"+"** pour ajouter des colonnes :

| Nom de la colonne | Type | Options | Description |
|-------------------|------|---------|-------------|
| **ID** | Autonumber | - | ID unique auto-généré |
| **Type** | Single select | News, Outils, SaaS Story | Type de contenu |
| **Jour** | Single select | Lundi, Mardi, Jeudi | Jour de publication |
| **Date Publication** | Date | Format: DD/MM/YYYY | Date prévue |
| **Thème** | Single line text | - | Thème (pour SaaS Story) |
| **Sujet/Outil** | Single line text | - | Sujet ou nom de l'outil |
| **Titre** | Single line text | - | Titre du post (SaaS Story) |
| **Description** | Long text | - | Description/angle |
| **Brouillon LinkedIn** | Long text | - | Texte pour LinkedIn |
| **Brouillon Twitter** | Long text | - | Texte pour Twitter |
| **Statut** | Single select | À générer, À valider, Validé, Publié | Statut du post |
| **Date Publiée** | Date | Format: DD/MM/YYYY HH:mm | Date réelle de publication |
| **URL LinkedIn** | URL | - | Lien du post publié |
| **URL Twitter** | URL | - | Lien du tweet publié |
| **Notes** | Long text | - | Notes diverses |

### Configuration des Single Select

**Pour "Type" :**
- News (couleur rouge)
- Outils (couleur jaune)
- SaaS Story (couleur bleue)

**Pour "Jour" :**
- Lundi
- Mardi
- Jeudi

**Pour "Statut" :**
- À générer (gris)
- À valider (orange)
- Validé (vert)
- Publié (bleu)

---

## 3. Import des Données {#import-donnees}

### Option A : Import depuis Excel

1. **Dans Airtable, cliquer sur "Add or import"**
2. **Choisir "CSV or spreadsheet"**
3. **Uploader votre `Calendrier_Editorial.xlsx`**
4. **Mapper les colonnes** (Airtable détecte automatiquement)
5. **Import**

### Option B : Script Python pour peupler Airtable

**Installer la bibliothèque Airtable :**
```bash
pip3 install pyairtable
```

**Script `populate_airtable.py` :**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour peupler Airtable depuis le plan structuré
"""

from pyairtable import Api
import json
from datetime import datetime, timedelta

# Configuration
AIRTABLE_API_KEY = "votre_api_key"  # À obtenir depuis Airtable
AIRTABLE_BASE_ID = "votre_base_id"  # Dans l'URL de votre base
AIRTABLE_TABLE_NAME = "Posts"

# Initialiser l'API
api = Api(AIRTABLE_API_KEY)
table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)

# Charger le plan structuré
with open('plan_structure.json', 'r', encoding='utf-8') as f:
    plan = json.load(f)

# Date de début (lundi prochain)
today = datetime.now()
days_until_monday = (7 - today.weekday()) % 7
if days_until_monday == 0:
    days_until_monday = 7
date_debut = today + timedelta(days=days_until_monday)

print("🚀 Peuplement d'Airtable...")

# Mapping des jours
jour_to_offset = {
    "Lundi": 0,
    "Mardi": 1,
    "Jeudi": 3
}

# Calculer le nombre de semaines
max_items = max(len(plan['news']), len(plan['outils']), len(plan['saas_story']))

records_created = 0

# Générer les posts pour chaque semaine
for semaine in range(max_items):
    date_semaine = date_debut + timedelta(weeks=semaine)
    
    # News (Lundi)
    if semaine < len(plan['news']):
        item = plan['news'][semaine]
        record = {
            "Type": "News",
            "Jour": "Lundi",
            "Date Publication": (date_semaine + timedelta(days=0)).strftime('%Y-%m-%d'),
            "Sujet/Outil": item['sujet'],
            "Statut": "À générer"
        }
        table.create(record)
        records_created += 1
        print(f"  ✓ News - {item['sujet']}")
    
    # Outils (Mardi)
    if semaine < len(plan['outils']):
        item = plan['outils'][semaine]
        record = {
            "Type": "Outils",
            "Jour": "Mardi",
            "Date Publication": (date_semaine + timedelta(days=1)).strftime('%Y-%m-%d'),
            "Sujet/Outil": item['outil'],
            "Statut": "À générer"
        }
        table.create(record)
        records_created += 1
        print(f"  ✓ Outils - {item['outil']}")
    
    # SaaS Story (Jeudi)
    if semaine < len(plan['saas_story']):
        item = plan['saas_story'][semaine]
        record = {
            "Type": "SaaS Story",
            "Jour": "Jeudi",
            "Date Publication": (date_semaine + timedelta(days=3)).strftime('%Y-%m-%d'),
            "Thème": item['theme'],
            "Titre": item['titre'],
            "Description": item['description'],
            "Statut": "À générer"
        }
        table.create(record)
        records_created += 1
        print(f"  ✓ SaaS Story - {item['titre']}")

print(f"\n✅ {records_created} posts créés dans Airtable !")
```

**Exécuter le script :**
```bash
python3 populate_airtable.py
```

---

## 4. Configuration n8n {#configuration-n8n}

### Obtenir les credentials Airtable

**1. API Key :**
- Aller sur https://airtable.com/account
- Section "API"
- Cliquer sur "Generate API key"
- **Copier la clé** (commence par `key...`)

**2. Base ID :**
- Ouvrir votre base Airtable
- Regarder l'URL : `https://airtable.com/appXXXXXXXXXXXXXX/...`
- Le `appXXXXXXXXXXXXXX` est votre Base ID
- **Copier le Base ID**

**3. Table Name :**
- Le nom de votre table : `Posts`

### Configurer les credentials dans n8n

1. **Dans n8n : Settings → Credentials**
2. **Add Credential → Airtable API**
3. **Remplir :**
   - **API Key :** Coller votre clé API
   - **Name :** "Airtable - Calendrier Editorial"
4. **Test** (optionnel)
5. **Save**

---

## 5. Workflow Complet {#workflow-complet}

### Architecture du workflow

```
┌────────────────────────────────────────────────────────┐
│              WORKFLOW AIRTABLE + n8n                    │
├────────────────────────────────────────────────────────┤
│                                                         │
│  1. [Schedule Trigger]                                 │
│     └─ Tous les jours à 8h30                          │
│                                                         │
│  2. [Airtable - List Records]                         │
│     └─ Filter: Statut = "Validé"                      │
│     └─ Filter: Date Publication = TODAY()             │
│                                                         │
│  3. [IF Node]                                         │
│     └─ Des posts à publier ?                          │
│                                                         │
│  4. [Loop Over Items]                                 │
│     └─ Pour chaque post trouvé                        │
│                                                         │
│  5. [LinkedIn - Create Post]                          │
│     └─ Publier le brouillon LinkedIn                  │
│                                                         │
│  6. [Twitter - Create Tweet] (Optionnel)              │
│     └─ Publier le brouillon Twitter                   │
│                                                         │
│  7. [Airtable - Update Record]                        │
│     └─ Statut → "Publié"                              │
│     └─ Date Publiée → NOW()                           │
│     └─ URLs des posts                                 │
│                                                         │
│  8. [Send Email]                                      │
│     └─ Notification de succès                         │
│                                                         │
└────────────────────────────────────────────────────────┘
```

### Configuration des nodes

#### Node 1 : Schedule Trigger

**Configuration :**
- **Mode :** Cron
- **Cron Expression :** `30 8 * * *`
- **Timezone :** Europe/Paris

#### Node 2 : Airtable - List Records

**Configuration :**
- **Credential :** Airtable - Calendrier Editorial
- **Operation :** List
- **Base :** Votre Base ID (ou sélectionner dans la liste)
- **Table :** Posts

**Filter Formula :**
```
AND(
  {Statut} = "Validé",
  IS_SAME({Date Publication}, TODAY(), 'day')
)
```

**Options :**
- **Return All :** true
- **Download Attachments :** false

#### Node 3 : IF Node

**Configuration :**
- **Condition :** `{{ $json.id }}` is not empty

#### Node 4 : LinkedIn - Create Post

**Configuration :**
- **Credential :** LinkedIn OAuth2
- **Resource :** Post
- **Operation :** Create
- **Text :** `{{ $json.fields['Brouillon LinkedIn'] }}`
- **Visibility :** PUBLIC

#### Node 5 : Twitter - Create Tweet (Optionnel)

**Configuration :**
- **Method :** POST
- **URL :** `https://api.twitter.com/2/tweets`
- **Authentication :** OAuth1
- **Body :**
```json
{
  "text": "{{ $json.fields['Brouillon Twitter'] }}"
}
```

#### Node 6 : Airtable - Update Record

**Configuration :**
- **Credential :** Airtable - Calendrier Editorial
- **Operation :** Update
- **Base :** Votre Base ID
- **Table :** Posts
- **Record ID :** `{{ $json.id }}`

**Fields to Update :**
```json
{
  "Statut": "Publié",
  "Date Publiée": "{{ $now.toISO() }}",
  "URL LinkedIn": "{{ $node['LinkedIn - Create Post'].json.url }}",
  "URL Twitter": "{{ $node['Twitter - Create Tweet'].json.data?.id }}"
}
```

#### Node 7 : Send Email

**Configuration :**
- **To :** votre-email@example.com
- **Subject :** `✅ Posts publiés - {{ $now.format('dd/MM/yyyy') }}`
- **Text :**
```
Bonjour,

{{ $json.count || 1 }} post(s) ont été publiés avec succès.

Type : {{ $json.fields.Type }}
LinkedIn : {{ $node['LinkedIn - Create Post'].json.url }}

Bonne journée !
```

---

## 6. Workflow JSON Prêt à Importer

Voir le fichier `workflow_airtable_publication.json` dans le repo.

---

## 7. Utilisation Quotidienne {#utilisation}

### Ajouter un nouveau post

**Dans Airtable :**

1. **Cliquer sur "+"** en bas de la table
2. **Remplir les champs :**
   - Type : News / Outils / SaaS Story
   - Jour : Lundi / Mardi / Jeudi
   - Date Publication : 2025-10-25
   - Sujet/Outil : "ChatGPT"
   - Statut : "À générer"
3. **Save**

### Générer le contenu

**Option A : Manuellement avec le script Python**

```bash
# Générer pour un post spécifique
python3 generer_post_airtable.py --record-id recXXXXXXXXXXXXXX
```

**Option B : Workflow n8n de génération**

Créer un workflow séparé qui :
1. Lit les posts avec statut "À générer"
2. Appelle OpenAI pour générer les brouillons
3. Met à jour Airtable avec les brouillons
4. Change le statut à "À valider"

### Valider un post

**Dans Airtable :**

1. **Ouvrir le post**
2. **Lire les brouillons** LinkedIn et Twitter
3. **Ajuster si nécessaire**
4. **Changer le statut** à "Validé"
5. **Save**

### Vérifier les posts publiés

**Dans Airtable :**

1. **Créer une vue "Publiés"**
   - Filter : Statut = "Publié"
   - Sort : Date Publiée (descending)
2. **Voir les URLs** des posts publiés
3. **Analyser les performances**

---

## 8. Vues Airtable Utiles

### Vue Calendrier

1. **Cliquer sur "Grid view" → Create → Calendar**
2. **Nommer :** "Calendrier de Publication"
3. **Date field :** Date Publication
4. **Color by :** Type

**Résultat :** Visualisation calendrier de tous vos posts

### Vue Kanban

1. **Create → Kanban**
2. **Nommer :** "Pipeline de Publication"
3. **Stack by :** Statut

**Résultat :** Voir les posts par statut (À générer, À valider, Validé, Publié)

### Vue Filtrée "Cette Semaine"

1. **Dupliquer la vue principale**
2. **Nommer :** "Cette Semaine"
3. **Filter :**
   - Date Publication is within → this week

**Résultat :** Voir uniquement les posts de la semaine

---

## 9. Script Python pour Générer le Contenu

**Fichier `generer_post_airtable.py` :**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Générer le contenu des posts Airtable avec OpenAI
"""

from pyairtable import Api
from openai import OpenAI
import os

# Configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = "Posts"

# Initialiser les APIs
airtable_api = Api(AIRTABLE_API_KEY)
table = airtable_api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
openai_client = OpenAI()

# Prompts (réutiliser ceux de content_generator.py)
PROMPTS = {
    "news": {
        "linkedin": "Tu es un expert en IA...",
        "twitter": "Tu es un expert en IA..."
    },
    "outils": {
        "linkedin": "Tu es un expert en outils IA...",
        "twitter": "Tu es un expert en outils IA..."
    },
    "saas_story": {
        "linkedin": "Tu es un entrepreneur...",
        "twitter": "Tu es un entrepreneur..."
    }
}

def generer_post(type_contenu, plateforme, **kwargs):
    """Générer un post avec OpenAI"""
    prompt_template = PROMPTS[type_contenu.lower().replace(" ", "_")][plateforme]
    prompt = prompt_template.format(**kwargs)
    
    response = openai_client.chat.completions.create(
        model="gpt-4-mini",
        messages=[
            {"role": "system", "content": "Tu es un expert en création de contenu."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=500
    )
    
    return response.choices[0].message.content.strip()

def generer_posts_airtable():
    """Générer le contenu pour tous les posts 'À générer'"""
    
    # Récupérer les posts à générer
    formula = "{Statut} = 'À générer'"
    records = table.all(formula=formula)
    
    print(f"🚀 {len(records)} posts à générer\n")
    
    for record in records:
        fields = record['fields']
        record_id = record['id']
        
        print(f"Génération pour : {fields.get('Sujet/Outil') or fields.get('Titre')}")
        
        # Déterminer le type et générer
        type_contenu = fields['Type']
        
        if type_contenu == "News":
            linkedin = generer_post("news", "linkedin", sujet=fields['Sujet/Outil'])
            twitter = generer_post("news", "twitter", sujet=fields['Sujet/Outil'])
        
        elif type_contenu == "Outils":
            linkedin = generer_post("outils", "linkedin", outil=fields['Sujet/Outil'])
            twitter = generer_post("outils", "twitter", outil=fields['Sujet/Outil'])
        
        elif type_contenu == "SaaS Story":
            linkedin = generer_post("saas_story", "linkedin", 
                                   titre=fields['Titre'], 
                                   description=fields['Description'])
            twitter = generer_post("saas_story", "twitter", 
                                  titre=fields['Titre'], 
                                  description=fields['Description'])
        
        # Mettre à jour Airtable
        table.update(record_id, {
            "Brouillon LinkedIn": linkedin,
            "Brouillon Twitter": twitter,
            "Statut": "À valider"
        })
        
        print(f"  ✅ Généré et mis à jour\n")
    
    print(f"✅ Tous les posts ont été générés !")

if __name__ == "__main__":
    generer_posts_airtable()
```

**Utilisation :**
```bash
# Configurer les variables
export AIRTABLE_API_KEY="keyXXXXXXXXXXXXXX"
export AIRTABLE_BASE_ID="appXXXXXXXXXXXXXX"

# Générer
python3 generer_post_airtable.py
```

---

## 10. Avantages d'Airtable vs Google Sheets

| Fonctionnalité | Airtable | Google Sheets |
|----------------|----------|---------------|
| **Interface** | ⭐⭐⭐⭐⭐ Moderne et intuitive | ⭐⭐⭐ Classique |
| **Vues multiples** | ✅ Calendrier, Kanban, Galerie | ❌ Seulement tableau |
| **API** | ⭐⭐⭐⭐⭐ Simple, rapide | ⭐⭐⭐ OAuth compliqué |
| **n8n Integration** | ✅ Node natif, facile | ⚠️ OAuth requis |
| **Mobile App** | ⭐⭐⭐⭐⭐ Excellente | ⭐⭐⭐ Bonne |
| **Collaboration** | ✅ Commentaires, mentions | ✅ Commentaires |
| **Formules** | ⭐⭐⭐⭐ Puissantes | ⭐⭐⭐⭐⭐ Très puissantes |
| **Gratuit** | ✅ 1200 lignes | ✅ Illimité |

---

## 11. Limites du Plan Gratuit

**Airtable Free :**
- 1200 lignes par base (largement suffisant pour 1200 posts)
- 2 Go de stockage
- 2 semaines d'historique de révisions
- API : 5 requêtes/seconde

**Si vous dépassez :**
- Plan Plus : 10$/utilisateur/mois
- 5000 lignes par base
- 5 Go de stockage

---

## 12. Conclusion

**Airtable + n8n = Combo Parfait**

✅ **Plus simple** que Google Sheets
✅ **Plus beau** et agréable à utiliser
✅ **Plus rapide** à configurer dans n8n
✅ **Plus flexible** avec les vues multiples
✅ **Gratuit** pour votre usage

**Prochaines étapes :**

1. ✅ Créer votre base Airtable
2. ✅ Importer vos données
3. ✅ Configurer n8n avec Airtable
4. ✅ Importer le workflow
5. ✅ Tester et activer

Bon automatisation ! 🚀
