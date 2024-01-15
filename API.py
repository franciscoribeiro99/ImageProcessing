from flask import Flask, request, send_file
import ImageProcessing

app = Flask(__name__)


@app.route('/embed_secret', methods=['POST'])
def embed_secret():
    data = request.json
    cover_image_path = data['cover_image_path']
    secret_text = data['secret_text']
    output_path = data['output_path']

    #function to embed the secret
    ImageProcessing.embed_secret(cover_image_path, secret_text, output_path)

    # Return the path of the modified image
    return send_file(output_path, as_attachment=True)


@app.route('/extract_secret', methods=['POST'])
def extract_secret():
    data = request.json
    stego_image_path = data['stego_image_path']
    output_path = data['output_path']

    #function to exract the secret
    ImageProcessing.extract_secret(stego_image_path, output_path)

    # Return the path of the extracted image
    return send_file(output_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
