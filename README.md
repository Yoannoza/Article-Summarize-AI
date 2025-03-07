# 📰 Résumeur Automatique d'Articles - FastAPI + Streamlit

## 🚀 Présentation

Lie
https://gamma.app/docs/Untitled-k5cnybpu8oa2eh2


Ce projet propose une **API web** et une **interface utilisateur Streamlit** pour **résumer automatiquement des articles de presse** ou tout autre texte. L’utilisateur peut soit **fournir une URL d’article**, soit **coller un texte** directement. Le résumé est généré par **l'un des 4 modèles supportés**, sélectionnables à la demande :

| Modèle    | Fournisseur   | Points forts                                                                                                                                                                                |
| :-------- | :------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Pegasus   | Hugging Face  | Spécialisé dans les news, très performant sur la presse.  Bon rapport qualité/vitesse.                                                                                                           |
| BART      | Hugging Face  | Concis et précis, bon équilibre global.  Idéal pour des résumés équilibrés.                                                                                                                |
| Mistral   | Groq          | Ultra rapide, performant sur textes variés.  Choix parfait pour une latence minimale.                                                                                                     |
| Llama 2   | Groq          | Modèle large, excellente qualité sur textes longs et complexes.  Privilégiez ce modèle pour les textes qui nécessitent une compréhension approfondie.                                    |

---

## 🏗️ Architecture

### 📦 Composants

- **FastAPI** : Back-end exposant l’API `/resume`.
- **Streamlit** : Interface utilisateur simple pour tester les résumés.
- **Hugging Face Inference API** : Utilisé pour Pegasus et BART.
- **Groq API** : Utilisé pour Mistral et Llama 2.
- **Newspaper3k**: Extraction d'articles à partir d'URLs.

---

### 🔗 Flux de fonctionnement

1. L’utilisateur choisit entre "URL" ou "Texte libre" dans l'interface Streamlit.
2. Le texte (ou le contenu extrait de l’URL) est transmis à l’API FastAPI.
3. Selon le modèle choisi :
    - Pegasus/BART : Appel à la Hugging Face Inference API.
    - Mistral/Llama 2 : Appel à la Groq API.
4. Le résumé est retourné à l’utilisateur via l'interface Streamlit.

---

## ⚙️ Installation

### 1️⃣ Cloner le projet

```bash
git clone https://github.com/votre-repo/resumeur-articles.git
cd resumeur-articles
```

2️⃣ Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
# ou
venv\Scripts\activate      # Windows
```


3️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

4️⃣ Configurer les clés API

Créer un fichier .env à la racine du projet :
```bash
touch .env
```
Ajouter les clés API dans le fichier .env :

```bash
HUGGINGFACE_API_KEY=your_huggingface_api_key
GROQ_API_KEY=your_groq_api_key
```

Important: Remplacez your_huggingface_api_key et your_groq_api_key par vos clés API réelles.


▶️ Lancer le projet

Démarrer l’API FastAPI :
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Lancer l’interface utilisateur Streamlit :
```bash
streamlit run app/interface.py
```

📡 Endpoints
Résumer un article (API)
Méthode: POST
Endpoint: /resume
Corps de la requête (JSON)
Pour une URL :
```json
{
    "url": "https://exemple.com/article",
    "text": null,
    "model": "pegasus"
}
```
Pour un texte brut :
```json
{
    "url": null,
    "text": "Voici un texte à résumer...",
    "model": "mistral"
}
```

Paramètres :
url: (string, optionnel) L'URL de l'article à résumer. Doit être null si text est fourni.
text: (string, optionnel) Le texte à résumer. Doit être null si url est fourni.
model: (string, requis) Le modèle à utiliser pour le résumé. Les options sont: pegasus, bart, mistral, llama.


🌐 Interface utilisateur (Streamlit)
L’interface Streamlit permet :
De coller une URL ou un texte brut.
De choisir le modèle à utiliser.
De comparer les résumés obtenus avec chaque modèle (fonctionnalité À venir).



