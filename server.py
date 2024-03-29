from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from PIL import Image
import FGSM, generate
import base64
import torch

global primary
global desired_class_2



model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
model.eval()
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
   if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
   file = request.files['file']
   # If user does not select file, browser also
   # submit an empty part without filename
   if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
   if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(save_path)
      try:
         wanted_class = desired_class_2
      except:
         wanted_class = None
      old_category, new_category = generate.generate(model, save_path, label = None, string_label = wanted_class)

      image_path = 'uploads/image.png'
    # Ensure the image path is correct and accessible
    
      with open(image_path, "rb") as image_file:
         encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
         primary = {'message': 'File uploaded successfully', 'image': encoded_string, "old_category" : old_category, "new_category" : new_category}
      return jsonify(primary), 200

   return jsonify({'message': 'File type not allowed'}), 400

@app.route('/send-classes', methods=['POST'])
def recieve_class():
   desired_class = request.data.decode('utf-8')
   print(desired_class)
   global desired_class_2
   desired_class_2 = desired_class
   return jsonify("Placeholder"), 200

if __name__ == '__main__':
   app.run(debug=True, port=5001, host="0.0.0.0")
