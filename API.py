import json
import os

import matplotlib.pyplot as plt
from flask import Flask, request, send_file, send_from_directory, jsonify
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
    data = request.json
    # with open('embed_secret.json', 'r') as embed_file:
    #     data = json.load(embed_file)

    cover_image_base64 = data['cover_image_path']
    secret_text = data['secret_text']
    output_path = 'imageWithHiddenText/ImageWithHiddenText.png'
    imm_array = ImageProcessing.base64_to_image(cover_image_base64)
    ImageProcessing.write_image(imm_array, 'imagesInput/image.png')

    ImageProcessing.embed_secret('imagesInput/image.png', secret_text, output_path)
    read_img_arr= ImageProcessing.read_image(output_path)
    base64_extracted_image = ImageProcessing.image_to_base64(read_img_arr)

    # layer_folder = 'layers'
    # list_layer_base64 = []

    # for filename in os.listdir(layer_folder):
    #     layer_path = os.path.join(layer_folder, filename)
    #     list_layer_base64.append(ImageProcessing.image_to_base64(ImageProcessing.read_image(layer_path)))

    # return jsonify({'status': 'done', 'extracted_image': base64_extracted_image, 'layers': list_layer_base64})
    return jsonify({'status': 'done', 'extracted_image': base64_extracted_image})


@app.route('/extract_secret', methods=['GET', 'POST'])
def extract_secret():
    # with open('extract_secret.json', 'r') as embed_file:
    #     data = json.load(embed_file)
    data = request.json
    stego_image = data['stego_image_path']
    output_path = 'output/extractedText.png'

    imm_array = ImageProcessing.base64_to_image(stego_image)
    ImageProcessing.write_image(imm_array, 'imageWithHiddenText/ImageWithHiddenText.png')
    ImageProcessing.extract_secret('imageWithHiddenText/ImageWithHiddenText.png', output_path)
    read_image_arr = ImageProcessing.read_image(output_path)
    base64_extracted_image = ImageProcessing.image_to_base64(read_image_arr)

    layer_folder = 'layers'
    list_layer_base64 = []

    for filename in os.listdir(layer_folder):
        layer_path = os.path.join(layer_folder, filename)
        list_layer_base64.append(ImageProcessing.image_to_base64(ImageProcessing.read_image(layer_path)))


    return  jsonify({'status': 'done', 'extracted_image': base64_extracted_image, 'layers': list_layer_base64})



if __name__ == '__main__':
    app.run(debug=True)
