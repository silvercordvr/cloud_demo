const express = require('express');
const router = express.Router();
const {createAuthHeadersFromFile} = require('./utils/webAuthorization');
const axios = require('axios');

router.get('/', (req, res) => {
  res.send('Node.js server');
});

router.post('/chat-message-ue', async (req, res) =>{

    try {

        const history = req.body.history ? req.body.history : [];
        const character = req.body.character ? req.body.character : "Assistant";
        const aiVerbose = req.body.aiVerbose ? req.body.aiVerbose : 150;

        if (!req.body.sessionId) {
        req.body.sessionId = "ue5-unknown-user";
        }
        const testPersonCard = req.body.testPersonCard;

        const response = await sendOogaChatMessage(history, character, aiVerbose, parseInt(aiVerbose) - 10, false, [], null, testPersonCard);
        let textResponse = "";

        if (response.data && response.data.choices && response.data.choices[0] && response.data.choices[0].message && response.data.choices[0].message.content) {
        textResponse = response.data.choices[0].message.content;
        }

        res.json({
            chat_response: textResponse
          });

    } catch (error) {
        console.log(`======= ERROR ======= ${error.message}`)
        res.status(500).send(error.message);
    }
  
});

async function sendOogaChatMessage(history, character, maxTokens = 150, minLength = 100, stop = false, stops = ["\n", "."], additionalContent = null, charPersona = null) {
    const context = [...history];
    if (additionalContent) {
        context.push({ role: "user", content: additionalContent });
    }

    const params = {
        "messages": context,
        "mode": "chat",
        "character": character,
        "temperature": 0.7,
        "max_tokens": maxTokens,
        "presence_penalty": 0.6,
        "frequency_penalty": 0.6,
        "no_repeat_ngram_size": 2,
        "min_length": minLength
    }

    if (stop) {
        params.stop = stops
    }

    // AUTH HEADERS (for alpha web server ONLY!)
    const headers = await createAuthHeadersFromFile();  

    const response = await axios.post("/chat", params,{headers: headers});
    return response;
}

module.exports = router;
