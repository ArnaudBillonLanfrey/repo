# Ajouter les icônes d'objets

## Le système en bref

L'app affiche toujours une icône générique (par catégorie : devise, craft, drop, quête,
récolte, spécial) à côté de chaque matériau. Tu peux la remplacer par la vraie icône du
jeu via `icons/icon-map.json`, avec deux méthodes possibles — tu peux mélanger les deux :

### Option A (recommandée) — Icône + info-bulle officielles Lodestone, aucun fichier à héberger

Chaque page d'objet sur le Lodestone (`fr.finalfantasyxiv.com/lodestone/.../item/...`)
permet de récupérer deux choses officielles et gratuites, hébergées par Square Enix :

1. **L'icône** : vue source de la page Lodestone de l'objet → cherche `og:image` → tu
   obtiens une URL du type :
   ```
   https://lds-img.finalfantasyxiv.com/itemicon/6b/6b4d2cd7fb7056e8b19003935875f548a748d110.png
   ```
2. **L'info-bulle officielle au survol** (Fan Kit Tooltip) : l'URL de la page Lodestone
   elle-même, ex. `https://fr.finalfantasyxiv.com/lodestone/playguide/db/item/d55d1338b13`

Ajoute les deux dans `icons/icon-map.json` sous forme d'objet :
```json
{
  "marteau-a-panne-croisee-superstellaire": {
    "icon": "https://lds-img.finalfantasyxiv.com/itemicon/6b/6b4d2cd7fb7056e8b19003935875f548a748d110.png",
    "link": "https://fr.finalfantasyxiv.com/lodestone/playguide/db/item/d55d1338b13"
  }
}
```
Tu peux aussi ne renseigner que l'icône (chaîne simple, comme avant) si tu n'as pas
encore le lien de la page :
```json
{ "nom-du-materiau": "https://lds-img.finalfantasyxiv.com/itemicon/.../....png" }
```

Rien d'autre à faire — aucun fichier à uploader, tout est servi directement par Square
Enix (icône + info-bulle officielle identique à celle du Lodestone, grâce au script
Fan Kit Tooltip déjà intégré dans l'app).

**Astuce** : si tu me donnes le lien Lodestone d'un objet, je peux en extraire l'icône et
compléter la ligne pour toi — ma recherche automatique ne retrouve pas toujours le bon
lien, mais un lien que tu me donnes directement fonctionne à chaque fois.

### Option B — Fichier local numéroté (si tu as extrait les icônes du jeu toi-même)

1. Dépose le dossier d'icônes numérotées dans `icons/` (aucun renommage)
2. Dans `icons/icon-map.json`, indique juste le numéro :
   ```json
   {
     "pioche-superstellaire": "023191"
   }
   ```

### Option C — Renommage direct

Dépose un fichier nommé comme la colonne **Nom de fichier attendu** du CSV (ex.
`pioche-superstellaire.png`) dans `icons/`. Utilisé automatiquement, sans toucher à
`icon-map.json`.

## Où déposer les fichiers

```
ton-depot/
├── index.html
└── icons/
    ├── icon-map.json                      ← correspondances (Options A et B)
    ├── 023191.png                         ← icônes locales numérotées (Option B)
    └── pioche-superstellaire.png          ← icône renommée directement (Option C)
```

## Quel nom pour quel objet ?

Tout est dans `icones-a-fournir.csv` :
- **Nom de fichier attendu** → la clé à utiliser dans `icon-map.json` (sans le `.png`)
- **Nom du matériau** → à quoi ça correspond dans le jeu, pour le chercher sur le Lodestone
- **Catégorie** → l'icône générique affichée en attendant
- **Séries concernées** → où ce matériau apparaît

362 matériaux uniques en tout (mis à jour après le découpage Artisanat/Récolte et l'ajout
des collectionnables d'artisans + Pêcheur), triés par ordre alphabétique.

## Limite à connaître

Le chargement de `icon-map.json` se fait via `fetch()`, qui ne fonctionne qu'en http(s) —
parfait sur **GitHub Pages**, mais pas si tu ouvres `index.html` en double-cliquant depuis
ton ordinateur (`file://`). Dans ce cas, seule l'Option C (renommage direct) fonctionnera
en local ; les Options A et B fonctionneront normalement une fois déployé.
