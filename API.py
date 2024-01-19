import json
import os

import matplotlib.pyplot as plt
from flask import Flask, request, send_file, send_from_directory
from flask import Flask, request, send_file
from flask_cors import CORS
import ImageProcessing

app = Flask(__name__)
CORS(app)

@app.route('/status', methods=['GET'])
def status():
    return '', 200

@app.route('/embed_secret', methods=['GET', 'POST'])
def embed_secret():
    # with open('embed_secret.json', 'r') as embed_file:
    #     data = json.load(embed_file)
    data = request.json
    cover_image_path = data['cover_image_path']
    print(cover_image_path)
    secret_text = data['secret_text']
    output_path = data['output_path']

    #function to embed the secret
    ImageProcessing.embed_secret(cover_image_path, secret_text, output_path)
    layer_paths = data.get('layers', [])
    for layer in layer_paths:
        send_from_directory(os.path.dirname(layer), os.path.basename(layer), as_attachment=True)

    layer_paths = 'layers'

    return '   it is  done'


@app.route('/extract_secret', methods=['GET', 'POST'])
def extract_secret():
    with open('extract_secret.json', 'r') as embed_file:
        data = json.load(embed_file)
    #data = request.json
    stego_image_path = data['stego_image_path']
    output_path = data['output_path']

    ImageProcessing.extract_secret(stego_image_path, output_path)

    send_file(output_path, as_attachment=True)


    layers = data.get('layers', [])
    for layer in layers:
        send_from_directory(os.path.dirname(layer), os.path.basename(layer), as_attachment=True)


    # Return the path of the extracted image
    return '     it is done'



if __name__ == '__main__':
    app.run(debug=True)
