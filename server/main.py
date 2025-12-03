# a lot of the webserver code here was generated from QWEN3
# theres a lot of modifcations made by us here, though

# webserver libraries
from flask import Flask, request, jsonify
import os

# !!!!custom image recognition python file!!!!
# to see the code, navigate to server/imageRecognition.py
import imageRecognition

# main flask app instance
app = Flask(__name__)
# create upload dir for storing uploaded images
UPLOAD_FOLDER = 'server/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# tie specific URL to a function that handles POST requests to upload images
@app.route('/upload', methods=['POST'])
def upload_image():
    # check if the post request has the file part
    if 'image' not in request.files:
        return jsonify({"error": "No image part", "file": request.files}), 400
    
    # if theres an image part, check it has a name.
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # (not written by ai!)
    # make sure theres a prompt in the request header.
    # if not, default to the first prompt
    prompt = None
    if 'prompt' not in request.headers:
        prompt = 0
    else:
        prompt = request.headers["prompt"]

    
    
    # Save the image to the upload folder
    # this overwrites the old image on the server, if present (if they're the same name)
    filename = file.filename + "." + request.headers["imgFormat"]
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    #debug
    print(request.headers["prompt"])
    
    #get AI description based on prompt from request header
    if (prompt == "1"):
        #get distance from request header. noot used and never fed to the AI
        dist = request.headers["dist"] 
        output = imageRecognition.describeObjectFromServer(UPLOAD_FOLDER + "/" + filename, dist) #ultrasonic (1 press)
    elif (prompt == "2"):
        output = imageRecognition.extractTextFromServer(UPLOAD_FOLDER + "/" + filename) # text extraction (2 presses)
    else:
        output = imageRecognition.describeImageFromServer(UPLOAD_FOLDER + "/" + filename) # detailed description (3 presses)

    #in case ollama (what we use for AI hosting) fails
    if (output == False):
        return jsonify({
        "error": "Image received, model failure",
        "prompt": f"prompt: {prompt}"
    }), 400
    
    # return the response
    return jsonify({
        "message": "Image received!",
        "text": output,
        "prompt": prompt
    }), 200

# start the webserver
def run():
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    run()

