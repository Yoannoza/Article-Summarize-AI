import chainlit as cl
import re
import requests

@cl.on_chat_start
async def start():
    await cl.Message(content="Hello World! 👋").send()

def est_un_lien(texte: str) -> int:
    """
    Vérifie si une chaîne de texte est un lien URL valide.

    Args:
        texte (str): La chaîne de texte à vérifier.

    Returns:
        int: 1 si la chaîne de texte est un lien URL valide, sinon 0.
    """
    regex = r"^(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$"
    return 1 if re.match(regex, texte) else 0

@cl.on_message
async def handle_message(message: cl.Message):
    # Déterminer si l'entrée est un lien ou un texte
    verify_link_or_not = est_un_lien(message.content)

    API_URL = "https://article-summarize-ai.onrender.com/resume" 
    # API_URL = "http://127.0.0.1:8000/resume"  # Pour local

    response_text = "Une erreur est survenue."

    if verify_link_or_not == 1:
        # L'utilisateur a fourni une URL
        try:
            response = requests.post(API_URL, json={'url': message.content})
            data = response.json()

            if response.status_code == 200 and 'resume' in data:
                response_text = (
                    f"✅ **Résumé généré avec succès !**\n\n"
                    f"**Titre :** {data.get('title', 'Titre indisponible')}\n"
                    f"**Lien :** {data.get('url', 'Lien indisponible')}\n\n"
                    f"**Résumé :**\n{data.get('resume')}"
                )
            else:
                response_text = f"⚠️ Erreur : {data.get('detail', 'Réponse inattendue')}"
        except Exception as e:
            response_text = f"❌ Une erreur est survenue : {e}"

    elif verify_link_or_not == 0:
        # L'utilisateur a fourni un texte
        try:
            response = requests.post(API_URL, json={'text': message.content})
            data = response.json()

            if response.status_code == 200 and 'resume' in data:
                response_text = f"📝 **Résumé généré avec succès !**\n\n{data.get('resume')}"
            else:
                response_text = f"⚠️ Erreur : {data.get('detail', 'Réponse inattendue')}"
        except Exception as e:
            response_text = f"❌ Une erreur est survenue : {e}"

    # Envoyer la réponse
    await cl.Message(content=response_text).send()
















# import chainlit as cl
# import re
# import requests

# @cl.on_chat_start
# async def main():
#     await cl.Message(content="Hello Wor").send()

# def est_un_lien(texte):
#   """
#   Vérifie si une chaîne de texte est un lien URL valide.

#   Args:
#     texte: La chaîne de texte à vérifier.

#   Returns:
#     1 si la chaîne de texte est un lien URL valide, 1 sinon.
#   """
#   # Expression régulière pour détecter les liens URL
#   regex = r"^(http(s)?://)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$"
  
#   # Vérifier si le texte correspond à l'expression régulière
#   if re.match(regex, texte):
#     return 1
#   else:
#     return 0


# @cl.on_message
# async def main(message: cl.Message):
#     # Créer un message personnalisé
#     verify_link_or_not = est_un_lien(message.content)

#     # URL de l'API FastAPI
#     API_URL = "https://article-summarize-ai.onrender.com/resume" 
    
#     #API_URL = "http://127.0.0.1:8000/chainlit"  # Assurez-vous que l'API FastAPI est en cours d'exécution

#     if verify_link_or_not == 1:
#             if message.content:
#                     try:
#                         response = requests.post(API_URL, json={'url': message.content})
#                         data = response.json()
#                         if response.status_code == 200 and 'resume' in data:
#                             #response_text = f" Résumé généré avec succès!!!/n Titre de l'article: {data.get('title', 'Titre indisponible')}/n Lien vers l'article: {data.get('resume')}"
#                             response_text = (
#                                         f"✅ **Résumé généré avec succès !**\n\n"
#                                         f"**Titre :** {data.get('title', 'Titre indisponible')}\n"
#                                         f"**Lien :** {data.get('url', 'Lien indisponible')}\n\n"  # Correction ici
#                                         f"**Résumé :**\n{data.get('resume')}"
#                                     )
#                         else:
#                             response_text = f"Erreur !!!: {data.get('error', 'Réponse inattendue')}"
#                     except Exception as e:
#                         response_text = f"Une erreur est survenue : {e}"
#             else:
#                 st.warning("Veuillez entrer une URL valide.")

#     elif verify_link_or_not == 0:
#                     try:
#                         response = requests.post(API_URL, json={'text': message.content})
#                         data = response.json()
#                         if response.status_code == 200 and 'resume' in data:
#                             response_text = f" Résumé généré avec succès!!! 📝/n {data.get('resume')}"
#                         else:
#                             response_text = f"Erreur !!!: {data.get('error', 'Réponse inattendue')}"
#                     except Exception as e:
#                         response_text = f"Une erreur est survenue : {e}"

#     # response_text = f"bienvenue vous vous {message.content}"
    
#     # Envoyer une réponse
#     await cl.Message(
#         content=response_text
#         # content=response_text
#     ).send()

