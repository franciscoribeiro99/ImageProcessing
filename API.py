import os

from flask import Flask, request, send_file, send_from_directory
import ImageProcessing

app = Flask(__name__)


@app.route('/embed_secret', methods=['GET', 'POST'])
def embed_secret():
    data = request.json
    cover_image_path = data['cover_image_path']
    secret_text = data['secret_text']
    output_path = data['output_path']

    #function to embed the secret
    ImageProcessing.embed_secret(cover_image_path, secret_text, output_path)
    layer_paths = data.get('layers', [])
    for layer in layer_paths:
        send_from_directory(os.path.dirname(layer), os.path.basename(layer), as_attachment=True)

    layer_paths = 'layers'
    for layer in layer_paths:
        os.remove(f'{layer_paths}/{layer}')
    os.remove('output/extractedText.png')
    os.remove('imageWithHiddenText/extractedText.png')
    os.remove('imagesInput/image.png')
    # Return the path of the modified image
    return 'done'


@app.route('/extract_secret', methods=['GET', 'POST'])
def extract_secret():
    data = request.json
    stego_image_path = data['stego_image_path']
    output_path = data['output_path']

    ImageProcessing.extract_secret(stego_image_path, output_path)

    send_file(output_path, as_attachment=True)


    layers = data.get('layers', [])
    for layer in layers:
        send_from_directory(os.path.dirname(layer), os.path.basename(layer), as_attachment=True)

    layer_paths = 'layers'
    for layer in layer_paths:
        os.remove(f'{layer_paths}/{layer}')
    os.remove('output/extractedText.png')
    os.remove('imageWithHiddenText/extractedText.png')
    os.remove('imagesInput/image.png')
    # Return the path of the extracted image
    return 'done'



if __name__ == '__main__':
    app.run(debug=True)
