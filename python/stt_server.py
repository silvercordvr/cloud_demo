import os
from flask import Flask, request, jsonify
from whisper import load_model

app = Flask(__name__)

model = load_model("small", device="cuda")

@app.route('/stt', methods=['POST'])
def stt():
    data = request.json
    filename = data.get('filename')
    if not filename:
        return jsonify({"error": "Filename is required"}), 400

    try:
        result = model.transcribe(filename, language="English")
        return jsonify({"text": result['text']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5004)