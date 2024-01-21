import base64
import io
import os
import textwrap

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
from six import BytesIO


def image_to_base64(image_array):
    pil_image = Image.fromarray(image_array)

    image_stream = io.BytesIO()

    pil_image.save(image_stream, format='PNG')

    base64_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return base64_image
def base64_to_image(base64_string):
    base64_string = str(base64_string)
    padded_base64_string = base64_string + '=' * (4 - len(base64_string) % 4)

    binary_data = base64.b64decode(padded_base64_string)
    image_stream = BytesIO(binary_data)

    pil_image = Image.open(image_stream)
    image_array = np.array(pil_image)

    return image_array


def read_image(image_path):
   color_image=cv2.imread(image_path)
   return cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

def write_image(image, path):
    #imm_arr = base64_to_image(image)

    cv2.imwrite(path, image)

def extract_8_bit_planes(gray_image):
    bit_planes = [np.zeros_like(gray_image) for _ in range(8)]
    for i in range(8):
        bit_planes[i] = np.bitwise_and(gray_image, 2 ** i)
        bit_planes[i] = np.right_shift(bit_planes[i], i)

    return bit_planes


def reconstruct_image(bit_planes):
    reconstructed_image = np.zeros_like(bit_planes[0])
    for i, plane in enumerate(bit_planes):
        reconstructed_image |= (plane << i)
    return reconstructed_image


def embed_secret(cover_path_image, secret_text, output_path, font_path='font/font.ttf', font_size=20):
    color_image = cv2.imread(cover_path_image)
    #print(type(color_image))
    # Convert secret text to binary image (as a mask)
    secret_binary_mask = text_to_image(secret_text, color_image.shape[1], color_image.shape[0], font_path, font_size)


    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)



    # Extract the bit planes from the gray image
    bit_planes = extract_8_bit_planes(gray_image)
    biplanesHidde=extract_8_bit_planes(secret_binary_mask)

    bit_planes[0]=biplanesHidde[0]
    reconstructed_image = reconstruct_image(bit_planes)
    display_bit_planes(bit_planes)
    # Modify only the LSB where the secret text is present
    reconstructed_image_with_secret = np.where(secret_binary_mask == 1, reconstructed_image & ~1 | secret_binary_mask, reconstructed_image)

    write_image(reconstructed_image_with_secret, output_path)



def extract_secret(stego_image_path, output_path):
    stego_image = read_image(stego_image_path)
    bit_planes = extract_8_bit_planes(stego_image)
    secret_image = bit_planes[0] * 255  # Assuming LSB is the first bit-plane
    display_bit_planes(bit_planes)
    write_image(secret_image, output_path)


def text_to_image(text, width, height, font_path, min_font_size=10, max_font_size=50):
    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    max_text_width, max_text_height = get_text_dimensions('W' * len(text),
                                                          ImageFont.truetype(font_path, size=max_font_size))

    font_size = max(min(max_font_size, (width / max_text_width) * max_font_size), min_font_size)

    font = ImageFont.truetype(font_path, size=int(font_size))
    max_chars_per_line = (width // (font_size // 2)) - 5
    lines = textwrap.wrap(text, width=max_chars_per_line)

    total_text_height = sum(draw.textbbox((0, 0), line, font=font, anchor='mm')[3] for line in lines)

    y = (height - total_text_height) // 2

    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font, anchor='mm')
        text_height = text_bbox[3] - text_bbox[1]
        draw.text((width // 2, y), line, fill=(255, 255, 255), font=font, anchor='mm')
        y += text_height

    img = img.convert('L')

    return np.array(img)

def get_text_dimensions(text_string, font):
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return text_width, text_height

def display_bit_planes(bit_planes):
    plt.figure(figsize=(10, 8))
    for i in range(8):
        plt.subplot(2, 4, i+1)
        plt.imshow(bit_planes[i], cmap='gray')
        plt.title(f'Bit Plane {i}')
        plt.axis('off')
        plt.imsave(f'layers/layer_{i}.png', bit_planes[i], format='png')
    plt.tight_layout()


# Example Usage
#embed_secret('imagesInput/image.png', 'Hi', 'imageWithHiddenText/ImageWithHiddenText.png')
#extract_secret('imageWithHiddenText/ImageWithHiddenText.png', 'output/extractedText.png')
