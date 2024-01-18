import unittest
import cv2
import numpy as np
import os
from PIL import ImageFont

from ImageProcessing import (read_image, write_image, extract_8_bit_planes,
                             reconstruct_image, embed_secret, extract_secret,
                             text_to_image, get_text_dimensions)

class TestImageProcessing(unittest.TestCase):

    def setUp(self):
        self.test_image_path = "imagesInput/image.png"
        self.test_output_path = "output/output.png"
        self.secret_output_path = "output/extracted.png"

    def test_read_image(self):
        image = read_image(self.test_image_path)
        self.assertIsNotNone(image)
        self.assertTrue(isinstance(image, np.ndarray))
        self.assertGreater(image.size, 0)  # Image should not be empty

    def test_write_image(self):
        image = cv2.imread(self.test_image_path, cv2.IMREAD_GRAYSCALE)
        write_image(image, self.test_output_path)
        self.assertTrue(os.path.exists(self.test_output_path))
        # Check if the written image is not empty
        written_image = cv2.imread(self.test_output_path, cv2.IMREAD_GRAYSCALE)
        self.assertIsNotNone(written_image)
        self.assertGreater(written_image.size, 0)

    def tearDown(self):
        # Tear down code, like deleting test output files
        for path in [self.test_output_path, self.secret_output_path]:
            if os.path.exists(path):
                os.remove(path)

    def test_extract_8_bit_planes(self):
        image = cv2.imread(self.test_image_path, cv2.IMREAD_GRAYSCALE)
        planes = extract_8_bit_planes(image)
        self.assertEqual(len(planes), 8)
        for plane in planes:
            self.assertTrue(isinstance(plane, np.ndarray))
            self.assertEqual(plane.shape, image.shape)
            self.assertTrue(np.any(plane))  # Check if the plane is not empty

    def test_reconstruct_image(self):
        image = cv2.imread(self.test_image_path, cv2.IMREAD_GRAYSCALE)
        planes = extract_8_bit_planes(image)
        reconstructed = reconstruct_image(planes)
        self.assertTrue(isinstance(reconstructed, np.ndarray))
        self.assertEqual(reconstructed.shape, image.shape)
        np.testing.assert_array_equal(image, reconstructed)  # Check for exact reconstruction

    def test_embed_and_extract_secret(self):
        secret_text = "Test Secret"
        embed_secret(self.test_image_path, secret_text, self.test_output_path)
        self.assertTrue(os.path.exists(self.test_output_path))

        extract_secret(self.test_output_path, self.secret_output_path)
        self.assertTrue(os.path.exists(self.secret_output_path))
        # Further tests could include checking the content of the extracted secret

    def test_text_to_image(self):
        text = "Test"
        font_path = 'font/font.otf'
        img = text_to_image(text, 100, 100, font_path, 12)
        self.assertTrue(isinstance(img, np.ndarray))
        self.assertGreater(img.size, 0)  # Check if image is not empty

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
