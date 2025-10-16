#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour peupler Airtable depuis le plan structuré
"""

from pyairtable import Api
import json
import os
from datetime import datetime, timedelta

# Configuration
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN") or os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = "Posts"

if not AIRTABLE_TOKEN or not AIRTABLE_BASE_ID:
    print("❌ Erreur : Variables d'environnement manquantes")
    print("   Exécutez :")
    print("   export AIRTABLE_TOKEN='votre_token'  # Personal Access Token (recommandé)")
    print("   ou")
    print("   export AIRTABLE_API_KEY='votre_clé'  # API Key (ancien)")
    print("   export AIRTABLE_BASE_ID='votre_base_id'")
    print("")
    print("ℹ️  Airtable utilise maintenant des Personal Access Tokens.")
    print("   Voir AIRTABLE_TOKEN_SETUP.md pour plus d'infos.")
    exit(1)

# Initialiser l'API
api = Api(AIRTABLE_TOKEN)
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
print(f"📅 Date de début : {date_debut.strftime('%d/%m/%Y')}\n")

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
    
    print(f"Semaine {semaine + 1} ({date_semaine.strftime('%d/%m/%Y')}):")
    
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
    
    print()

print(f"✅ {records_created} posts créés dans Airtable !")
print(f"📊 Répartition :")
print(f"   - News : {len(plan['news'])}")
print(f"   - Outils : {len(plan['outils'])}")
print(f"   - SaaS Story : {len(plan['saas_story'])}")
print(f"\n🎉 Vous pouvez maintenant consulter votre base Airtable !")
