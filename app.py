from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from newspaper import Article
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

# Charger les variables d'environnement
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Liste des modèles supportés
MODELS = {
    "pegasus": "google/pegasus-cnn_dailymail",
    "bart": "facebook/bart-large-cnn",
    "mistral": "mixtral-8x7b-32768",
    "llama": "llama-3.3-70b-versatile", 
}

app = FastAPI()

# Ajouter CORSMiddleware pour permettre les requêtes CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines (ou spécifie des origines précises comme ["https://ton-front-end.com"])
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permet tous les headers
)

class ArticleRequest(BaseModel):
    url: str = None
    text: str = None
    model: str = "pegasus"

def get_summary(article_text, model_name):
    # Vérifier si le modèle est un modèle Groq ou Hugging Face
    if model_name not in MODELS:
        raise HTTPException(status_code=400, detail=f"Modèle non supporté: {model_name}")
    
    # Si le modèle est Mistral ou Llama, utiliser Groq
    if model_name in ["mistral", "llama"]:
        return get_summary_from_groq(article_text, model_name)
    
    # Si le modèle est sur Hugging Face, on fait un appel classique
    return get_summary_from_huggingface(article_text, model_name)

def get_summary_from_huggingface(article_text, model_name):
    # Utilisation de l'API Hugging Face (ancienne méthode)
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    api_url = f"https://api-inference.huggingface.co/models/{MODELS[model_name]}"
    payload = {"inputs": article_text}
    
    response = requests.post(api_url, headers=HEADERS, json=payload)
    result = response.json()
    
    if isinstance(result, list):
        return result[0]['summary_text']
    elif 'error' in result:
        raise HTTPException(status_code=500, detail=f"Erreur Hugging Face: {result['error']}")
    
    raise HTTPException(status_code=500, detail="Résumé non disponible")

def get_summary_from_groq(article_text, model_name):
    # Utilisation de l'API Groq pour Mistral ou Llama
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    # Préparer les données pour l'API Groq
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    data = {
        "model": MODELS[model_name],
        "messages": [{
            "role": "system",
            "content": "Tu es un résuméur d'articles de presse. Fais de super résumés."
        }, {
            "role": "user",
            "content": article_text
        }]
    }
    
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    result = response.json()
    
    if response.status_code == 200 and 'choices' in result:
        return result['choices'][0]['message']['content']
    else:
        raise HTTPException(status_code=500, detail=f"Erreur Groq: {result.get('error', 'Inconnue')}")

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
    """Vérifie si tous les modèles sont dispos"""
    statuses = {}
    for name, model_path in MODELS.items():
        response = requests.get(f"https://api-inference.huggingface.co/models/{model_path}", headers=HEADERS)
        statuses[name] = "ok" if response.status_code == 200 else "indisponible"

    return statuses
