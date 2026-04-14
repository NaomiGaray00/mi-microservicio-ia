from flask import Flask, request, jsonify
from textblob import TextBlob
import nltk

# Esto descarga los archivos que le faltan a Railway para entender el texto
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
        
        # Análisis simple de polaridad
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
    app.run(host='0.0.0.0', port=5000)
