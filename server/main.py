# pretty much this whole webserver was made with my local AI model
# i wish i had the patience to learn how to make one but im not doing ts

#no multithreading since we only have 1 gpu anyways lol

from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

import imageRecognition

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
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
    output = imageRecognition.describeImageFromServer("uploads/" + filename)
    
    # TODO: return text output
    return jsonify({
        "message": "Image received!",
        "text": output,
        "prompt": prompt
    }), 200

def run():
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    run()

