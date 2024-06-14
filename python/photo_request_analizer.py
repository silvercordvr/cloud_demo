from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")

def analyze_photo_request(text):
    doc = nlp(text)
    photo_keywords = ["picture", "pictures", "photo", "photos", "image", "images", "show"]

    is_photo_request = False
    subjects = []
    found_negations = False

    for token in doc:
        if token.dep_ == "neg":
            found_negations = True
            break

    if not found_negations:
        for token in doc:
            if token.text.lower() in photo_keywords:
                is_photo_request = True
                subjects = [child.text for child in token.subtree if child.pos_ in ["NOUN", "PROPN"] and child.text.lower() not in photo_keywords]
                break

    return is_photo_request, subjects

@app.route('/photo-analyze', methods=['POST'])
def analyze():
    data = request.json
    input_text = data.get('text')

    is_photo_request, subjects = analyze_photo_request(input_text)

    result = {
        "is_photo_request": is_photo_request,
        "subjects": subjects
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
