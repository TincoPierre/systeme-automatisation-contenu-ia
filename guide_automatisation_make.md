# Guide d'Automatisation de Publication avec Make.com

## Vue d'ensemble

Ce guide vous accompagne pas à pas dans la configuration d'un workflow Make.com pour automatiser la publication de vos posts LinkedIn et X (Twitter).

## Prérequis

### 1. Créer un compte Make.com
- Rendez-vous sur [make.com](https://www.make.com)
- Créez un compte gratuit (1000 opérations/mois incluses)
- Le plan gratuit est suffisant pour démarrer (environ 60 posts/mois = 180 opérations)

### 2. Préparer votre Google Sheet
- Importez le fichier `Calendrier_Editorial.xlsx` dans Google Drive
- Convertissez-le en Google Sheets (Fichier > Enregistrer au format Google Sheets)
- Notez l'URL du Google Sheet

### 3. Connecter vos comptes sociaux

#### LinkedIn
- Vous aurez besoin d'un compte LinkedIn (personnel ou page entreprise)
- Make.com se connectera via OAuth (connexion sécurisée)

#### X (Twitter)
- Vous aurez besoin d'un compte X avec accès à l'API
- **Important** : L'accès à l'API X nécessite un abonnement (Basic à 100$/mois minimum)
- **Alternative** : Utiliser Buffer ou Hootsuite qui ont déjà l'accès API

## Architecture du Workflow Make.com

```
┌─────────────────────────────────────────────────────────────┐
│                    WORKFLOW MAKE.COM                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. [TRIGGER] Schedule                                       │
│     └─ Tous les jours à 8h00                                │
│                                                              │
│  2. [GOOGLE SHEETS] Search Rows                             │
│     └─ Chercher : Statut = "Validé"                         │
│     └─ ET : Date Publication = Aujourd'hui                  │
│                                                              │
│  3. [FILTER] Vérifier si des posts trouvés                  │
│     └─ Si aucun post : Arrêter                              │
│                                                              │
│  4. [ITERATOR] Pour chaque post trouvé                      │
│     │                                                        │
│     ├─ 5a. [LINKEDIN] Create Post                           │
│     │    └─ Contenu : {{Brouillon LinkedIn}}                │
│     │                                                        │
│     ├─ 5b. [TWITTER] Create Tweet                           │
│     │    └─ Contenu : {{Brouillon Twitter}}                 │
│     │                                                        │
│     └─ 6. [GOOGLE SHEETS] Update Row                        │
│          └─ Statut = "Publié"                               │
│          └─ Date Publiée = {{now}}                          │
│          └─ URL LinkedIn = {{5a.url}}                       │
│          └─ URL Twitter = {{5b.url}}                        │
│                                                              │
│  7. [EMAIL] Notification                                    │
│     └─ "X posts publiés aujourd'hui"                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Configuration Pas à Pas

### Étape 1 : Créer un nouveau Scénario

1. Dans Make.com, cliquez sur **"Create a new scenario"**
2. Nommez-le : **"Publication Auto LinkedIn & Twitter"**

### Étape 2 : Ajouter le Trigger (Déclencheur)

1. Cliquez sur le **"+"** pour ajouter un module
2. Recherchez **"Schedule"**
3. Sélectionnez **"Schedule"** (l'icône horloge)
4. Configuration :
   - **Interval** : Every day
   - **Time** : 08:00 (ou l'heure souhaitée)
   - **Timezone** : Votre fuseau horaire

### Étape 3 : Connecter Google Sheets

1. Ajoutez un module **Google Sheets**
2. Sélectionnez **"Search Rows"**
3. Connectez votre compte Google
4. Configuration :
   - **Spreadsheet** : Sélectionnez votre Calendrier_Editorial
   - **Sheet** : Calendrier
   - **Filter** : 
     ```
     Statut = Validé
     AND
     Date Publication = {{formatDate(now; "YYYY-MM-DD")}}
     ```
   - **Maximum number of returned rows** : 10

### Étape 4 : Ajouter un Filtre

1. Ajoutez un module **Filter**
2. Nommez-le : "Vérifier posts à publier"
3. Configuration :
   - **Condition** : Total number of bundles > 0

### Étape 5 : Ajouter un Iterator

1. Ajoutez un module **Iterator**
2. Connectez-le au résultat de Google Sheets
3. Cela permettra de traiter chaque post individuellement

### Étape 6a : Publier sur LinkedIn

1. Ajoutez un module **LinkedIn**
2. Sélectionnez **"Create a Share Update"** (ou "Create Post")
3. Connectez votre compte LinkedIn
4. Configuration :
   - **Text** : `{{Brouillon LinkedIn}}`
   - **Visibility** : Public (ou selon préférence)

**Note** : Si vous publiez sur une Page Entreprise, sélectionnez l'option correspondante.

### Étape 6b : Publier sur X (Twitter)

1. Ajoutez un module **X (Twitter)**
2. Sélectionnez **"Create a Tweet"**
3. Connectez votre compte X
4. Configuration :
   - **Text** : `{{Brouillon Twitter}}`

**⚠️ Problème d'API X** : Si vous n'avez pas accès à l'API X (payant), utilisez une alternative :

#### Alternative 1 : Buffer
- Ajoutez un module **Buffer**
- Créez un compte Buffer (gratuit pour 3 canaux)
- Connectez X via Buffer
- Publiez via Buffer

#### Alternative 2 : Zapier
- Zapier a un meilleur support pour X
- Workflow similaire à Make.com

### Étape 7 : Mettre à jour Google Sheets

1. Ajoutez un module **Google Sheets**
2. Sélectionnez **"Update a Row"**
3. Configuration :
   - **Spreadsheet** : Votre Calendrier_Editorial
   - **Sheet** : Calendrier
   - **Row number** : `{{Iterator.Row Number}}`
   - **Statut** : Publié
   - **Date Publiée** : `{{formatDate(now; "YYYY-MM-DD HH:mm")}}`
   - **URL LinkedIn** : `{{LinkedIn.url}}` (si disponible)
   - **URL Twitter** : `{{Twitter.url}}` (si disponible)

### Étape 8 : Ajouter une Notification (Optionnel)

1. Ajoutez un module **Email**
2. Sélectionnez **"Send an Email"**
3. Configuration :
   - **To** : Votre email
   - **Subject** : `Posts publiés - {{formatDate(now; "DD/MM/YYYY")}}`
   - **Content** : 
     ```
     Bonjour,
     
     {{Iterator.Total bundles}} posts ont été publiés aujourd'hui.
     
     Détails :
     {{Iterator.Type}} - {{Iterator.Titre}}
     
     Bonne journée !
     ```

### Étape 9 : Tester le Workflow

1. Cliquez sur **"Run once"** en bas à gauche
2. Vérifiez que chaque module s'exécute correctement
3. Consultez les logs pour détecter les erreurs

### Étape 10 : Activer le Scénario

1. Une fois les tests concluants, cliquez sur **"ON"** en bas à gauche
2. Le workflow s'exécutera automatiquement chaque jour à l'heure définie

## Alternative : Workflow Simplifié avec Buffer

Si l'API X pose problème, voici un workflow alternatif :

```
1. [TRIGGER] Schedule (chaque jour à 8h)
2. [GOOGLE SHEETS] Search Rows (Statut = Validé, Date = Aujourd'hui)
3. [ITERATOR] Pour chaque post
4. [BUFFER] Create Post
   - Profiles : LinkedIn + X
   - Text : {{Brouillon LinkedIn}} (pour LinkedIn)
   - Text : {{Brouillon Twitter}} (pour X)
   - Schedule : Now
5. [GOOGLE SHEETS] Update Row (Statut = Publié)
```

**Avantages de Buffer** :
- Interface simple
- Pas besoin d'API X payante
- Gestion multi-comptes facile
- Planification visuelle

## Script Python pour Publication Locale (Alternative 100% Maison)

Si vous préférez éviter Make.com, voici un script Python à exécuter localement :

```python
# À créer : publish_posts.py
# Utilise les APIs LinkedIn et X directement
# Peut être exécuté via un cron job quotidien
```

**Avantages** :
- Contrôle total
- Pas de coût externe
- Personnalisation illimitée

**Inconvénients** :
- Nécessite un serveur toujours allumé
- Plus complexe à maintenir
- Gestion des erreurs manuelle

## Recommandations

### Pour Démarrer (0-3 mois)
✅ **Make.com + Buffer**
- Simple à configurer
- Peu coûteux (0-20€/mois)
- Validation manuelle facile

### Pour Scaler (3-12 mois)
✅ **Make.com + APIs Directes**
- Investir dans l'API X si volume élevé
- Automatisation complète
- Analytics intégrés

### Pour Industrialiser (12+ mois)
✅ **Solution Custom Python**
- Hébergement sur serveur dédié
- Intégration avec analytics
- Multi-comptes et multi-langues

## Checklist de Lancement

- [ ] Compte Make.com créé
- [ ] Google Sheet configuré et partagé
- [ ] Comptes LinkedIn et X connectés
- [ ] Workflow Make.com créé et testé
- [ ] 3-5 posts validés dans le calendrier
- [ ] Test de publication réussi
- [ ] Workflow activé
- [ ] Notification email configurée
- [ ] Calendrier de veille pour les 2 prochaines semaines

## Dépannage

### Problème : "No rows found"
- Vérifiez que le statut est bien "Validé" (avec accent)
- Vérifiez le format de date (YYYY-MM-DD)
- Vérifiez que la date correspond à aujourd'hui

### Problème : "LinkedIn API error"
- Reconnectez votre compte LinkedIn dans Make.com
- Vérifiez les permissions accordées
- Essayez de publier manuellement sur LinkedIn pour vérifier le compte

### Problème : "Twitter API not available"
- Utilisez Buffer comme alternative
- Ou souscrivez à l'API X Basic (100$/mois)

### Problème : "Rate limit exceeded"
- Réduisez la fréquence de publication
- Espacez les posts de quelques minutes
- Vérifiez les limites de votre plan Make.com

## Support et Ressources

- **Documentation Make.com** : https://www.make.com/en/help
- **API LinkedIn** : https://learn.microsoft.com/en-us/linkedin/
- **API X** : https://developer.twitter.com/en/docs
- **Buffer** : https://buffer.com/

## Prochaines Étapes

1. ✅ Configurer Make.com
2. ✅ Tester avec 3-5 posts
3. ⏳ Générer le contenu pour 2 semaines
4. ⏳ Valider les posts
5. ⏳ Activer l'automatisation
6. ⏳ Monitorer les performances
7. ⏳ Ajuster la stratégie selon les résultats
