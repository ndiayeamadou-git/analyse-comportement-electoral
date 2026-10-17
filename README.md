# Analyse statistique et spatiale des comportements électoraux à l'échelle des bureaux de vote

Présidentielle française 2022, premier tour. Projet réalisé lors d'un stage au sein de l'UFR ASSP de l'Université Lumière Lyon 2 (Master 1 MIASHS, année 2025-2026).

**Question de recherche** : peut-on identifier des profils électoraux homogènes à l'échelle des bureaux de vote et étudier leur lien avec les caractéristiques socio-économiques des territoires ?

Les bureaux de vote n'ont pas de contours géographiques officiels, et les données socio-économiques de l'INSEE sont publiées par IRIS, un découpage qui ne coïncide pas avec celui des bureaux. Ce projet reconstruit les zones d'influence des bureaux, croise les trois sources de données, puis analyse la base obtenue.

## Résultats principaux

- Une base à l'échelle du bureau de vote (France métropolitaine et DOM, 68 806 polygones, 101 départements) qui croise résultats électoraux, géographie reconstruite et variables socio-économiques.
- Cinq profils électoraux territorialisés, obtenus par K-Means sur une projection UMAP.
- Une régression locale pondérée (distance de Mahalanobis) qui améliore les prédictions de la régression linéaire globale pour 10 candidats sur 12, avec des gains de MAE allant jusqu'à 4,1 %.

## Méthode

1. **Polygones de Voronoï** : pour chaque département, les adresses électorales géolocalisées du REU sont transformées en polygones de Voronoï, puis découpées selon les limites communales de l'IGN (ADMIN EXPRESS).
2. **Agrégation spatiale** : chaque IRIS est redistribué entre les bureaux qu'il intersecte, au prorata de la surface d'intersection, pondérée par la population active. Les variables socio-économiques d'un bureau sont la moyenne pondérée de celles des IRIS qui le recouvrent.
3. **Analyse exploratoire** : résultats nationaux, participation, corrélations entre candidats.
4. **Clustering** : K-Means sur les 12 scores, avec ou sans ACP, puis sur une projection UMAP (`n_neighbors = 30`, `min_dist = 0,1`).
5. **Régression** : une régression OLS par candidat (échantillon d'entraînement de 80 %, évaluation sur les 20 % restants), comparée à une régression locale pondérée (WLS). Pour chaque bureau cible, les bureaux voisins sont pondérés par un noyau gaussien de la distance de Mahalanobis entre profils socio-économiques, avec une bande passante σ fixée à la médiane des distances (3,363).

## Données

| Source | Contenu |
|---|---|
| Ministère de l'Intérieur (data.gouv.fr) | Résultats du premier tour par bureau de vote (69 682 lignes) |
| Répertoire Électoral Unique (REU) | Environ 15,9 millions d'adresses géocodées associées à un bureau |
| INSEE, base Activité-Résidents 2022 | Chômage, diplômes, modes de transport par IRIS |
| INSEE, Filosofi 2021 | Revenus et niveaux de vie par IRIS et par commune |
| IGN, ADMIN EXPRESS | Limites communales |

Les données ne sont pas versionnées dans ce dépôt (volume). Voir [`data/README.md`](data/README.md) pour les télécharger et les placer.

## Structure du dépôt

```
.
├── notebooks/
│   ├── 01_exploration_REU.ipynb
│   ├── 02_contours_voronoi_REU.ipynb
│   ├── 03_exploration_socio_eco.ipynb
│   ├── 04_agregation_iris_bureau.ipynb
│   ├── 05_exploration_electorale.ipynb
│   ├── 06_clustering.ipynb
│   └── 07_regression_ols_wls.ipynb
├── src/
│   └── geo.py                  # fonctions de construction des polygones de Voronoï
├── figures/                    # figures produites par les notebooks
├── results/
│   └── tableau_comparatif_ols_wls.csv
├── data/                       # données (non versionnées)
├── requirements.txt
└── README.md
```

## Reproduire l'analyse

```bash
git clone https://github.com/ndiayeamadou-git/analyse-comportement-electoral.git
cd analyse-comportement-electoral
python -m venv .venv
source .venv/bin/activate        # sous Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

Placez les fichiers dans `data/` (voir `data/README.md`), puis exécutez les notebooks dans l'ordre. Ils ont été développés sur Google Colab : adaptez la variable de chemin (`BASE`) en début de notebook si vous les lancez en local.

## Résultats détaillés

### Cinq profils territoriaux (K-Means, k = 5, sur UMAP)

| Cluster | Part des bureaux | Profil | Candidat(s) dominant(s) |
|---|---|---|---|
| C0 | 19,7 % | Métropoles aisées | Macron (35,8 %) |
| C1 | 21,6 % | Sud-Ouest rural | Le Pen (24,4 %), Macron (22,8 %), Mélenchon (21,0 %) |
| C2 | 19,6 % | Littoral et Est | Macron (30,4 %), Le Pen (27,2 %) |
| C3 | 13,5 % | Banlieues populaires et DOM | Mélenchon (43,5 %) |
| C4 | 25,5 % | France populaire du Nord | Le Pen (38,7 %) |

Le choix de k = 5 plutôt que k = 3 (silhouette de 0,410 contre 0,430 dans l'espace UMAP) privilégie l'interprétabilité. Une tentative de Spectral Clustering a été abandonnée : la matrice d'affinité dense aurait nécessité environ 37 Go de mémoire.

### OLS global contre WLS local (mesures hors échantillon)

| Candidat | MAE OLS | MAE WLS | Gain MAE |
|---|---|---|---|
| Lassalle | 2,1232 | 2,0370 | 4,1 % |
| Le Pen | 5,9001 | 5,6831 | 3,7 % |
| Mélenchon | 5,1135 | 4,9316 | 3,6 % |
| Pécresse | 1,8843 | 1,8536 | 1,6 % |
| Jadot | 1,4282 | 1,4110 | 1,2 % |
| Macron | 4,6589 | 4,6109 | 1,0 % |
| Hidalgo | 0,8513 | 0,8459 | 0,6 % |
| Poutou | 0,4791 | 0,4773 | 0,4 % |
| Roussel | 1,0629 | 1,0596 | 0,3 % |
| Zemmour | 2,1929 | 2,1873 | 0,3 % |
| Arthaud | 0,3878 | 0,3889 | -0,3 % |
| Dupont-Aignan | 0,9206 | 0,9290 | -0,9 % |

Le gain moyen est modeste (1,3 %), mais la dispersion des coefficients locaux est de 2,4 à 7,7 fois supérieure à l'incertitude du coefficient global pour Macron, Le Pen et Mélenchon. Le lien entre profil socio-économique et vote varie donc réellement d'un territoire à l'autre. Le fichier complet, avec les RMSE, est dans `results/tableau_comparatif_ols_wls.csv`.

## Limites

- **Inférence écologique** : les résultats décrivent des relations entre territoires, pas des comportements individuels d'électeurs.
- **Zones d'influence approximatives** : les polygones de Voronoï approchent les zones desservies par chaque bureau, ils ne sont pas les contours réels.
- **Agrégation surfacique** : la redistribution des IRIS suppose une densité de population uniforme à l'intérieur de chaque IRIS.
- **Variables limitées** : huit variables socio-économiques seulement. Les catégories socioprofessionnelles (PCS) n'ont pas pu être intégrées.
- **Bande passante fixe** : σ est fixé à la médiane des distances, sans validation croisée.

## Perspectives

- Matrice de transfert de vote entre les deux tours (non réalisée).
- Intégration des PCS.
- Random Forest ou XGBoost avec importance des variables et valeurs SHAP.
- Détection de bureaux atypiques, dont les résultats s'écartent de ce que prédit leur profil socio-économique.

## Auteur

Amadou Ndiaye, Master MIASHS, Université Lumière Lyon 2. Stage encadré par Stéphane Chrétien (tuteur de stage) et Pablo Jensen (enseignant référent).
