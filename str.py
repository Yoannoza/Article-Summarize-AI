import streamlit as st
import requests

# Configuration de la page
st.set_page_config(
    page_title="Résumé d'Article IA",
    page_icon="📰",
    layout="centered"
)

# Design & style CSS personnalisé — Chic et moderne
st.markdown(
    """
    <style>
    /* Background et card central */
    .main {background-color: #f8f9fc; padding-top: 50px;}
    div.block-container { 
        background-color: white; 
        padding: 40px; 
        border-radius: 15px; 
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); 
        max-width: 700px; 
        margin: auto;
    }
    /* Titre principal */
    h1 {text-align: center; font-size: 2.2rem; color: #4a4a4a;}
    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        border: 1px solid #ddd; 
        border-radius: 12px; 
        padding: 12px; 
        background-color: #fdfdfd;
    }
    /* Boutons */
    .stButton>button {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white; 
        font-weight: bold;
        border: none; 
        border-radius: 12px; 
        padding: 12px 24px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2575fc 0%, #6a11cb 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(106, 17, 203, 0.3);
    }
    /* Radio et selectbox */
    .stRadio>div>label, .stSelectbox>div>div {
        font-weight: 500;
        color: #555;
    }
    /* Messages */
    .stAlert {border-radius: 12px;}
    </style>
    """,
    unsafe_allow_html=True
)

# Titre & intro
st.title("📰 Résumé Intelligent de Texte ou d'Article")
st.write("🔎 Obtenez l'essentiel d'un article ou d'un texte en quelques secondes, grâce à la puissance de l'IA.")

# Sélection de méthode (URL ou texte libre)
option = st.radio("📌 Choisissez une option :", ["Résumé d'un article via URL", "Résumé d'un texte saisi"])

# URL de l'API FastAPI
API_URL = "https://summurize-api-5069ac36b480.herokuapp.com/resume"

# Fonction pour appeler l'API
def generate_summary(data):
    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Erreur lors de la connexion à l'API : {e}")
        return None

# Liste de modèles IA
models = ["pegasus", "bart", "mistral", "llama"]

# Bloc URL
if option == "Résumé d'un article via URL":
    st.subheader("🌐 Analyse d'un article web")
    article_url = st.text_input("🔗 Collez l'URL de l'article ici")
    model = st.selectbox("🧠 Modèle de résumé", models, index=0)

    if st.button("✨ Générer le résumé"):
        if article_url.strip():
            with st.spinner("⏳ Analyse et génération en cours..."):
                data = {"url": article_url, "model": model}
                result = generate_summary(data)

                if result and 'resume' in result:
                    st.success("✅ Résumé généré avec succès !")
                    st.subheader(result.get('title', 'Titre non disponible'))
                    st.markdown(f"🔗 [Lien vers l'article original]({result.get('url')})")
                    st.markdown("### ✍️ Résumé généré :")
                    st.write(result['resume'])
                else:
                    st.error("⚠️ Une erreur est survenue lors de la génération.")
        else:
            st.warning("⚠️ Veuillez entrer une URL valide.")

# Bloc Texte Libre
elif option == "Résumé d'un texte saisi":
    st.subheader("📄 Résumé d'un texte libre")
    user_text = st.text_area("✍️ Collez votre texte ici")
    model = st.selectbox("🧠 Modèle de résumé", models, index=0)

    if st.button("✨ Générer le résumé"):
        if user_text.strip():
            with st.spinner("⏳ Génération en cours..."):
                data = {"text": user_text, "model": model}
                result = generate_summary(data)

                if result and 'resume' in result:
                    st.success("✅ Résumé généré avec succès !")
                    st.markdown("### ✍️ Résumé généré :")
                    st.write(result['resume'])
                else:
                    st.error("⚠️ Une erreur est survenue lors de la génération.")
        else:
            st.warning("⚠️ Veuillez saisir un texte valide.")

# Footer stylé
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #aaa; font-size: 0.85rem;">
        Créé avec 💙 par <a href="https://github.com/ton-repo" target="_blank" style="color:#6a11cb;">Toi</a> | Propulsé par Streamlit & FastAPI
    </div>
    """,
    unsafe_allow_html=True
)
