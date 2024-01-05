# Projet Gestionnaire de Tâches

## Description
Le projet Gestionnaire de Tâches est une application web Flask permettant de gérer une liste de tâches, avec la possibilité d'ajouter, supprimer et trier les tâches en fonction de différents critères.

## Fonctionnalités
- Ajout d'une nouvelle tâche avec titre, contenu, date, heure et indication d'urgence.
- Suppression d'une tâche existante.
- Affichage de la liste des tâches triées par nom, date ou date de création.
- Possibilité de rechercher des tâches par titre.
- Gestion des tâches urgentes avec un style distinct.

## Structure du Projet
- `app.py`: Fichier principal contenant le code Flask et la logique métier.
- `templates/`: Dossier contenant les fichiers HTML pour les pages web.
- `emploidutemps.db`: Base de données SQLite pour stocker les tâches.

## Installation
1. Cloner le dépôt: `git clone https://github.com/votre-utilisateur/emploi-du-temps.git`
2. Installer les dépendances: `pip install -r requirements.txt`

## Utilisation
1. Exécuter l'application: `python app.py`
2. Accéder à l'application dans un navigateur à l'adresse [http://localhost:5000](http://localhost:5000)

## Configuration
Aucune configuration spécifique n'est nécessaire pour l'utilisation de base. La base de données est automatiquement créée.
