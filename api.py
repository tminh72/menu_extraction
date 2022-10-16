from importlib.resources import path
import json
from flask import Flask, request, json
import base64
import numpy as np
import cv2

app = Flask(__name__)

from extractor_pairs import Extractor
extractor = Extractor() 

# Health-checking method
@app.route('/healthCheck', methods=['GET'])
def health_check():
    """
    Health check the server
    Return:
    Status of the server
        "OK"
    """
    return "OK"

# Inference method
@app.route('/infer', methods=['POST'])
def infer():
    # Read data from request
    image_name = request.form.get('image_name')
    encoded_img = request.form.get('image')
    # Convert base64 back to bytes
    img_decode_byte = base64.b64decode(encoded_img)
    img = np.frombuffer(img_decode_byte,dtype=np.uint8)
    img_decode_jpeg = cv2.imdecode(img, flags=1)
    try:
        extractor.load_img(img_decode_jpeg)
        extractor.run()
        pairs = extractor.results
        response = {
            "image_name": image_name,
            "infers": []
        }
        for pair in pairs:
            dct = {
                'food_name_en': pair[1],
                'food_name_vi': pair[0],
                'food_price': pair[2],

            }
            response['infers'].append(dct)
        return json.dumps(response)
        
    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    app.run(port=5000, debug=False,host='0.0.0.0')

    