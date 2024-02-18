from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from PIL import Image


app = Flask(__name__)
CORS(app)

@app.route('/data', methods=['GET'])
def get_data():
   # Return some data
   data = {
       "message": "Hello from Flask!"
   }
   return jsonify(data)


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    print(request.files)
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 401
    file = request.files['file']
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 402
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        return jsonify({'message': 'File uploaded successfully', 'path': save_path}), 200

    return jsonify({'message': 'File type not allowed'}), 403


if __name__ == '__main__':
   app.run(debug=True, port=5001, host="0.0.0.0")
