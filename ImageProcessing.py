import os
import textwrap

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
    """
    Extracts 8-bit planes from a grayscale image.

    Parameters:
    gray_image (numpy.ndarray): Input grayscale image.

    Returns:
    list: A list of 8 numpy arrays, each representing a bit plane of the input image.
    """
    bit_planes = [np.zeros_like(gray_image) for _ in range(8)]
    for i in range(8):
        bit_planes[i] = np.bitwise_and(gray_image, 2 ** i)
        bit_planes[i] = np.right_shift(bit_planes[i], i)

    return bit_planes


def reconstruct_image(bit_planes):
    """
        Reconstructs an image from its 8-bit planes.

        Parameters:
        bit_planes (list): A list of 8 numpy arrays, each representing a bit plane of an image.

        Returns:
        numpy.ndarray: Reconstructed image from the bit planes.
        """
    reconstructed_image = np.zeros_like(bit_planes[0])
    for i, plane in enumerate(bit_planes):
        reconstructed_image |= (plane << i)
    return reconstructed_image


def embed_secret(cover_image_path, secret_text, output_path, font_path='font/font.otf', font_size=100):
    """
      Embeds secret text into the least significant bit plane of a cover image.

      Parameters:
      cover_image_path (str): Path to the cover image.
      secret_text (str): Text to be embedded.
      output_path (str): Path to save the image with embedded text.
      font_path (str, optional): Path to the font file. Defaults to 'font/font.otf'.
      font_size (int, optional): Font size for rendering the text. Defaults to 100.
      """
    color_image = cv2.imread(cover_image_path)
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
    """
        Extracts secret text from the least significant bit plane of a stego image.

        Parameters:
        stego_image_path (str): Path to the stego image.
        output_path (str): Path to save the extracted secret text as an image.
        """
    stego_image = read_image(stego_image_path)
    bit_planes = extract_8_bit_planes(stego_image)
    secret_image = bit_planes[0] * 255  # Assuming LSB is the first bit-plane
    display_bit_planes(bit_planes)
    write_image(secret_image, output_path)

def text_to_image(text, width, height, font_path, font_size):
    """
        Converts text to a binary image.

        Parameters:
        text (str): Text to be converted.
        width (int): Width of the output image.
        height (int): Height of the output image.
        font_path (str): Path to the font file.
        font_size (int): Font size for rendering the text.

        Returns:
        numpy.ndarray: Binary image representing the input text.
        """
    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size=font_size)
    max_chars_per_line = (width // (font_size // 2))-15
    lines = textwrap.wrap(text, width=max_chars_per_line)

    total_text_height = sum(draw.textbbox((0, 0), line, font=font, anchor='mm')[3] for line in lines)

    y = (height - total_text_height) // 2

    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font, anchor='mm')
        text_height = text_bbox[3] - text_bbox[1]
        draw.text((width//2, y), line, fill=(255, 255, 255), font=font, anchor='mm')
        y += text_height


    img = img.convert('L')

    return np.array(img)

def get_text_dimensions(text_string, font):
    """
       Calculates the dimensions of a text string when rendered in a given font.

       Parameters:
       text_string (str): Text whose dimensions are to be calculated.
       font (ImageFont): Font used for rendering the text.

       Returns:
       tuple: Width and height of the rendered text.
       """
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return text_width, text_height

def display_bit_planes(bit_planes):
    """
       Displays and saves the 8-bit planes of an image.

       Parameters:
       bit_planes (list): A list of 8 numpy arrays, each representing a bit plane of an image.
       """
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
