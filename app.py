from flask import Flask, request, jsonify
import requests
from newspaper import Article
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/pegasus-cnn_dailymail"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
def get_summary(article_text):
    payload = {"inputs": article_text}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    result = response.json()
    if isinstance(result, list):  # Cas normal
        return result[0]['summary_text']
    elif 'error' in result:
        raise Exception(result['error'])
    return "Résumé non disponible"

@app.route('/resume', methods=['POST'])
def resume_article():
    data = request.get_json()
    if data.get('url'):
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL manquante'}), 400

        try:
            article = Article(url)
            article.download()
            article.parse()
            summary = get_summary(article.text)

            return jsonify({
                'title': article.title,
                'url': url,
                'resume': summary
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    elif data.get('text'):
        text = data.get('text')

        if not text:
            return jsonify({'error': 'Texte manquant'}), 400

        try:
            summary = get_summary(text)

            return jsonify({
                'resume': summary
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': "No Link, No Text"}), 500
        


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
