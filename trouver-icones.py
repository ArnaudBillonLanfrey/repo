#!/usr/bin/env python3
"""
Script d'automatisation : recherche les icones officielles pour tous les materiaux
listes dans icones-a-fournir.csv, via l'API publique communautaire XIVAPI.

PREREQUIS :
    pip install requests

UTILISATION :
    python trouver-icones.py

Produit un fichier icon-map-auto.json pret a remplacer/completer icons/icon-map.json.

IMPORTANT :
- Ce script cherche uniquement l'ICONE (pas le lien Lodestone pour l'info-bulle,
  les systemes d'ID sont differents et il n'y a pas de correspondance publique
  simple entre les deux). Pour l'info-bulle au survol, il faudra toujours ajouter
  le lien a la main pour les objets qui t'interessent le plus.
- XIVAPI est un service communautaire gratuit, pas garanti a 100%. Si le script
  echoue completement (erreur de connexion dès le premier essai), l'API est
  peut-etre indisponible -- dis-le moi, on cherchera une alternative.
- Teste d'abord avec un petit nombre d'objets (voir LIMITE ci-dessous) avant de
  lancer sur les 362, pour verifier que les resultats sont bons.
"""

import csv
import json
import time
import sys

try:
    import requests
except ImportError:
    print("Le module 'requests' n'est pas installe. Lance d'abord : pip install requests")
    sys.exit(1)

INPUT_CSV = "icones-a-fournir.csv"
OUTPUT_JSON = "icon-map-auto.json"
XIVAPI_SEARCH = "https://xivapi.com/search"

# Mets un nombre ici (ex: 10) pour tester sur un echantillon avant de lancer sur tout.
# Mets None pour traiter la liste entiere.
LIMITE = 10


def search_icon(name_en, name_fr):
    """Cherche un objet sur XIVAPI, d'abord par son nom anglais (plus fiable),
    puis par son nom francais si rien n'est trouve."""
    for name, lang in [(name_en, "en"), (name_fr, "fr")]:
        if not name:
            continue
        try:
            r = requests.get(
                XIVAPI_SEARCH,
                params={"string": name, "indexes": "Item", "language": lang},
                timeout=10,
            )
            r.raise_for_status()
            data = r.json()
            results = data.get("Results", [])
            if results:
                icon_path = results[0].get("Icon")
                if icon_path:
                    return f"https://xivapi.com{icon_path}"
        except Exception as e:
            print(f"    (erreur recherche '{name}' [{lang}] : {e})")
    return None


def main():
    with open(INPUT_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if LIMITE:
        rows = rows[:LIMITE]
        print(f"MODE TEST : traitement des {LIMITE} premiers objets seulement.")
        print("(change LIMITE = None dans le script pour traiter la liste entiere)\n")

    print(f"{len(rows)} materiaux a chercher...\n")

    out = {}
    found = 0
    for i, row in enumerate(rows):
        slug = row["Nom de fichier attendu"].rsplit(".png", 1)[0]
        name_fr = row.get("Nom du materiau (FR)", "")
        name_en = row.get("Nom EN (pour recherche)", "")

        print(f"[{i+1}/{len(rows)}] {name_fr}", end=" -> ")
        icon = search_icon(name_en, name_fr)

        if icon:
            out[slug] = {"icon": icon}
            found += 1
            print("trouve")
        else:
            print("NON TROUVE")

        time.sleep(0.3)  # politesse envers l'API publique

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"\n{found}/{len(rows)} icones trouvees.")
    print(f"Resultat ecrit dans {OUTPUT_JSON}")
    print("\nVerifie le resultat, puis fusionne-le avec icons/icon-map.json")
    print("(garde les entrees existantes qui ont deja un 'link', ne les ecrase pas).")


if __name__ == "__main__":
    main()
