# Système d'Automatisation de Contenu IA

## Vue d'ensemble

Ce système complet vous permet de **générer et publier automatiquement du contenu** sur LinkedIn et X (Twitter) autour de l'intelligence artificielle et de l'automatisation.

### Objectifs
- 📰 Partager les dernières actualités IA (Lundi)
- 🛠️ Présenter des outils innovants (Mardi)
- 📖 Raconter votre parcours SaaS (Jeudi)

### Résultat
Un calendrier éditorial de **62 posts** prêts à être générés et publiés automatiquement sur 6 mois.

## Architecture du Système

```
┌─────────────────────────────────────────────────────────────┐
│                    SYSTÈME COMPLET                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. VEILLE                                                   │
│     └─ Newsletters + RSS + Réseaux sociaux                  │
│     └─ Identification des sujets pertinents                 │
│                                                              │
│  2. PLANIFICATION                                           │
│     └─ Calendrier_Editorial.xlsx                            │
│     └─ 3 posts/semaine (Lundi, Mardi, Jeudi)               │
│                                                              │
│  3. GÉNÉRATION                                              │
│     └─ content_generator.py                                 │
│     └─ OpenAI GPT-4 pour créer les posts                   │
│     └─ 2 versions : LinkedIn + Twitter                     │
│                                                              │
│  4. VALIDATION                                              │
│     └─ Révision manuelle dans Excel                        │
│     └─ Ajustements si nécessaire                           │
│                                                              │
│  5. PUBLICATION                                             │
│     └─ n8n (automatique, open source)                      │
│     └─ Publication selon calendrier                         │
│                                                              │
│  6. SUIVI                                                   │
│     └─ URLs sauvegardées dans Excel                        │
│     └─ Analytics pour optimisation                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Fichiers du Système

### 📊 Données et Planification
- **`Calendrier_Editorial.xlsx`** : Calendrier complet avec 62 posts planifiés
- **`plan_structure.json`** : Données structurées du plan marketing original

### 🤖 Scripts de Génération
- **`content_generator.py`** : Générateur de contenu avec OpenAI
- **`generer_batch.py`** : Génération en masse de posts
- **`export_to_excel.py`** : Export vers Excel formaté

### 📖 Guides et Documentation
- **`README.md`** : Ce fichier (vue d'ensemble)
- **`QUICKSTART_N8N.md`** : Démarrage rapide n8n (10 minutes)
- **`guide_n8n.md`** : Guide complet n8n (recommandé)
- **`guide_automatisation_make.md`** : Configuration Make.com (alternative)
- **`guide_veille_automatisee.md`** : Système de veille continue
- **`architecture_systeme.md`** : Architecture technique détaillée

### 🔧 Configuration n8n
- **`workflow_publication_auto.json`** : Workflow n8n prêt à importer
- **`docker-compose.yml`** : Configuration Docker pour n8n
- **`.env.example`** : Variables d'environnement

## Installation et Configuration

### Prérequis
- Python 3.11+ (pour la génération de contenu)
- Node.js 18+ ou Docker (pour n8n)
- Compte OpenAI avec API key
- Compte Google (pour Google Sheets)
- Comptes LinkedIn et X (Twitter)

### Installation

#### 1. Génération de Contenu (Python)

```bash
# Installer les dépendances Python
pip3 install -r requirements.txt

# Configurer l'API OpenAI
export OPENAI_API_KEY="votre-clé-api"

# Vérifier l'installation
python3 content_generator.py
```

#### 2. Automatisation (n8n)

**Option A : Docker (Recommandé)**
```bash
# Copier la configuration
cp .env.example .env

# Éditer et changer le mot de passe
nano .env

# Démarrer n8n
docker-compose up -d

# Accéder à http://localhost:5678
```

**Option B : npm**
```bash
# Installer n8n globalement
npm install -g n8n

# Démarrer n8n
n8n start

# Accéder à http://localhost:5678
```

**Option C : Railway (Cloud)**
- Créer un compte sur [railway.app](https://railway.app)
- Deploy n8n template
- Importer le workflow

📖 **Guide complet :** Voir `QUICKSTART_N8N.md` pour plus de détails

## Utilisation

### Étape 1 : Générer le Contenu

**Générer 3 posts de test** :
```bash
python3 generer_batch.py test
```

**Générer 5 posts** (par défaut) :
```bash
python3 generer_batch.py
```

**Générer TOUS les posts** (62 posts) :
```bash
python3 generer_batch.py all
```

**Afficher les statistiques** :
```bash
python3 generer_batch.py stats
```

### Étape 2 : Valider les Posts

1. Ouvrir `Calendrier_Editorial.xlsx`
2. Consulter les colonnes "Brouillon LinkedIn" et "Brouillon Twitter"
3. Ajuster le contenu si nécessaire
4. Changer le statut de "À valider" à "Validé"

### Étape 3 : Configurer l'Automatisation avec n8n

Suivre le guide détaillé dans `guide_n8n.md` ou le quickstart `QUICKSTART_N8N.md` :

1. Installer et démarrer n8n (voir section Installation ci-dessus)
2. Importer le workflow `workflow_publication_auto.json`
3. Configurer les credentials (OpenAI, Google Sheets, LinkedIn)
4. Importer le calendrier dans Google Sheets
5. Tester le workflow manuellement
6. Activer le workflow (publication automatique à 8h30)

**Alternative :** Vous pouvez aussi utiliser Make.com (voir `guide_automatisation_make.md`)

### Étape 4 : Mettre en Place la Veille

Suivre le guide dans `guide_veille_automatisee.md` :

1. S'abonner aux newsletters recommandées
2. Configurer Feedly avec les flux RSS
3. Suivre les experts sur X et LinkedIn
4. Créer une routine quotidienne (15 min)

## Exemples de Posts Générés

### Post LinkedIn - Outil IA (ChatGPT)

```
Vous passez trop de temps à rédiger des emails, des rapports ou à 
chercher des idées ? Vous n'êtes pas seul. La création de contenu 
peut vite devenir un gouffre de productivité.

C'est là que ChatGPT entre en jeu. Ce modèle d'IA développé par 
OpenAI révolutionne la manière dont nous générons du texte, en 
offrant des réponses instantanées, précises et personnalisées.

Voici pourquoi ChatGPT est un atout indispensable :

• Rédaction rapide et fluide : Que ce soit pour un email 
  professionnel, un article LinkedIn ou un résumé de réunion, 
  ChatGPT vous aide à formuler vos idées en quelques secondes.

• Idéation et brainstorming : Besoin d'inspiration pour un projet 
  ou une campagne marketing ? L'outil propose des suggestions 
  créatives adaptées à votre contexte.

• Assistance multilingue : Traduction, reformulation ou rédaction 
  dans plusieurs langues pour toucher un public global.

Et vous, avez-vous déjà testé ChatGPT pour booster votre 
productivité ? N'hésitez pas à partager votre expérience !
```

### Post Twitter - Outil IA (ChatGPT)

```
Découvrez ChatGPT, l'IA qui booste votre productivité en générant 
des réponses rapides et précises 🤖✨. Parfait pour rédiger des 
emails pro ou brainstormer des idées créatives. 

#IA #Outils #Productivité
```

## Calendrier de Publication

| Jour | Type de Contenu | Exemple de Sujet |
|------|----------------|------------------|
| **Lundi** | News IA | "OpenAI lance GPT-5 : ce qui change" |
| **Mardi** | Outils IA | "ChatGPT : l'assistant IA indispensable" |
| **Jeudi** | SaaS Story | "Pourquoi je lance ce SaaS" |

**Fréquence** : 3 posts/semaine = 12 posts/mois = 144 posts/an

## Coûts Estimés

| Service | Coût mensuel | Notes |
|---------|--------------|-------|
| OpenAI API | 10-30€ | GPT-4-mini recommandé |
| Make.com | 0-9€ | Plan gratuit puis Core |
| Google Sheets | 0€ | Gratuit |
| Buffer (optionnel) | 0-6€ | Si problème API X |
| **TOTAL** | **10-45€/mois** | Très abordable |

## Métriques de Succès

### Semaine 1-2 (Test)
- ✅ 6 posts publiés
- ✅ Système fonctionnel
- ✅ Premiers retours

### Mois 1 (Rodage)
- 📊 12 posts publiés
- 📈 Engagement moyen par post
- 🔧 Ajustements du système

### Mois 3 (Optimisation)
- 📊 36 posts publiés
- 📈 Croissance de l'audience
- 🎯 Identification des sujets performants

### Mois 6 (Industrialisation)
- 📊 72 posts publiés
- 📈 Communauté engagée
- 🚀 Passage à la vidéo courte

## Roadmap

### Phase 1 : Lancement (Semaines 1-4) ✅
- [x] Analyser le plan marketing
- [x] Créer l'architecture du système
- [x] Développer les scripts de génération
- [x] Configurer l'automatisation
- [ ] Publier les premiers posts

### Phase 2 : Optimisation (Mois 2-3)
- [ ] Analyser les performances
- [ ] Ajuster les prompts de génération
- [ ] Optimiser les horaires de publication
- [ ] Enrichir la base d'outils

### Phase 3 : Expansion (Mois 4-6)
- [ ] Ajouter d'autres plateformes (Instagram, TikTok)
- [ ] Passer au format vidéo court
- [ ] Automatiser la veille avec IA
- [ ] Créer une base de connaissances

### Phase 4 : Industrialisation (Mois 6+)
- [ ] Multi-comptes et multi-langues
- [ ] Analytics avancés
- [ ] A/B testing automatisé
- [ ] Monétisation du contenu

## Support et Maintenance

### Tâches Quotidiennes (15 min)
- Veille matinale (newsletters + RSS)
- Vérification des publications du jour

### Tâches Hebdomadaires (30 min)
- Validation des posts de la semaine suivante
- Ajout de nouveaux sujets au calendrier
- Analyse des performances

### Tâches Mensuelles (1h)
- Génération en masse du contenu
- Optimisation des prompts
- Mise à jour de la liste d'outils

## Dépannage

### Problème : "OpenAI API error"
```bash
# Vérifier la clé API
echo $OPENAI_API_KEY

# Réinstaller le package
pip3 install --upgrade openai
```

### Problème : "Excel file corrupted"
```bash
# Régénérer le calendrier
python3 export_to_excel.py
```

### Problème : "Make.com workflow failed"
- Vérifier les connexions aux APIs
- Consulter les logs Make.com
- Tester manuellement chaque module

## Ressources Utiles

### Documentation
- [OpenAI API](https://platform.openai.com/docs)
- [Make.com Help](https://www.make.com/en/help)
- [LinkedIn API](https://learn.microsoft.com/en-us/linkedin/)
- [X API](https://developer.twitter.com/en/docs)

### Communautés
- Reddit : r/artificial, r/MachineLearning
- Discord : OpenAI, Hugging Face
- LinkedIn : Groupes IA francophones

### Outils Complémentaires
- **Canva** : Créer des visuels pour les posts
- **Grammarly** : Corriger les textes
- **Notion** : Organiser la veille
- **Buffer** : Alternative à Make.com

## Contribuer

Ce système est conçu pour être modulaire et extensible. Vous pouvez :

- Ajouter de nouveaux types de contenu
- Créer des prompts personnalisés
- Intégrer d'autres plateformes
- Améliorer les scripts Python

## Licence

Ce projet est fourni "tel quel" pour un usage personnel ou commercial.

## Contact et Support

Pour toute question ou suggestion :
- Créer une issue sur GitHub
- Me contacter via LinkedIn
- Rejoindre la communauté Discord

---

**Prêt à lancer votre machine à contenu IA ?** 🚀

Commencez par générer vos 3 premiers posts :
```bash
python3 generer_batch.py test
```

Puis consultez le guide d'automatisation :
```bash
cat guide_automatisation_make.md
```

Bon lancement ! 🎉
