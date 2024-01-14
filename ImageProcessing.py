import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

def read_image(image_path):
    return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

def write_image(image, path):
    cv2.imwrite(path, image)

def convert_to_binary_image(image):
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    return binary_image

def extract_8_bit_planes(image):
    bit_planes = [np.zeros_like(image, dtype=np.uint8) for _ in range(8)]
    for i in range(8):
        bit_planes[i] = np.bitwise_and(image, 2 ** i)
        bit_planes[i] = np.right_shift(bit_planes[i], i)
    return bit_planes

def reconstruct_image(bit_planes):
    reconstructed_image = np.zeros_like(bit_planes[0], dtype=np.uint8)
    for i, plane in enumerate(bit_planes):
        reconstructed_image |= (plane << i)
    return reconstructed_image

def embed_secret(cover_image_path, secret_text, output_path, font_path='font/font.otf', font_size=100):
    cover_image = read_image(cover_image_path)
    secret_image = text_to_image(secret_text, cover_image.shape[1], cover_image.shape[0], font_path, font_size)
    secret_binary = convert_to_binary_image(secret_image)

    bit_planes = extract_8_bit_planes(cover_image)
    bit_planes[0] = secret_binary  # Assuming LSB is the first bit-plane

    stego_image = reconstruct_image(bit_planes)
    write_image(stego_image, output_path)

def extract_secret(stego_image_path, output_path):
    stego_image = read_image(stego_image_path)
    bit_planes = extract_8_bit_planes(stego_image)
    secret_image = bit_planes[0] * 255  # Assuming LSB is the first bit-plane

    write_image(secret_image, output_path)

def text_to_image(text, width, height, font_path, font_size):
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size=font_size)

    text_width, text_height = get_text_dimensions(text, font)
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    draw.text((x, y), text, fill=(0, 0, 0), font=font)
    img = img.convert('L')
    return np.array(img)

def get_text_dimensions(text_string, font):
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return text_width, text_height

# Example Usage
embed_secret('imagesInput/image.png', 'Hello ', 'imageWithHiddenText/ImageWithHiddenText.png')
#extract_secret('imageWithHiddenText/ImageWithHiddenText.png', 'extractedText.png')