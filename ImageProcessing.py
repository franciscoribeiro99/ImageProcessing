import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt


def read_image(image_path):
   color_image=cv2.imread(image_path)
   return cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

def write_image(image, path):
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


def embed_secret(cover_image_path, secret_text, output_path, font_path='font/font.otf', font_size=100):
    color_image = cv2.imread(cover_image_path)
    # Convert secret text to binary image (as a mask)
    secret_binary_mask = text_to_image(secret_text, color_image.shape[1], color_image.shape[0], font_path, font_size)


    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)



    # Extract the bit planes from the gray image
    bit_planes = extract_8_bit_planes(gray_image)
    biplanesHidde=extract_8_bit_planes(secret_binary_mask)

    bit_planes[0]=biplanesHidde[0]
    reconstructed_image = reconstruct_image(bit_planes)

    # Modify only the LSB where the secret text is present
    reconstructed_image_with_secret = np.where(secret_binary_mask == 1, reconstructed_image & ~1 | secret_binary_mask, reconstructed_image)

    write_image(reconstructed_image_with_secret, output_path)





def extract_secret(stego_image_path, output_path):
    stego_image = read_image(stego_image_path)
    bit_planes = extract_8_bit_planes(stego_image)
    secret_image = bit_planes[0] * 255  # Assuming LSB is the first bit-plane

    write_image(secret_image, output_path)

def text_to_image(text, width, height, font_path, font_size):
    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size=font_size)

    text_width, text_height = get_text_dimensions(text, font)
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    draw.text((x, y), text, fill=(255, 255,255), font=font)

    img = img.convert('L')

    return np.array(img)

def get_text_dimensions(text_string, font):
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return text_width, text_height




# Example Usage
embed_secret('imagesInput/image.png', 'CR7 ', 'imageWithHiddenText/ImageWithHiddenText.png')
extract_secret('imageWithHiddenText/ImageWithHiddenText.png', 'output/extractedText.png')