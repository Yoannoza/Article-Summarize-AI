import streamlit as st
import requests

# Configuration de la page
st.set_page_config(page_title="Résumé d'Article IA", page_icon="📰", layout="centered")

# Styles personnalisés
st.markdown(
    """
    <style>
    .main {background-color: #f4f4f9;}
    .stTextInput>div>div>input {border-radius: 10px; border: 1px solid #ddd; padding: 10px;}
    .stTextArea>div>textarea {border-radius: 10px; border: 1px solid #ddd; padding: 10px;}
    .stButton>button {border-radius: 10px; background-color: #4CAF50; color: white; padding: 10px 24px; border: none;}
    .stButton>button:hover {background-color: #45a049;}
    </style>
    """,
    unsafe_allow_html=True
)

# Titre et description
st.title("📰 Résumé Intelligent de Texte ou d'Article")
st.write("Obtenez rapidement l'essentiel d'un article à partir de son URL ou d'un texte saisi manuellement.")

# Choix de la méthode
option = st.radio("Choisissez une option", ["Résumé d'un article via URL", "Résumé d'un texte saisi"])

# L'API URL de FastAPI
API_URL = "https://summurize-api-5069ac36b480.herokuapp.com/resume"  # Assurez-vous d'utiliser l'URL correcte de votre API FastAPI

# Fonction pour générer le résumé via l'API FastAPI
def generate_summary(data):
    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()  # Pour lever une exception si la réponse n'est pas 200
        data = response.json()
        
        if 'resume' in data:
            return data
        else:
            st.error(f"Erreur : {data.get('error', 'Réponse inattendue')}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Une erreur est survenue : {e}")
        return None

# Liste des modèles disponibles
models = [
    "pegasus", "bart", "flan-t5", "distilbart", "t5", 
    "longt5", "led", "mbart", "mistral", "llama2"
]

if option == "Résumé d'un article via URL":
    article_url = st.text_input("Collez l'URL de l'article ici")
    model = st.selectbox("Choisissez le modèle", models, index=0)
    
    if st.button("Générer le résumé"):
        if article_url:
            with st.spinner('Analyse en cours...'):
                data = {'url': article_url, 'model': model}
                result = generate_summary(data)
                
                if result:
                    st.success("Résumé généré avec succès!")
                    st.subheader(result.get('title', 'Titre indisponible'))
                    st.markdown(f"🔗 [Lien vers l'article]({result.get('url')})")
                    st.markdown(f"### 📝 Résumé :")
                    st.write(result.get('resume'))
        else:
            st.warning("Veuillez entrer une URL valide.")

elif option == "Résumé d'un texte saisi":
    user_text = st.text_area("Collez votre texte ici")
    model = st.selectbox("Choisissez le modèle", models, index=0)
    
    if st.button("Résumer le texte"):
        if user_text:
            with st.spinner('Résumé en cours...'):
                data = {'text': user_text, 'model': model}
                result = generate_summary(data)
                
                if result:
                    st.success("Résumé généré avec succès!")
                    st.markdown(f"### 📝 Résumé :")
                    st.write(result.get('resume'))
        else:
            st.warning("Veuillez entrer du texte à résumer.")
