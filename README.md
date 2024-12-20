# Carte des Infrastructures Culturelles en France 🎭

Une application interactive pour visualiser et explorer les infrastructures culturelles à travers la France, développée dans le cadre du projet "Revitalisation des petites villes" de Data For Good.

## 🚀 Démarrage Rapide

0. Installer UV
   - Suivre https://docs.astral.sh/uv/getting-started/installation/

1. Cloner le dépôt et accéder au répertoire :
```bash
git clone git@github.com:naloui1/Dataforgood.git
cd Dataforgood
```

1. Créer et activer l'environnement virtuel :
```bash
uv venv --python 3.12
source .venv/bin/activate  # Linux/Mac

```

3. Installer les dépendances :
```bash
uv sync
```

4. Lancer l'application :
```bash
uv run streamlit run app.py
```

L'application sera accessible à l'adresse : http://localhost:8501

## Mind map
- https://lucid.app/lucidspark/8e5176a1-7ab5-4476-b3c4-c64e9fc3202a/edit?invitationId=inv_8851fc4c-79e6-4a9d-acde-1809bb47f920

## 🎯 Fonctionnalités

- **Carte Interactive** : Visualisation des sites culturels avec clustering
- **Filtres Dynamiques** :
  - Recherche par commune
  - Filtrage par type d'infrastructure
  - Filtrage par catégorie culturelle
- **Interface Adaptative** :
  - Mode sombre/clair
  - Statistiques en temps réel
  - Zoom intelligent sur les communes

## 📊 Données

Les données (`data/mock_cultural_data.csv`) incluent :
- Nom et code postal des communes
- Types d'infrastructures culturelles
- Catégories (patrimoine, spectacle vivant)
- Coordonnées géographiques

## 🔧 Technologies

- Python
- Streamlit
- Folium
- Pandas
- Streamlit-Folium

## 📝 Contexte du Projet

Ce projet s'inscrit dans l'initiative "Revitalisation des petites villes" de Data For Good, visant à enrichir l'outil Dataviz PVD de la Banque des Territoires. Il se concentre spécifiquement sur l'analyse et la visualisation de l'offre culturelle dans les petites villes françaises.

Les "petites villes" sont essentielles à la vie des habitants, surtout dans les territoires ruraux, notamment pour l'accès à la culture et au patrimoine. Le programme Petites Villes de Demain (PVD) accompagne les villes de moins de 20 000 habitants qui jouent un rôle de centralité sur leur bassin de vie.

Cette application fait partie des outils développés pour aider à :
- Visualiser la répartition des infrastructures culturelles
- Analyser l'accessibilité des équipements culturels
- Comprendre les spécificités culturelles de chaque territoire

Pour plus d'informations sur le projet global : https://defis.data.gouv.fr/defis/revitalisation-des-petites-villes