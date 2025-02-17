# Resumeur Automatique d'Articles - API Flask

Ce projet est une API REST construite avec Flask permettant de résumer automatiquement des articles à partir d'une URL. Elle utilise le modèle PEGASUS de Google pré-entraîné sur CNN/DailyMail pour générer des résumés pertinents.

## Fonctionnalités

- Extraire le contenu d'un article à partir d'une URL.
- Générer automatiquement un résumé pertinent.
- Utilise Hugging Face Inference API pour des performances optimales.
- Interface REST simple via Flask.

## Prérequis

- Python 3.x
- Compte sur [Hugging Face](https://huggingface.co/)

## Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/tonpseudo/resumeur-automatique-api.git
cd resumeur-automatique-api
```

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

3. Créer un fichier `.env` pour stocker la clé API Hugging Face :

```
HUGGINGFACE_API_KEY=ton_token_huggingface
```

## Utilisation

### Lancer le serveur

```bash
python app.py
```

Par défaut, le serveur tourne sur `http://127.0.0.1:5000`.

### Effectuer une requête

Exemple avec `curl` :

```bash
curl -X POST http://127.0.0.1:5000/resume \  
-H "Content-Type: application/json" \  
-d '{"url": "https://exemple.com/article"}'
```

Exemple de réponse :

```json
{
  "title": "Titre de l'article",
  "url": "https://exemple.com/article",
  "resume": "Résumé généré ici."
}
```

## Déploiement

### Sur Railway.app

1. Créer un fichier `Procfile` :

```
web: python app.py
```

2. Pousser le projet sur GitHub.
3. Sur [Railway.app](https://railway.app/), créer un projet, connecter le repo GitHub et déployer.

### Utiliser Hugging Face API

Ce projet est conçu pour utiliser l'Inference API de Hugging Face avec le modèle :

- Modèle utilisé : [google/pegasus-cnn_dailymail](https://huggingface.co/google/pegasus-cnn_dailymail)

## Configuration Personnalisée

Si vous avez fine-tuné votre propre modèle Pegasus sur Hugging Face, remplacez l'URL de l'API dans `app.py` :

```python
API_URL = "https://api-inference.huggingface.co/models/votre-utilisateur/votre-modele"
```

## Technologies Utilisées

- Flask
- Hugging Face Transformers
- Newspaper3k
- PEGASUS

## Structure du Projet

```
.
├── app.py
├── requirements.txt
├── Procfile
├── README.md
└── .env
```

## Améliorations Futures

- Ajouter la gestion des langues multiples (mBART, Mistral, etc.).
- Intégrer la possibilité de choisir le modèle via la requête.
- Déploiement avec Docker.

## Auteur

- [Ton Nom](https://github.com/tonpseudo)

## Licence

Ce projet est sous licence MIT.

