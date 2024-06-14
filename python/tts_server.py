import os
from flask import Flask, request, jsonify, send_from_directory
from TTS.api import TTS
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '../tts'))

tts = None

def initialize_tts():
    global tts
    model_name = 'tts_models/multilingual/multi-dataset/xtts_v2'
    try:
        tts = TTS(model_name)
        tts.to('cuda')
        print(f"Model {model_name} loaded and moved to GPU successfully.")
    except Exception as e:
        print(f"Error loading model {model_name}: {e}")

@app.route('/tts', methods=['POST'])
def tts_generate():
    global tts
    data = request.json
    text = data.get('text')
    filename = data.get('filename')
    model_name_with_speaker = data.get('model_name', 'tts_models/multilingual/multi-dataset/xtts_v2')

    if ':' in model_name_with_speaker:
        model_name, speaker_idx = model_name_with_speaker.split(':', 1)
    else:
        model_name = model_name_with_speaker
        speaker_idx = ""

    if not text or not filename:
        return jsonify({"error": "Text and filename are required"}), 400

    output_path = os.path.join(app.static_folder, filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f'Model name: "{model_name}"')
    print(f'Speaker index: "{speaker_idx}"')

    try:       
        tts.tts_to_file(text=text, file_path=output_path, language="en", speaker=speaker_idx)
        return jsonify({"message": "File generated successfully", "path": f"{filename}"})
    except Exception as e:
        print(f"Error during TTS generation: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/tts-delete', methods=['DELETE'])
def delete_file():
    session = request.args.get('session')
    character = request.args.get('character')
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "Filename is required"}), 400

    if not filename.endswith('.wav'):
        return jsonify({"error": "Only WAV files can be deleted"}), 400

    secure_path = os.path.join(app.static_folder, secure_filename(session), secure_filename(character), secure_filename(filename))

    if os.path.isfile(secure_path):
        os.remove(secure_path)
        return jsonify({"message": "WAV file deleted successfully"}), 200
    else:
        return jsonify({"error": "File not found"}), 404      

@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    initialize_tts()
    app.run(port=5003)
