from flask import Flask, request, jsonify
from textblob import TextBlob
import nltk
import os  # <--- Agregamos esto para leer variables de la nube

# Descarga de recursos necesaria para la IA
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)

@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        datos = request.get_json()
        if not datos or 'texto' not in datos:
            return jsonify({"error": "No se envió el campo 'texto'"}), 400
            
        texto = datos.get('texto', '')
        blob = TextBlob(texto)
        
        polaridad = blob.sentiment.polarity
        resultado = "Positivo" if polaridad > 0.1 else "Negativo" if polaridad < -0.1 else "Neutral"
        
        return jsonify({
            "status": "success",
            "sentimiento": resultado,
            "puntuacion": round(polaridad, 2)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Esto le dice a tu código: "Usa el puerto que te dé la nube, o el 5000 si estás en mi PC"
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)
