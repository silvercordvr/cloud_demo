## Test Request Descriptions for Server Verification

To ensure the server is functioning correctly, please perform the following test requests. These tests will verify the server's response to authentication and data handling.

### 1. Echo POST Request

#### 1.1. Echo POST Request with Correct Credentials

**Request Method:** POST  
**Endpoint:** `{https://server_address}/echo-post`  
**Headers:**
- Authorization: Basic (Base64 encoded `Username:Password`, i.e., `admin:password123`)
- Content-Type: application/json

**Body:**
```json
{
    "data": "test"
}
```

**Expected Response:**
- **Status Code:** 200 OK
- **Response Body:**
    ```json
    {
        "received_data": {
            "data": "test"
        }
    }
    ```

#### 1.2 Echo POST Request with Incorrect Credentials

**Request Method:** POST  
**Endpoint:** `{https://server_address}/echo-post`  
**Headers:**
- Authorization: Basic (Base64 encoded `Username:Password`, i.e., `admin1:password123`)
- Content-Type: application/json

**Body:**
```json
{
    "data": "test"
}
```

**Expected Response:**
- **Status Code:** 401 Unauthorized
- **Response Body:**
    ```json
    {
        "error": "Unauthorized"
    }
    ```

### Detailed Steps

#### 1.3. Preparing the Authorization Header

To create the Basic Auth header, you need to base64 encode the string `Username:Password`. For example:

- For `Username: admin` and `Password: password123`, the string `admin:password123` is base64 encoded to `YWRtaW46cGFzc3dvcmQxMjM=`.
- For `Username: admin1` and `Password: password123`, the string `admin1:password123` is base64 encoded to `YWRtaW4xOnBhc3N3b3JkMTIz`.

You can use any base64 encoding tool or library to achieve this.

#### 1.4. Performing the Test Requests

**Correct Credentials Example (cURL):**
```sh
curl -X POST {https://server_address}/echo-post \
     -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     -H "Content-Type: application/json" \
     -d '{"data": "test"}'
```

**Incorrect Credentials Example (cURL):**
```sh
curl -X POST {https://server_address}/echo-post \
     -H "Authorization: Basic YWRtaW4xOnBhc3N3b3JkMTIz=" \
     -H "Content-Type: application/json" \
     -d '{"data": "test"}'
```

Here's a detailed description of the test request for obtaining a text response from the chat-bot, including both the request and the expected response:

### 2. Test Request for Chat-Bot Response

#### 2.1. Request Description

**Method**: POST  
**URL**: `{https://server_address}/chat-message-ue`  
**Headers**: 
- `Authorization`: Basic Auth (Username: `admin`, Password: `password123`)  

**Body**: (raw JSON)
```json
{
    "history": [
        {
            "role": "user",
            "content": "Hi. Who are you?"
        }
    ],
    "character": "Assistant",
    "aiVerbose": 30
}
```

#### 2.2. Expected Response

**Status Code**: 200  
**Body**: (raw JSON)
```json
{
    "chat_response": "I am an advanced artificial intelligence model designed for assistance and problem-solving. My purpose is to provide helpful information, make recommendations,"
}
```

### 3. Test Request for Uploading WAV File and Processing It (STT)

#### 3.1. Request Description

**Method**: POST  
**URL**: `{https://server_address}/upload-wav`  
**Headers**:
- `Authorization`: Basic Auth (Username: `admin`, Password: `password123`)
- `User-ID`: `12345`

**Body**: (raw binary data, representing the WAV file)
- Example file: [link_to_file](../test_files/xtts_v2_sample_Aaron_Dreschner.wav)

#### 3.2. Expected Response

**Status Code**: 200  
**Body**: (raw JSON)
```json
{
    "text": "Hi, this is a sample of my voice. I hope you like it."
}
```

#### 3.3. Error Handling

**Missing User-ID Header**:
- **Status Code**: 400  
- **Body**: (raw JSON)
```json
{
    "error": "User-ID header is missing"
}
```

**No Data Received**:
- **Status Code**: 400  
- **Body**: (raw JSON)
```json
{
    "error": "No data received"
}
```

**Unauthorized Request**:
- **Status Code**: 401  
- **Body**: (raw JSON)
```json
{
    "error": "Unauthorized"
}
```

### 4. Test Request for Photo Analysis Endpoint

#### 4.1. Request Description

**Method**: POST  
**URL**: `{https://server_address}/photo-analyze`  
**Headers**:
- `Authorization`: Basic Auth (Username: `admin`, Password: `password123`)

**Body**: (raw JSON)
- Example 1:
  ```json
  {
      "text": "Hello there!"
  }
  ```
- Example 2:
  ```json
  {
      "text": "Show me a photo of your cat"
  }
  ```

#### 4.2. Expected Response

**Example 1**:
- **Status Code**: 200  
- **Body**: (raw JSON)
  ```json
  {
      "is_photo_request": false,
      "subjects": []
  }
  ```

**Example 2**:
- **Status Code**: 200  
- **Body**: (raw JSON)
  ```json
  {
      "is_photo_request": true,
      "subjects": [
          "cat"
      ]
  }
  ```

#### 4.3. Error Handling

**Unauthorized Request**:
- **Status Code**: 401  
- **Body**: (raw JSON)
  ```json
  {
      "error": "Unauthorized"
  }
  ```

### 5. Test Request for TTS Endpoint

#### 5.1. Request Description

**Method**: POST  
**URL**: `{https://server_address}/tts`  
**Headers**:
- `Authorization`: Basic Auth (Username: `admin`, Password: `password123`)

**Body**: (raw JSON)
```json
{
    "text": "Hey! I want to hear your voice.",
    "filename": "12345/assistant/test.wav",
    "model_name": "tts_models/multilingual/multi-dataset/xtts_v2:Aaron Dreschner"
}
```

#### 5.2. Expected Response

**Status Code**: 200  
**Body**: (raw JSON)
```json
{
    "message": "File generated successfully",
    "path": "12345/assistant/test.wav"
}
```

**Result**: The file `test.wav` should be created in the "./tts/12345/assistant/" folder and be accessible via the URL: `{https://server_address}/audio/12345/assistant/test.wav`.

#### 5.3. Error Handling

**Unauthorized Request**:
- **Status Code**: 401  
- **Body**: (raw JSON)
  ```json
  {
      "error": "Unauthorized"
  }
  ```

### 6. Test Request for Deleting Audio File Endpoint

#### 6.1. Request Description

**Method**: DELETE  
**URL**: `{https://server_address}/tts-delete?session=12345&character=assistant&filename=test.wav`  
**Headers**:
- `Authorization`: Basic Auth (Username: `admin`, Password: `password123`)

#### 6.2. Expected Response

**Status Code**: 200  
**Body**: (raw JSON)
```json
{
    "message": "WAV file deleted successfully"
}
```

**Result**: The file `test.wav` should be deleted from the directory `./tts/12345/assistant`.

#### 6.3. Error Handling

**Missing Parameters**:
- **Status Code**: 400  
- **Body**: (raw JSON)
  ```json
  {
      "error": "All parameters (session, character, filename) are required"
  }
  ```

**Unauthorized Request**:
- **Status Code**: 401  
- **Body**: (raw JSON)
  ```json
  {
      "error": "Unauthorized"
  }
  ```