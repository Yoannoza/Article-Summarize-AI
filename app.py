from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from newspaper import Article
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# Liste des modèles supportés
MODELS = {
    "pegasus": "google/pegasus-cnn_dailymail",
    "bart": "facebook/bart-large-cnn",
    "flan-t5": "google/flan-t5-large",
    "distilbart": "sshleifer/distilbart-cnn-12-6",
    "t5": "t5-base",
    "longt5": "google/long-t5-tglobal-base",
    "led": "allenai/led-base-16384",
    "mbart": "facebook/mbart-large-50",
    "mistral": "mistralai/Mistral-7B-Instruct-v0.2",
    "llama2": "meta-llama/Llama-2-7b-chat",
}

app = FastAPI()


class ArticleRequest(BaseModel):
    url: str = None
    text: str = None
    model: str = "pegasus"


def get_summary(article_text, model_name):
    if model_name not in MODELS:
        raise HTTPException(status_code=400, detail=f"Modèle non supporté: {model_name}")
    
    api_url = f"https://api-inference.huggingface.co/models/{MODELS[model_name]}"
    payload = {"inputs": article_text}
    
    response = requests.post(api_url, headers=HEADERS, json=payload)
    result = response.json()
    
    if isinstance(result, list):
        return result[0]['summary_text']
    elif 'error' in result:
        raise HTTPException(status_code=500, detail=f"Erreur Hugging Face: {result['error']}")
    
    raise HTTPException(status_code=500, detail="Résumé non disponible")


@app.post("/resume")
def resume_article(request: ArticleRequest):
    if request.url:
        try:
            article = Article(request.url)
            article.download()
            article.parse()
            summary = get_summary(article.text, request.model)

            return {
                'title': article.title,
                'url': request.url,
                'resume': summary,
                'model': request.model
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur extraction: {str(e)}")

    elif request.text:
        try:
            summary = get_summary(request.text, request.model)
            return {
                'resume': summary,
                'model': request.model
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur résumé: {str(e)}")

    raise HTTPException(status_code=400, detail="Ni URL ni texte fournis")


@app.get("/health")
def health_check():
    """Vérifie si tous les modèles sont dispos et gère les erreurs comme l'authentification, timeout, etc."""
    statuses = {}

    # On parcourt chaque modèle et on fait une requête GET pour vérifier sa disponibilité
    for name, model_path in MODELS.items():
        try:
            # Essayer d'obtenir la réponse du modèle
            response = requests.get(f"https://api-inference.huggingface.co/models/{model_path}", headers=HEADERS, timeout=10)

            # Vérification de la réponse en fonction du code de statut
            if response.status_code == 200:
                statuses[name] = "OK"
            elif response.status_code == 403:
                statuses[name] = "Accès interdit (erreur d'authentification)"
            elif response.status_code == 404:
                statuses[name] = "Modèle non trouvé"
            elif response.status_code == 500:
                statuses[name] = "Erreur serveur interne"
            else:
                statuses[name] = f"Erreur inconnue: {response.status_code}"
        
        except requests.exceptions.Timeout:
            statuses[name] = "Erreur: Timeout (Le serveur met trop de temps à répondre)"
        except requests.exceptions.TooManyRedirects:
            statuses[name] = "Erreur: Trop de redirections"
        except requests.exceptions.RequestException as e:
            # Gestion générale de toutes les autres erreurs
            statuses[name] = f"Erreur de requête: {str(e)}"

    return statuses