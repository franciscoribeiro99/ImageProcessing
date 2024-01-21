import json
import os

import matplotlib.pyplot as plt
from flask import Flask, request, send_file, send_from_directory, jsonify
from flask import Flask, request, send_file
from flask_cors import CORS

import ImageProcessing

app = Flask(__name__)
CORS(app)


# Endpoint to check the status of the server
@app.route('/status', methods=['GET'])
def status():
    return '', 200


@app.route('/embed_secret', methods=['GET', 'POST'])
def embed_secret():
    '''Endpoint to embed a secret in an image'''
    # Read data from the 'embed_secret.json' file
    with open('embed_secret.json', 'r') as embed_file:
        data = json.load(embed_file)

    # Extract relevant information from the JSON data
    cover_image_base64 = data['cover_image_path']
    secret_text = data['secret_text']
    output_path = 'imageWithHiddenText/ImageWithHiddenText.png'

    # Convert base64-encoded image to NumPy array
    imm_array = ImageProcessing.base64_to_image(cover_image_base64)
    # Write the image to a file
    ImageProcessing.write_image(imm_array, 'imagesInput/image.png')

    # Embed the secret text in the image
    ImageProcessing.embed_secret('imagesInput/image.png', secret_text, output_path)

    # Read the resulting image array
    read_img_arr = ImageProcessing.read_image(output_path)
    # Convert the image array to base64
    base64_extracted_image = ImageProcessing.image_to_base64(read_img_arr)

    # Collect base64 representations of image layers in a list
    layer_folder = 'layers'
    list_layer_base64 = []
    for filename in os.listdir(layer_folder):
        layer_path = os.path.join(layer_folder, filename)
        list_layer_base64.append(ImageProcessing.image_to_base64(ImageProcessing.read_image(layer_path)))

    return jsonify({'status': 'done', 'extracted_image': base64_extracted_image, 'layers': list_layer_base64})



@app.route('/extract_secret', methods=['GET', 'POST'])
def extract_secret():
    '''Endpoint to extract a secret from a image'''
    # Extract data from the incoming JSON request
    data = request.json
    stego_image = data['stego_image_path']
    output_path = 'output/extractedText.png'

    # Convert base64-encoded image to NumPy array
    imm_array = ImageProcessing.base64_to_image(stego_image)
    # Write the image to a file
    ImageProcessing.write_image(imm_array, 'imageWithHiddenText/ImageWithHiddenText.png')

    # Extract the secret text from the steganographic image
    ImageProcessing.extract_secret('imageWithHiddenText/ImageWithHiddenText.png', output_path)

    # Read the resulting image array
    read_image_arr = ImageProcessing.read_image(output_path)
    # Convert the image array to base64
    base64_extracted_image = ImageProcessing.image_to_base64(read_image_arr)

    # Collect base64 representations of image layers in a list
    layer_folder = 'layers'
    list_layer_base64 = []
    for filename in os.listdir(layer_folder):
        layer_path = os.path.join(layer_folder, filename)
        list_layer_base64.append(ImageProcessing.image_to_base64(ImageProcessing.read_image(layer_path)))

    return jsonify({'status': 'done', 'extracted_image': base64_extracted_image, 'layers': list_layer_base64})


if __name__ == '__main__':
    app.run(debug=True)
