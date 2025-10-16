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

if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
    print("❌ Erreur : Variables d'environnement Airtable manquantes")
    print("   Exécutez :")
    print("   export AIRTABLE_API_KEY='votre_clé'")
    print("   export AIRTABLE_BASE_ID='votre_base_id'")
    exit(1)

# Initialiser les APIs
airtable_api = Api(AIRTABLE_API_KEY)
table = airtable_api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
openai_client = OpenAI()

# Prompts
PROMPTS = {
    "news": {
        "linkedin": """Tu es un expert en IA et automatisation qui crée du contenu engageant sur LinkedIn.

Crée un post LinkedIn sur cette actualité IA : {sujet}

Le post doit :
- Commencer par un hook accrocheur
- Expliquer l'actualité de manière claire et accessible
- Donner ton analyse ou ton point de vue
- Terminer par une question pour engager la discussion
- Utiliser des sauts de ligne pour l'aération
- Maximum 1300 caractères
- Pas d'emojis excessifs (2-3 maximum)

Format professionnel mais accessible.""",
        
        "twitter": """Tu es un expert en IA qui crée du contenu viral sur Twitter/X.

Crée un tweet sur cette actualité IA : {sujet}

Le tweet doit :
- Être percutant et direct
- Donner l'info clé en premier
- Maximum 280 caractères
- 1-2 emojis pertinents
- Pas de hashtags (seront ajoutés séparément)

Style : informatif mais engageant."""
    },
    
    "outils": {
        "linkedin": """Tu es un expert en outils IA qui aide les professionnels à être plus productifs.

Crée un post LinkedIn présentant cet outil IA : {outil}

Le post doit :
- Commencer par le problème que l'outil résout
- Présenter l'outil et ses fonctionnalités clés
- Donner un cas d'usage concret
- Terminer par un call-to-action (tester l'outil)
- Utiliser des sauts de ligne pour l'aération
- Maximum 1300 caractères
- 2-3 emojis maximum

Format : tutoriel rapide et actionnable.""",
        
        "twitter": """Tu es un expert en outils IA qui partage des découvertes sur Twitter/X.

Crée un tweet présentant cet outil IA : {outil}

Le tweet doit :
- Présenter l'outil en une phrase
- Donner 1-2 fonctionnalités clés
- Maximum 280 caractères
- 1-2 emojis
- Pas de hashtags

Style : découverte excitante."""
    },
    
    "saas_story": {
        "linkedin": """Tu es un entrepreneur qui partage son parcours de création d'un SaaS.

Crée un post LinkedIn sur ce sujet : {titre}
Description : {description}

Le post doit :
- Raconter une histoire personnelle et authentique
- Partager une leçon apprise ou un insight
- Être vulnérable et honnête
- Inspirer d'autres entrepreneurs
- Utiliser des sauts de ligne pour l'aération
- Maximum 1300 caractères
- Pas d'emojis ou très peu (1-2)

Format : storytelling authentique.""",
        
        "twitter": """Tu es un entrepreneur qui partage son parcours sur Twitter/X.

Crée un tweet sur ce sujet : {titre}
Description : {description}

Le tweet doit :
- Partager une leçon clé ou un insight
- Être authentique et direct
- Maximum 280 caractères
- 0-1 emoji
- Pas de hashtags

Style : leçon apprise, authentique."""
    }
}

def generer_post(type_contenu, plateforme, **kwargs):
    """Générer un post avec OpenAI"""
    type_key = type_contenu.lower().replace(" ", "_")
    prompt_template = PROMPTS[type_key][plateforme]
    prompt = prompt_template.format(**kwargs)
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4-mini",
            messages=[
                {"role": "system", "content": "Tu es un expert en création de contenu pour les réseaux sociaux."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"  ❌ Erreur OpenAI : {e}")
        return None

def generer_posts_airtable():
    """Générer le contenu pour tous les posts 'À générer'"""
    
    # Récupérer les posts à générer
    formula = "{Statut} = 'À générer'"
    records = table.all(formula=formula)
    
    if not records:
        print("ℹ️  Aucun post à générer (statut 'À générer')")
        return
    
    print(f"🚀 {len(records)} posts à générer\n")
    
    for i, record in enumerate(records, 1):
        fields = record['fields']
        record_id = record['id']
        
        titre_post = fields.get('Sujet/Outil') or fields.get('Titre', 'Sans titre')
        print(f"[{i}/{len(records)}] {fields['Type']} - {titre_post}")
        
        # Déterminer le type et générer
        type_contenu = fields['Type']
        
        linkedin = None
        twitter = None
        
        try:
            if type_contenu == "News":
                linkedin = generer_post("news", "linkedin", sujet=fields.get('Sujet/Outil', ''))
                twitter = generer_post("news", "twitter", sujet=fields.get('Sujet/Outil', ''))
            
            elif type_contenu == "Outils":
                linkedin = generer_post("outils", "linkedin", outil=fields.get('Sujet/Outil', ''))
                twitter = generer_post("outils", "twitter", outil=fields.get('Sujet/Outil', ''))
            
            elif type_contenu == "SaaS Story":
                linkedin = generer_post("saas_story", "linkedin", 
                                       titre=fields.get('Titre', ''), 
                                       description=fields.get('Description', ''))
                twitter = generer_post("saas_story", "twitter", 
                                      titre=fields.get('Titre', ''), 
                                      description=fields.get('Description', ''))
            
            # Mettre à jour Airtable si génération réussie
            if linkedin and twitter:
                table.update(record_id, {
                    "Brouillon LinkedIn": linkedin,
                    "Brouillon Twitter": twitter,
                    "Statut": "À valider"
                })
                print(f"  ✅ Généré et mis à jour\n")
            else:
                print(f"  ⚠️  Génération partielle, non sauvegardé\n")
                
        except Exception as e:
            print(f"  ❌ Erreur : {e}\n")
            continue
    
    print(f"✅ Génération terminée !")
    print(f"📊 Vérifiez vos posts dans Airtable (statut 'À valider')")

if __name__ == "__main__":
    generer_posts_airtable()

