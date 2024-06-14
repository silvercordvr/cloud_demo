## Task: It is necessary to install a system with the following characteristics on a cloud server.

### Technical Specification

1. **PyTorch and CUDA Support**
   - Install the latest version of PyTorch with CUDA support and ensure NVIDIA drivers are compatible.

2. **Oobabooga Text Generation Web UI**
   - Install from [GitHub repository](https://github.com/oobabooga/text-generation-webui).
   - Preinstall model: [Noromaid-13B-v0.3-AWQ](https://huggingface.co/TheBloke/Noromaid-13B-v0.3-AWQ).

3. **Coqui.ai Text-to-Speech (TTS) Framework**
   - Install from [GitHub repository](https://github.com/coqui-ai/TTS).
   - Preinstall model: [XTTS-v2](https://huggingface.co/coqui/XTTS-v2).

4. **Whisper Speech-to-Text (STT) Model**
   - Install from [GitHub repository](https://github.com/openai/whisper).

5. **Python Server for TTS**
   - Code: [python/tts_server.py](python/tts_server.py).
   - Server setup for generating audio files with Coqui.ai and serving them via HTTP.

6. **Python Server for STT**
   - Code: [python/stt_server.py](python/stt_server.py).
   - Server for recognizing speech from audio files to text.

7. **Node.js and NPM**
   - Ensure the latest version of Node.js and NPM are installed.

8. **Node.js Server for Chatbot Response**
   - Code: [server.js](server.js).
   - Node.js server for generating final responses from the chatbot.

9. **Python Server for Proxying**
   - Code: [python/gpu_server.py](python/gpu_server.py).
   - Server for proxying requests to auxiliary servers.

10. **NGINX Server for Proxying and SSL**
    - Install and configure NGINX for final proxying and SSL support.

### Final Outcome
The final deliverable should include the following functionalities:
   - Processing requests to servers as specified in the proxy server code.
   - All communication should be secured via HTTPS, using either the IP address or domain name of the remote server.

### System Startup

Before starting the Node.js server, you need to install the necessary modules. Run the `npm install` command in the console in the project directory (at the same level as the `package.json` file).

The project's startup script is `start.js`, and `npm start` command launches the Node.js server and all Python servers.

To start the text generation, TTS, and SST services, create a batch (`.bat`) or bash (`.sh`) script based on your operating system. Include the command to run `start.js`.

Ensure servers are resilient with automatic restarts if any server goes offline. Configure NGINX for final proxying with SSL to ensure all routes are accessible via HTTPS.

### Tests

Test requests to assess system functionality are described in [this file](test_requests).