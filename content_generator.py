#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Générateur de Contenu pour LinkedIn et X (Twitter)
Utilise l'API OpenAI pour générer des posts à partir d'un plan de contenu
"""

import os
import json
from datetime import datetime, timedelta
from openai import OpenAI

# Configuration
client = OpenAI()  # API key déjà configurée dans les variables d'environnement

# Prompts personnalisés par type de contenu
PROMPTS = {
    "news": {
        "linkedin": """Tu es un expert en IA et en création de contenu LinkedIn. 
        
Crée un post LinkedIn engageant sur le sujet suivant : "{sujet}"

Le post doit :
- Commencer par un hook accrocheur (question, statistique surprenante, ou affirmation forte)
- Expliquer pourquoi cette actualité est importante
- Donner 2-3 insights concrets ou implications pratiques
- Se terminer par une question pour engager la conversation
- Utiliser des sauts de ligne pour l'aération
- Faire entre 150 et 250 mots
- Avoir un ton professionnel mais accessible
- Ne pas utiliser d'emojis excessifs (maximum 2-3)

Format : Texte brut, sans titre, prêt à être copié-collé.""",
        
        "twitter": """Tu es un expert en IA et en création de contenu pour X (Twitter).

Crée un tweet percutant sur le sujet suivant : "{sujet}"

Le tweet doit :
- Être concis et impactant (maximum 280 caractères)
- Commencer par un hook fort
- Donner une information clé ou un insight
- Utiliser 1-2 emojis pertinents
- Inclure 2-3 hashtags pertinents (#IA #AI #Tech)

Format : Texte brut, prêt à être copié-collé."""
    },
    
    "outils": {
        "linkedin": """Tu es un expert en outils IA et en création de contenu LinkedIn.

Crée un post LinkedIn présentant l'outil IA suivant : "{outil}"

Le post doit :
- Commencer par un hook qui présente le problème que l'outil résout
- Présenter l'outil et sa proposition de valeur unique
- Lister 3-4 fonctionnalités clés avec des exemples concrets d'usage
- Mentionner le type d'utilisateurs qui en bénéficieraient le plus
- Inclure un call-to-action subtil (ex: "Avez-vous déjà testé ?")
- Faire entre 150 et 250 mots
- Avoir un ton enthousiaste mais professionnel
- Utiliser des sauts de ligne et des bullet points si pertinent

Format : Texte brut, sans titre, prêt à être copié-collé.""",
        
        "twitter": """Tu es un expert en outils IA et en création de contenu pour X (Twitter).

Crée un tweet présentant l'outil IA suivant : "{outil}"

Le tweet doit :
- Présenter l'outil et son bénéfice principal en une phrase
- Mentionner 1-2 cas d'usage concrets
- Être concis (maximum 280 caractères)
- Utiliser 1-2 emojis pertinents
- Inclure 2-3 hashtags (#IA #Outils #Productivité)

Format : Texte brut, prêt à être copié-collé."""
    },
    
    "saas_story": {
        "linkedin": """Tu es un entrepreneur qui partage son parcours de création d'un SaaS sur LinkedIn.

Crée un post LinkedIn authentique sur le sujet suivant :
Titre : "{titre}"
Angle : {description}

Le post doit :
- Commencer par une accroche personnelle et authentique
- Raconter une expérience concrète avec des détails spécifiques
- Partager 2-3 apprentissages ou insights clés
- Être vulnérable et honnête (partager les difficultés aussi)
- Se terminer par une question pour créer de l'engagement
- Faire entre 150 et 250 mots
- Avoir un ton personnel, humble et inspirant
- Utiliser "je" et "mon" pour créer de la proximité

Format : Texte brut, sans titre, prêt à être copié-collé.""",
        
        "twitter": """Tu es un entrepreneur qui partage son parcours de création d'un SaaS sur X (Twitter).

Crée un tweet authentique sur le sujet suivant :
Titre : "{titre}"
Angle : {description}

Le tweet doit :
- Partager un insight ou apprentissage clé de manière concise
- Être personnel et authentique
- Utiliser un ton direct et humble
- Faire maximum 280 caractères
- Utiliser 1 emoji pertinent
- Inclure 2-3 hashtags (#SaaS #Entrepreneuriat #BuildInPublic)

Format : Texte brut, prêt à être copié-collé."""
    }
}


def generer_post(type_contenu, plateforme, **kwargs):
    """
    Génère un post pour une plateforme donnée
    
    Args:
        type_contenu: "news", "outils", ou "saas_story"
        plateforme: "linkedin" ou "twitter"
        **kwargs: Arguments spécifiques au type de contenu
    
    Returns:
        str: Le texte du post généré
    """
    
    # Récupérer le prompt template
    prompt_template = PROMPTS[type_contenu][plateforme]
    
    # Formater le prompt avec les arguments
    prompt = prompt_template.format(**kwargs)
    
    # Appeler l'API OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",  # Modèle optimisé coût/performance
            messages=[
                {"role": "system", "content": "Tu es un expert en création de contenu pour les réseaux sociaux, spécialisé dans l'IA et l'entrepreneuriat tech."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,  # Un peu de créativité
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"❌ Erreur lors de la génération : {e}")
        return None


def generer_contenu_depuis_plan(plan_path="/home/ubuntu/plan_structure.json", output_path="/home/ubuntu/contenu_genere.json"):
    """
    Génère du contenu pour tous les items du plan
    
    Args:
        plan_path: Chemin vers le fichier JSON du plan structuré
        output_path: Chemin vers le fichier JSON de sortie
    """
    
    # Charger le plan
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)
    
    contenu_genere = []
    
    print("🚀 Démarrage de la génération de contenu...\n")
    
    # Générer pour les News
    print("📰 Génération des posts News...")
    for idx, item in enumerate(plan['news'], 1):
        print(f"  [{idx}/{len(plan['news'])}] {item['sujet']}")
        
        linkedin = generer_post("news", "linkedin", sujet=item['sujet'])
        twitter = generer_post("news", "twitter", sujet=item['sujet'])
        
        contenu_genere.append({
            "type": "News",
            "jour": "Lundi",
            "sujet": item['sujet'],
            "linkedin": linkedin,
            "twitter": twitter,
            "statut": "À valider"
        })
    
    # Générer pour les Outils
    print("\n🛠️  Génération des posts Outils...")
    for idx, item in enumerate(plan['outils'][:5], 1):  # Limiter à 5 pour le test
        print(f"  [{idx}/5] {item['outil']}")
        
        linkedin = generer_post("outils", "linkedin", outil=item['outil'])
        twitter = generer_post("outils", "twitter", outil=item['outil'])
        
        contenu_genere.append({
            "type": "Outils",
            "jour": "Mardi",
            "outil": item['outil'],
            "linkedin": linkedin,
            "twitter": twitter,
            "statut": "À valider"
        })
    
    # Générer pour les SaaS Stories
    print("\n📖 Génération des posts SaaS Story...")
    for idx, item in enumerate(plan['saas_story'][:5], 1):  # Limiter à 5 pour le test
        print(f"  [{idx}/5] {item['titre']}")
        
        linkedin = generer_post("saas_story", "linkedin", 
                               titre=item['titre'], 
                               description=item['description'])
        twitter = generer_post("saas_story", "twitter", 
                              titre=item['titre'], 
                              description=item['description'])
        
        contenu_genere.append({
            "type": "SaaS Story",
            "jour": "Jeudi",
            "theme": item['theme'],
            "titre": item['titre'],
            "description": item['description'],
            "linkedin": linkedin,
            "twitter": twitter,
            "statut": "À valider"
        })
    
    # Sauvegarder le contenu généré
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(contenu_genere, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Génération terminée ! {len(contenu_genere)} posts créés.")
    print(f"📁 Contenu sauvegardé dans : {output_path}")
    
    return contenu_genere


def generer_exemple_unique(type_contenu="outils", outil="ChatGPT"):
    """
    Génère un exemple unique pour tester
    """
    print(f"🧪 Test de génération pour {outil}...\n")
    
    print("=" * 60)
    print("LINKEDIN")
    print("=" * 60)
    linkedin = generer_post(type_contenu, "linkedin", outil=outil)
    print(linkedin)
    
    print("\n" + "=" * 60)
    print("TWITTER / X")
    print("=" * 60)
    twitter = generer_post(type_contenu, "twitter", outil=outil)
    print(twitter)
    
    return {"linkedin": linkedin, "twitter": twitter}


if __name__ == "__main__":
    # Test avec un exemple unique
    print("🎯 Mode Test : Génération d'un exemple\n")
    generer_exemple_unique("outils", "ChatGPT")
    
    # Pour générer tout le contenu, décommenter la ligne suivante :
    # generer_contenu_depuis_plan()
