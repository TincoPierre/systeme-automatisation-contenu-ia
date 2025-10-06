# Architecture du Système d'Automatisation de Contenu

## Vue d'ensemble

Le système d'automatisation proposé permet de générer et publier automatiquement du contenu sur LinkedIn et X (Twitter) en s'appuyant sur trois piliers de contenu :

1. **News IA** (Lundi) - Actualités et nouveautés du monde de l'IA
2. **Outils IA** (Mardi) - Présentation d'outils innovants
3. **SaaS Story** (Jeudi) - Storytelling autour du lancement d'un SaaS

## Architecture Technique

### 1. Base de Données de Contenu (Google Sheets / Airtable)

**Structure proposée :**

| Colonne | Description | Exemple |
|---------|-------------|---------|
| `id` | Identifiant unique | 1, 2, 3... |
| `type_contenu` | News / Outils / SaaS Story | "Outils" |
| `jour_publication` | Jour de la semaine | "Mardi" |
| `theme` | Thème principal | "Validation" |
| `sujet` | Sujet ou outil à traiter | "ChatGPT" |
| `titre` | Titre du post | "Pourquoi je lance ce SaaS" |
| `description` | Description/angle | "Raconter la genèse..." |
| `brouillon_linkedin` | Texte généré pour LinkedIn | [Généré par IA] |
| `brouillon_twitter` | Texte généré pour X | [Généré par IA] |
| `statut` | À générer / À valider / Validé / Publié | "À valider" |
| `date_publication` | Date prévue de publication | "2025-10-14" |
| `date_publie` | Date réelle de publication | "2025-10-14 09:00" |
| `url_linkedin` | Lien du post publié | https://... |
| `url_twitter` | Lien du post publié | https://... |

### 2. Générateur de Contenu (Python + API OpenAI)

**Fonctionnement :**

Un script Python qui :
- Lit les lignes avec `statut = "À générer"` dans la base de données
- Pour chaque ligne, appelle l'API OpenAI (GPT-4) avec un prompt adapté au type de contenu
- Génère deux versions : une pour LinkedIn (plus longue, professionnelle) et une pour X (concise, percutante)
- Met à jour la base de données avec les brouillons générés
- Change le statut à "À valider"

**Prompts personnalisés par type :**

- **News IA** : Résumer une actualité IA de manière accessible et engageante
- **Outils IA** : Présenter un outil avec ses fonctionnalités clés et cas d'usage
- **SaaS Story** : Raconter une étape du parcours entrepreneurial avec authenticité

### 3. Système de Validation

**Options :**

**Option A - Validation Manuelle :**
- Vous recevez une notification (email/Slack) quand de nouveaux brouillons sont prêts
- Vous les consultez dans le Google Sheet
- Vous modifiez si nécessaire et changez le statut à "Validé"

**Option B - Validation Semi-Automatique :**
- Un dashboard simple (Streamlit ou Flask) affiche les brouillons
- Interface de validation en un clic avec possibilité d'édition rapide
- Plus ergonomique que Google Sheets

**Option C - Validation Automatique :**
- Les posts sont publiés automatiquement après génération
- Risqué au début, recommandé seulement après avoir testé la qualité des générations

**Recommandation : Option A au début, puis Option B une fois le système rodé.**

### 4. Planificateur de Publication (Make.com ou Zapier)

**Workflow Make.com :**

```
[Trigger: Chaque jour à 8h00]
    ↓
[Google Sheets: Lire les lignes avec statut="Validé" et date_publication=aujourd'hui]
    ↓
[Router: Séparer LinkedIn et Twitter]
    ↓
[LinkedIn API: Publier le post]    [Twitter API: Publier le post]
    ↓                                ↓
[Google Sheets: Mettre à jour statut="Publié" et date_publie]
    ↓
[Notification: Envoyer confirmation par email/Slack]
```

**Alternatives :**
- **Buffer** : Interface simple, planification visuelle
- **Hootsuite** : Plus complet mais plus cher
- **Script Python + Cron** : Solution 100% maison, plus de contrôle

### 5. Système de Veille Automatisée (Bonus)

Pour alimenter automatiquement la colonne "News IA" :

**Option 1 - RSS + Filtrage IA :**
- Agréger les flux RSS de sources fiables (ActuIA, TechCrunch, etc.)
- Utiliser une IA pour filtrer et résumer les actualités les plus pertinentes
- Ajouter automatiquement dans la base de données

**Option 2 - API de News :**
- Utiliser des APIs comme NewsAPI ou Google News API
- Filtrer par mots-clés : "intelligence artificielle", "IA", "AI", etc.
- Résumer avec GPT-4

**Option 3 - Web Scraping :**
- Script qui visite les sites d'actualité IA
- Extrait les titres et résumés
- Alimente la base de données

## Flux de Travail Complet

```
Semaine N-1:
1. Générateur de contenu s'exécute (dimanche soir)
   → Génère les brouillons pour la semaine suivante
   
2. Notification envoyée (lundi matin)
   → Vous recevez les brouillons à valider

3. Validation (lundi-mardi)
   → Vous validez/modifiez les posts dans le dashboard

Semaine N:
4. Publication automatique (selon calendrier)
   → Lundi 9h: Post News IA
   → Mardi 9h: Post Outils IA
   → Jeudi 9h: Post SaaS Story

5. Suivi et analytics
   → Statistiques de performance collectées
   → Ajustements du système si nécessaire
```

## Technologies Recommandées

| Composant | Solution Recommandée | Alternative |
|-----------|---------------------|-------------|
| Base de données | Google Sheets | Airtable, Notion |
| Génération de contenu | Python + OpenAI API | Claude API, Anthropic |
| Validation | Google Sheets | Dashboard Streamlit |
| Publication | Make.com | Zapier, Buffer |
| Veille | RSS + Python | Feedly, Inoreader |
| Hébergement script | GitHub Actions | Heroku, Railway |

## Coûts Estimés

| Service | Coût mensuel | Notes |
|---------|--------------|-------|
| OpenAI API | 10-30€ | Dépend du volume (GPT-4-mini recommandé) |
| Make.com | 0-9€ | Plan gratuit puis Core à 9€/mois |
| Google Sheets | 0€ | Gratuit |
| Hébergement | 0€ | GitHub Actions gratuit pour usage léger |
| **TOTAL** | **10-40€/mois** | Très abordable pour un système complet |

## Prochaines Étapes

1. ✅ Analyser le plan marketing existant
2. ✅ Concevoir l'architecture du système
3. ⏳ Développer le script de génération de contenu
4. ⏳ Configurer le workflow Make.com
5. ⏳ Tester le système en mode manuel
6. ⏳ Automatiser progressivement

## Notes Importantes

- **Commencer simple** : Validation manuelle au début pour garantir la qualité
- **Itérer progressivement** : Automatiser davantage une fois le système rodé
- **Surveiller la qualité** : L'IA peut parfois générer du contenu générique
- **Personnaliser les prompts** : Affiner les instructions pour coller à votre voix
- **Respecter les limites des APIs** : LinkedIn et X ont des quotas de publication
