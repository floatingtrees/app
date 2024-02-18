from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/data', methods=['GET'])
def get_data():
   # Return some data
   data = {
       "message": "Hello from Flask!"
   }
   return jsonify(data)

if __name__ == '__main__':
   app.run(debug=True, port=5001, host="0.0.0.0")
