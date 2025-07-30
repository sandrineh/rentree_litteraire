# 📚 Rentrée Littéraire 2023 – Analyse & Visualisation

Ce projet a pour objectif d’explorer, analyser et visualiser les données relatives à la rentrée littéraire 2023.  
Il permet d’identifier les tendances par genres, auteurs, maisons d’édition, et de représenter ces informations de manière interactive.

---

## 🎯 Objectifs du projet

- Centraliser les données sur la rentrée littéraire 2023 (œuvres, auteurs, prix littéraires, genres, etc.).
- Construire une base de données structurée pour faciliter les analyses.
- Créer des visualisations interactives (nuages de mots, cartes, graphiques).
- Mettre en place un environnement reproductible avec Poetry et Docker.
- Définir une pipeline de chargement de données depuis Excel vers PostgreSQL.

---

## 🛠️ Stack technique

- **Langage principal** : Python 3.10
- **Gestion des dépendances** : [Poetry](https://python-poetry.org/)
- **Bibliothèques principales** :
  - [geopy](https://geopy.readthedocs.io/) – géocodage et localisation
  - [folium](https://python-visualization.github.io/folium/) – cartes interactives
  - [altair](https://altair-viz.github.io/) – visualisations statistiques
  - [wordcloud](https://amueller.github.io/word_cloud/) – nuages de mots
  - [textblob](https://textblob.readthedocs.io/) – traitement de texte
  - [spaCy](https://spacy.io/) – NLP
- **Base de données** : PostgreSQL
- **Conteneurisation** : Docker (prévue pour les phases suivantes)

---

## 📂 Structure du dépôt

```

.
├── RL\_2023.py                        # Script principal
├── nuagemot.py                       # Génération nuage de mots
├── page\_prix\_litteraire.py           # Page dédiée aux prix littéraires
├── page\_rentree\_litteraire.py        # Page d’accueil / analyse générale
├── page\_rentree\_litteraire\_genre.py  # Analyse par genres
├── word\_cloud.py                     # Visualisations nuages de mots
├── RL\_23.ipynb                       # Notebook d’analyse
├── data/                             # Données brutes et transformées (.csv, .pkl)
├── pyproject.toml                    # Configuration Poetry
├── poetry.lock                       # Verrouillage des dépendances
├── requirements.txt                  # Dépendances (export possible depuis Poetry)
└── README.md                         # Ce fichier

````

---

## 🚀 Installation & exécution

### 1. Cloner le dépôt
```bash
git clone https://github.com/sandrineh/rentree_litteraire.git
cd rentree_litteraire
````

### 2. Installer les dépendances avec Poetry

```bash
poetry install
```

### 3. Activer l’environnement virtuel

```bash
poetry shell
```

### 4. Lancer les scripts ou notebooks

Exemple pour lancer le script principal :

```bash
python RL_2023.py
```

---

## 🗺️ Roadmap

### Phase 0 – Mise en place technique (en cours)

* [x] Créer schéma BDD dans DrawDB
* [x] Créer repo Git avec Poetry
* [ ] Écrire un README.md clair (objectif, stack, roadmap)
* [ ] Configurer PostgreSQL + Docker
* [ ] Écrire script de chargement Excel → PostgreSQL

### Phase 1 – Traitement & analyse des données

* Nettoyage et normalisation des données
* Intégration dans PostgreSQL
* Premières visualisations

### Phase 2 – Application interactive

* Interface Streamlit pour navigation et filtres
* Visualisations interactives
* Export des données

### Phase 3 – Déploiement

* Conteneurisation avec Docker
* Déploiement sur plateforme cloud (HuggingFace Spaces, Render, etc.)

---

## 📄 Licence

Ce projet est sous licence **MIT** – libre d’utilisation, modification et redistribution avec attribution.