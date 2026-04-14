from flask import Flask, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

@app.route('/analizar', methods=['POST'])
def analizar():
    datos = request.get_json()
    texto = datos.get('texto', '')
    
    # Traducimos mentalmente para que la IA entienda mejor el sentimiento
    try:
        blob = TextBlob(texto)
        # Si el texto es español, lo analizamos considerando la traducción
        if blob.detect_language() != 'en':
            blob = blob.translate(to='en')
        
        polaridad = blob.sentiment.polarity
    except:
        # Si falla la detección (texto muy corto), usamos el original
        polaridad = TextBlob(texto).sentiment.polarity
    
    resultado = "Positivo" if polaridad > 0.1 else "Negativo" if polaridad < -0.1 else "Neutral"
    
    return jsonify({
        "status": "success",
        "servicio": "IA Sentiment Analysis",
        "sentimiento": resultado,
        "puntuacion": round(polaridad, 2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)