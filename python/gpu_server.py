# GPU server with external API

from flask import Flask, request, jsonify, Response
from urllib.parse import quote, unquote
import requests
from auth import check_auth
from functools import wraps
import os

app = Flask(__name__)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

def proxy_request(url, method, data):
    if method == 'GET':
        response = requests.get(url)
    elif method == 'POST':
        response = requests.post(url, json=data)
    elif method == 'PUT':
        response = requests.put(url, json=data)
    elif method == 'DELETE':
        response = requests.delete(url)
    else:
        return jsonify({"error": "Unsupported HTTP method"}), 400
    
    return jsonify(response.json()), response.status_code

@app.route('/')
def hello():
    return '<h1>Main GPU Server</h1>'

# auth test for any machine
@app.route('/echo-post', methods=['POST'])
@requires_auth
def handle_post():
    data = request.get_json()
    if data is None:
        return 'No JSON data provided', 400
    return {'received_data': data}, 200       

# STT
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploaded_wav_files')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
@app.route('/upload-wav', methods=['POST'])
@requires_auth
def upload_wav_bytes():
    try:
        user_id = request.headers.get('User-ID')
        if not user_id:
            return jsonify({"error": "User-ID header is missing"}), 400

        byte_array = request.get_data()
        if not byte_array:
            return jsonify({"error": "No data received"}), 400

        filename = f"{user_id}_uploaded_file.wav"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, 'wb') as wav_file:
            wav_file.write(byte_array)
        
        url = 'http://127.0.0.1:5004/stt'
        data = {"filename":file_path}
        response = requests.post(url, json=data)
        os.remove(file_path)
        return jsonify(response.json())

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        print(traceback.format_exc()) 
        return jsonify({"error": str(e)}), 500    

# Request analyzer
@app.route('/photo-analyze', methods=['POST'])
@requires_auth
def forward_request_photo():
    data = request.json
    url = 'http://127.0.0.1:5002/photo-analyze'
    response = requests.post(url, json=data)
    return jsonify(response.json())   

# TTS
@app.route('/tts', methods=['POST'])
@requires_auth
def forward_request_tts():
    data = request.json
    url = 'http://127.0.0.1:5003/tts'
    response = requests.post(url, json=data)
    return jsonify(response.json())   

# Deleting audio file
@app.route('/tts-delete', methods=['DELETE'])
@requires_auth
def forward_delete_request_tts():
    session = request.args.get('session')
    character = request.args.get('character')
    filename = request.args.get('filename')

    if not all([session, character, filename]):
        return jsonify({"error": "All parameters (session, character, filename) are required"}), 400
    url = f'http://127.0.0.1:5003/tts-delete?session={quote(session)}&character={quote(character)}&filename={quote(filename)}'
    response = requests.delete(url)
    return jsonify(response.json()), response.status_code

# Static audio files (TTS generated)
@app.route('/audio/<path:encoded_filename>')
def get_file(encoded_filename):
    decoded_filename = unquote(encoded_filename)
    tts_server_url = f'http://127.0.0.1:5003/static/{decoded_filename}'
    response = requests.get(tts_server_url, stream=True)

    if response.status_code != 200:
        return jsonify({"error": "File not found or error on TTS server"}), response.status_code

    return Response(response.iter_content(chunk_size=1024), 
                    content_type=response.headers['Content-Type'],
                    direct_passthrough=True)     

#OobaBooga proxy
@app.route('/chat', methods=['POST'])
@requires_auth
def forward_request():
    data = request.json
    url = 'http://127.0.0.1:5000/v1/chat/completions'
    response = requests.post(url, json=data)
    return jsonify(response.json())                    

# Chat message
@app.route('/chat-message-ue', methods=['POST'])
@requires_auth
def forward_request_chat_message_ue():
    data = request.json
    url = 'http://127.0.0.1:6969/chat-message-ue'
    response = requests.post(url, json=data)
    return jsonify(response.json())                         

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)   