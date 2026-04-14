from flask import Flask, request, jsonify
from textblob import TextBlob
import nltk
import os

# Recursos necesarios
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)

@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        datos = request.get_json()
        textoOriginal = datos.get('texto', '')
        
        # --- LA MAGIA DE LA IA ---
        blob = TextBlob(textoOriginal)
        
        try:
            # Intentamos traducir al inglés para un análisis preciso
            # Si ya está en inglés o falla, seguirá con el original
            textoTraducido = str(blob.translate(to='en'))
            blob = TextBlob(textoTraducido)
        except:
            pass 
        # -------------------------

        polaridad = blob.sentiment.polarity
        
        # Ajustamos los rangos para mayor sensibilidad
        if polaridad > 0.05:
            resultado = "Positivo"
        elif polaridad < -0.05:
            resultado = "Negativo"
        else:
            resultado = "Neutral"
        
        return jsonify({
            "status": "success",
            "sentimiento": resultado,
            "puntuacion": round(polaridad, 2),
            "texto_analizado": str(blob) # Verás cómo la IA lo "leyó"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)
