# pretty much this whole webserver was made with my local AI model
# i wish i had the patience to learn how to make one but im not doing ts

#no multithreading since we only have 1 gpu anyways lol

from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

import imageRecognition
import ollama

app = Flask(__name__)
UPLOAD_FOLDER = 'server/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part", "file": request.files}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    prompt = None
    if 'prompt' not in request.files:
        prompt = 0
    else:
        prompt = request.files["prompt"]
    
    
    # Save the image (you can process it here later)
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    print(len(ollama.list().model_dump()))
    if (prompt == 0):
        output = imageRecognition.describeImageFromServer(UPLOAD_FOLDER + "/" + filename)
    else:
        output = imageRecognition.extractTextFromServer(UPLOAD_FOLDER + "/" + filename)

    if (output == False):
        return jsonify({
        "error": "Image received, model failure",
        "prompt": f"prompt: {prompt}"
    }), 400
    
    return jsonify({
        "message": "Image received!",
        "text": output,
        "prompt": prompt
    }), 200

def run():
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    run()

