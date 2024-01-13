import unittest
import cv2
import numpy as np
import os
from PIL import ImageFont

from ImageProcessing import read_image, write_image, convert_to_binary_image, extract_8_bit_planes, reconstruct_image, embed_secret, extract_secret, text_to_image, get_text_dimensions

class TestImageProcessing(unittest.TestCase):

    def setUp(self):
        self.test_image_path = "images/ImageTesting.png"
        self.test_output_path = "output/output.png"

    def test_read_image(self):
        image = read_image(self.test_image_path)
        self.assertIsNotNone(image)
        self.assertTrue(isinstance(image, np.ndarray))

    def test_write_image(self):
        image = cv2.imread(self.test_image_path, cv2.IMREAD_GRAYSCALE)
        write_image(image, self.test_output_path)
        self.assertTrue(os.path.exists(self.test_output_path))

    def test_convert_to_binary_image(self):
        image = cv2.imread(self.test_image_path, cv2.IMREAD_GRAYSCALE)
        binary_image = convert_to_binary_image(image)
        self.assertTrue(isinstance(binary_image, np.ndarray))
        # Checking if the conversion is binary (i.e., only contains 0s and 255s)
        unique_values = np.unique(binary_image)
        self.assertTrue(np.array_equal(unique_values, [0, 255]))

    def tearDown(self):
        # Tear down code, like deleting test output files
        if os.path.exists(self.test_output_path):
            os.remove(self.test_output_path)

    def test_extract_8_bit_planes(self):
        image = cv2.imread(self.test_image_path, cv2.IMREAD_GRAYSCALE)
        planes = extract_8_bit_planes(image)
        self.assertEqual(len(planes), 8)
        for plane in planes:
            self.assertTrue(isinstance(plane, np.ndarray))
            self.assertEqual(plane.shape, image.shape)

    def test_reconstruct_image(self):
        image = cv2.imread(self.test_image_path, cv2.IMREAD_GRAYSCALE)
        planes = extract_8_bit_planes(image)
        reconstructed = reconstruct_image(planes)
        self.assertTrue(isinstance(reconstructed, np.ndarray))
        self.assertEqual(reconstructed.shape, image.shape)
        # Optionally, compare reconstructed image with original image

    def test_embed_and_extract_secret(self):
        secret_text = "Test Secret"
        embed_secret(self.test_image_path, secret_text, self.test_output_path)
        self.assertTrue(os.path.exists(self.test_output_path))

        extract_secret(self.test_output_path, 'output/extracted.png')
        self.assertTrue(os.path.exists('output/extracted.png'))
        # Optionally, verify the extracted secret

    def test_text_to_image(self):
        text = "Test"
        font_path = 'font/font.otf'
        img = text_to_image(text, 100, 100, font_path, 12)
        self.assertTrue(isinstance(img, np.ndarray))

    def test_get_text_dimensions(self):
        font_path = 'font/font.otf'
        font = ImageFont.truetype(font_path, size=12)
        width, height = get_text_dimensions("Test", font)
        self.assertIsInstance(width, int)
        self.assertIsInstance(height, int)
        self.assertGreater(width, 0)
        self.assertGreater(height, 0)

if __name__ == '__main__':
    unittest.main()
