# 🚀 Démarrage Rapide Airtable

Guide ultra-rapide pour utiliser Airtable avec votre système de publication automatique.

## ⏱️ Temps estimé : 15 minutes

---

## Étape 1 : Créer votre Base Airtable (5 min)

### 1.1 Créer un compte

1. Aller sur [airtable.com](https://airtable.com)
2. Sign up (gratuit)
3. Vérifier l'email

### 1.2 Créer la base

1. Cliquer sur **"Create a base"**
2. **"Start from scratch"**
3. Nommer : **"Calendrier Editorial IA"**

### 1.3 Créer les colonnes

Renommer la table en **"Posts"**, puis ajouter ces colonnes :

| Colonne | Type | Options |
|---------|------|---------|
| ID | Autonumber | (déjà présent) |
| Type | Single select | News, Outils, SaaS Story |
| Jour | Single select | Lundi, Mardi, Jeudi |
| Date Publication | Date | Format: DD/MM/YYYY |
| Sujet/Outil | Single line text | - |
| Titre | Single line text | - |
| Description | Long text | - |
| Brouillon LinkedIn | Long text | - |
| Brouillon Twitter | Long text | - |
| Statut | Single select | À générer, À valider, Validé, Publié |
| Date Publiée | Date | Format: DD/MM/YYYY HH:mm |
| URL LinkedIn | URL | - |
| URL Twitter | URL | - |

**Astuce :** Utilisez des couleurs pour les Single select !

---

## Étape 2 : Obtenir les Credentials (2 min)

### 2.1 API Key

1. Aller sur https://airtable.com/account
2. Section **"API"**
3. **"Generate API key"**
4. **Copier la clé** (commence par `key...`)

### 2.2 Base ID

1. Ouvrir votre base Airtable
2. Regarder l'URL : `https://airtable.com/appXXXXXXXXXXXXXX/...`
3. **Copier** le `appXXXXXXXXXXXXXX`

---

## Étape 3 : Peupler Airtable (3 min)

### 3.1 Configurer les variables

```bash
export AIRTABLE_TOKEN="patXXXXXXXXXXXXXX"
export AIRTABLE_BASE_ID="appXXXXXXXXXXXXXX"
export OPENAI_API_KEY="sk-XXXXXXXXXXXXXXXX"
```

### 3.2 Installer les dépendances

```bash
pip3 install pyairtable
```

### 3.3 Peupler la base

```bash
python3 populate_airtable.py
```

**Résultat :** 62 posts créés dans Airtable avec le statut "À générer"

---

## Étape 4 : Générer le Contenu (5 min)

```bash
python3 generer_post_airtable.py
```

**Résultat :** Tous les posts ont maintenant des brouillons LinkedIn et Twitter, statut "À valider"

---

## Étape 5 : Configurer n8n (5 min)

### 5.1 Dans n8n

1. **Settings → Credentials → Add Credential**
2. Chercher **"Airtable API"**
3. **API Key :** Coller votre clé
4. **Save**

### 5.2 Importer le workflow

1. **Workflows → Import from File**
2. Sélectionner `workflow_airtable_publication.json`
3. **Import**

### 5.3 Configurer le workflow

1. Ouvrir le workflow
2. Pour chaque node Airtable :
   - Sélectionner votre credential
   - Sélectionner votre base
   - Sélectionner la table "Posts"
3. Configurer les autres credentials (LinkedIn, Email)

---

## Étape 6 : Tester (2 min)

### 6.1 Préparer un post de test

Dans Airtable :
1. Ouvrir un post
2. Vérifier que les brouillons sont présents
3. Changer **Statut** à **"Validé"**
4. Changer **Date Publication** à **aujourd'hui**

### 6.2 Tester le workflow

Dans n8n :
1. Cliquer sur **"Execute Workflow"**
2. Observer l'exécution
3. Vérifier que le post est publié sur LinkedIn
4. Vérifier que le statut est "Publié" dans Airtable

---

## Étape 7 : Activer (1 min)

Dans n8n :
1. Toggle **"Active"** en haut à droite
2. Le workflow s'exécutera automatiquement à 8h30 chaque jour

---

## ✅ Checklist Complète

- [ ] Compte Airtable créé
- [ ] Base "Calendrier Editorial IA" créée
- [ ] Colonnes configurées
- [ ] API Key obtenue
- [ ] Base ID obtenu
- [ ] Variables d'environnement configurées
- [ ] Base peuplée avec `populate_airtable.py`
- [ ] Contenu généré avec `generer_post_airtable.py`
- [ ] Credential Airtable configurée dans n8n
- [ ] Workflow importé dans n8n
- [ ] Test réussi
- [ ] Workflow activé

---

## 🎯 Utilisation Quotidienne

### Ajouter un nouveau post

**Dans Airtable :**
1. Cliquer sur **"+"** en bas
2. Remplir les champs
3. Statut : "À générer"
4. Save

### Générer le contenu

```bash
python3 generer_post_airtable.py
```

### Valider un post

**Dans Airtable :**
1. Ouvrir le post
2. Lire les brouillons
3. Ajuster si nécessaire
4. Statut → "Validé"

### Vérifier les publications

**Dans Airtable :**
- Vue "Publiés" (filter: Statut = "Publié")
- Voir les URLs des posts

---

## 🆘 Dépannage

### "API Key invalid"
- Vérifier que vous avez copié la clé complète
- Régénérer une nouvelle clé si nécessaire

### "Base not found"
- Vérifier le Base ID dans l'URL
- S'assurer que la base est bien accessible

### "Table not found"
- Vérifier que la table s'appelle exactement "Posts"
- Respecter la casse

### "No records found"
- Vérifier la formule de filtrage dans n8n
- S'assurer qu'il y a des posts avec statut "Validé" et date = aujourd'hui

---

## 📚 Ressources

- **Guide complet :** `guide_airtable_n8n.md`
- **Workflow n8n :** `workflow_airtable_publication.json`
- **Scripts Python :**
  - `populate_airtable.py` - Peupler la base
  - `generer_post_airtable.py` - Générer le contenu

---

## 🎉 C'est Prêt !

Votre système Airtable + n8n est opérationnel !

**Avantages :**
- ✅ Interface plus belle que Google Sheets
- ✅ Configuration n8n plus simple
- ✅ Vues multiples (calendrier, kanban)
- ✅ Application mobile excellente
- ✅ 100% gratuit

Bon automatisation ! 🚀
