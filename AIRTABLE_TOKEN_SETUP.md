# Configuration du Personal Access Token Airtable

## 🔐 Nouveau Système d'Authentification

Airtable utilise maintenant des **Personal Access Tokens** (jetons d'accès personnels) au lieu des anciennes API Keys.

**Avantages :**
- ✅ Plus sécurisé
- ✅ Permissions granulaires (scopes)
- ✅ Accès limité aux bases spécifiques
- ✅ Révocable individuellement

---

## 📋 Étapes de Configuration

### 1. Créer un Personal Access Token

1. **Aller sur https://airtable.com/create/tokens**
2. **Cliquer sur "Create new token"**
3. **Nommer le token :** "N8N" ou "Automatisation Publication"

### 2. Configurer les Scopes (Portées)

**Scopes nécessaires pour notre système :**

#### ✅ Record data and comments

- **`data.records:read`** ✅ **REQUIS**
  - Permet de lire les entrées (posts)
  - Nécessaire pour récupérer les posts à publier

- **`data.records:write`** ✅ **REQUIS**
  - Permet de créer, modifier et supprimer des entrées
  - Nécessaire pour mettre à jour le statut après publication

- **`data.recordComments:read`** ❌ Optionnel
  - Permet de lire les commentaires
  - Non nécessaire pour notre cas

- **`data.recordComments:write`** ❌ Optionnel
  - Permet de créer/modifier des commentaires
  - Non nécessaire pour notre cas

#### ✅ Base schema

- **`schema.bases:read`** ✅ **RECOMMANDÉ**
  - Permet de lire la structure de la base
  - Utile pour n8n pour lister les tables et champs

- **`schema.bases:write`** ❌ Non nécessaire
  - Permet de modifier la structure
  - Non nécessaire (structure déjà définie)

#### ❌ Advanced developer features

- **`webhook:manage`** ❌ Non nécessaire
  - Pour les webhooks
  - Non utilisé dans notre cas

- **`block:manage`** ❌ Non nécessaire
  - Pour les extensions personnalisées
  - Non utilisé dans notre cas

#### ❌ User metadata

- **`user.email:read`** ❌ Non nécessaire
  - Afficher l'email de l'utilisateur
  - Non nécessaire pour notre cas

---

## ✅ Configuration Recommandée

### Scopes Minimaux

Pour notre système de publication automatique, sélectionnez **uniquement** :

```
✅ data.records:read
✅ data.records:write
✅ schema.bases:read (recommandé)
```

### 3. Configurer l'Accès aux Bases

**Important :** Le token doit avoir accès à votre base !

1. **Dans la section "Accès"**
2. **Cliquer sur "Ajouter une base"**
3. **Sélectionner votre base "Calendrier Editorial IA"**

**Ou :**
- **"Ajouter toutes les ressources"** si vous voulez accès à toutes vos bases

### 4. Créer le Token

1. **Cliquer sur "Create token"**
2. **Copier le token** (commence par `pat...`)
3. **⚠️ IMPORTANT :** Sauvegardez-le immédiatement, il ne sera plus affiché !

---

## 🔧 Utilisation du Token

### Dans les Scripts Python

**Ancienne méthode (API Key) :**
```python
from pyairtable import Api

api = Api("keyXXXXXXXXXXXXXX")  # ❌ Ancien
```

**Nouvelle méthode (Personal Access Token) :**
```python
from pyairtable import Api

api = Api("patXXXXXXXXXXXXXX")  # ✅ Nouveau
```

**C'est exactement la même chose !** Le code reste identique, seul le format du token change.

### Dans n8n

**Configuration du credential :**

1. **n8n → Settings → Credentials**
2. **Add Credential → Airtable Personal Access Token**
   - Si vous ne voyez pas cette option, utilisez "Airtable API" (compatible)
3. **Coller votre token** (commence par `pat...`)
4. **Save**

**Note :** n8n accepte les deux formats (ancienne API Key et nouveau Personal Access Token).

---

## 🔄 Migration depuis API Key

### Si vous avez déjà une API Key

**Pas de panique !** Les anciennes API Keys fonctionnent encore, mais Airtable recommande de migrer.

**Pour migrer :**

1. **Créer un Personal Access Token** (voir ci-dessus)
2. **Mettre à jour vos variables d'environnement :**

```bash
# Ancien
export AIRTABLE_API_KEY="keyXXXXXXXXXXXXXX"

# Nouveau
export AIRTABLE_TOKEN="patXXXXXXXXXXXXXX"
```

3. **Mettre à jour vos scripts** (si vous utilisez `AIRTABLE_API_KEY`)

**Ou simplement :**
```bash
# Garder le même nom de variable
export AIRTABLE_API_KEY="patXXXXXXXXXXXXXX"
```

Les scripts fonctionneront sans modification !

---

## 📝 Variables d'Environnement

### Configuration Recommandée

```bash
# Personal Access Token Airtable
export AIRTABLE_TOKEN="patXXXXXXXXXXXXXX"

# Base ID (inchangé)
export AIRTABLE_BASE_ID="appXXXXXXXXXXXXXX"

# OpenAI API Key
export OPENAI_API_KEY="sk-XXXXXXXXXXXXXXXX"
```

### Fichier .env

Créer un fichier `.env` :

```bash
# Airtable
AIRTABLE_TOKEN=patXXXXXXXXXXXXXX
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX

# OpenAI
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXX
```

**Charger les variables :**
```bash
# Bash
source .env

# Ou avec python-dotenv
pip3 install python-dotenv
```

---

## 🔐 Sécurité

### Bonnes Pratiques

1. **Ne jamais commiter le token dans Git**
   - Ajouter `.env` dans `.gitignore`
   - Utiliser des variables d'environnement

2. **Utiliser des scopes minimaux**
   - Seulement `read` et `write` pour les records
   - Pas de `webhook:manage` ou autres si non nécessaire

3. **Limiter l'accès aux bases**
   - Seulement la base "Calendrier Editorial IA"
   - Pas "Toutes les ressources" sauf si nécessaire

4. **Révoquer les tokens inutilisés**
   - Aller sur https://airtable.com/create/tokens
   - Supprimer les anciens tokens

5. **Utiliser des tokens différents par environnement**
   - Token "Dev" pour développement
   - Token "Prod" pour production
   - Facilite la révocation en cas de problème

---

## 🧪 Tester le Token

### Test avec curl

```bash
curl "https://api.airtable.com/v0/meta/bases" \
  -H "Authorization: Bearer patXXXXXXXXXXXXXX"
```

**Résultat attendu :**
```json
{
  "bases": [
    {
      "id": "appXXXXXXXXXXXXXX",
      "name": "Calendrier Editorial IA",
      "permissionLevel": "create"
    }
  ]
}
```

### Test avec Python

```python
from pyairtable import Api

token = "patXXXXXXXXXXXXXX"
base_id = "appXXXXXXXXXXXXXX"

api = Api(token)
table = api.table(base_id, "Posts")

# Lire les 3 premiers posts
records = table.all(max_records=3)

for record in records:
    print(f"ID: {record['id']}")
    print(f"Type: {record['fields'].get('Type')}")
    print()
```

**Si ça fonctionne :** ✅ Token configuré correctement !

---

## ❓ FAQ

### Q: Mon ancien API Key fonctionne-t-il encore ?

**R:** Oui ! Les anciennes API Keys fonctionnent toujours. Mais Airtable recommande de migrer vers les Personal Access Tokens pour plus de sécurité.

### Q: Quelle est la différence entre API Key et Personal Access Token ?

**R:**

| Aspect | API Key | Personal Access Token |
|--------|---------|----------------------|
| Format | `keyXXXXXXXXXXXXXX` | `patXXXXXXXXXXXXXX` |
| Permissions | Toutes les bases | Granulaire (scopes) |
| Accès | Toutes les bases | Bases spécifiques |
| Révocation | Toutes les apps | Token individuel |
| Sécurité | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### Q: Dois-je modifier mes scripts ?

**R:** Non ! Si vous utilisez `pyairtable`, il suffit de remplacer le token :

```python
# Avant
api = Api("keyXXXXXXXXXXXXXX")

# Après
api = Api("patXXXXXXXXXXXXXX")
```

Le reste du code reste identique.

### Q: Le token expire-t-il ?

**R:** Non, les Personal Access Tokens n'expirent pas automatiquement. Vous devez les révoquer manuellement si nécessaire.

### Q: Puis-je avoir plusieurs tokens ?

**R:** Oui ! Vous pouvez créer autant de tokens que nécessaire. Recommandé :
- 1 token pour dev
- 1 token pour prod
- 1 token par application

---

## 🎯 Récapitulatif

### Checklist de Configuration

- [ ] Aller sur https://airtable.com/create/tokens
- [ ] Créer un nouveau token nommé "N8N"
- [ ] Sélectionner les scopes :
  - [ ] `data.records:read`
  - [ ] `data.records:write`
  - [ ] `schema.bases:read`
- [ ] Ajouter l'accès à la base "Calendrier Editorial IA"
- [ ] Créer le token
- [ ] Copier le token (commence par `pat...`)
- [ ] Configurer les variables d'environnement
- [ ] Tester avec le script Python
- [ ] Configurer dans n8n

---

## 🚀 Prochaines Étapes

Une fois le token configuré :

1. **Tester les scripts Python :**
```bash
export AIRTABLE_TOKEN="patXXXXXXXXXXXXXX"
export AIRTABLE_BASE_ID="appXXXXXXXXXXXXXX"
python3 populate_airtable.py
```

2. **Configurer n8n :**
   - Credentials → Airtable Personal Access Token
   - Coller le token
   - Tester le workflow

3. **Commencer à publier !** 🎉

---

## 📚 Ressources

- [Documentation Airtable - Personal Access Tokens](https://airtable.com/developers/web/guides/personal-access-tokens)
- [Migration Guide](https://support.airtable.com/docs/creating-personal-access-tokens)
- [API Reference](https://airtable.com/developers/web/api/introduction)

Bon automatisation ! 🚀
