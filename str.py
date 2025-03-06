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

if option == "Résumé d'un article via URL":
    article_url = st.text_input("Collez l'URL de l'article ici")
    if st.button("Générer le résumé"):
        if article_url:
            with st.spinner('Analyse en cours...'):
                try:
                    response = requests.post("https://summurize-api-5069ac36b480.herokuapp.com/resume", json={'url': article_url})
                    data = response.json()
                    if response.status_code == 200 and 'resume' in data:
                        st.success("Résumé généré avec succès!")
                        st.subheader(data.get('title', 'Titre indisponible'))
                        st.markdown(f"🔗 [Lien vers l'article]({data.get('url')})")
                        st.markdown(f"### 📝 Résumé :")
                        st.write(data.get('resume'))
                    else:
                        st.error(f"Erreur: {data.get('error', 'Réponse inattendue')}")
                except Exception as e:
                    st.error(f"Une erreur est survenue : {e}")
        else:
            st.warning("Veuillez entrer une URL valide.")

elif option == "Résumé d'un texte saisi":
    user_text = st.text_area("Collez votre texte ici")
    if st.button("Résumer le texte"):
        if user_text:
            with st.spinner('Résumé en cours...'):
                try:
                    response = requests.post("https://article-summarize-ai.onrender.com/resume", json={'text': user_text})
                    data = response.json()
                    if response.status_code == 200 and 'resume' in data:
                        st.success("Résumé généré avec succès!")
                        st.markdown(f"### 📝 Résumé :")
                        st.write(data.get('resume'))
                    else:
                        st.error(f"Erreur: {data.get('error', 'Réponse inattendue')}")
                except Exception as e:
                    st.error(f"Une erreur est survenue : {e}")
        else:
            st.warning("Veuillez entrer du texte à résumer.")
