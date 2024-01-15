import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_and_convert_to_grayscale(image_path):
    # Load an image and convert to grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return image

def extract_bit_planes(image):
    # Extract 8-bit planes from the grayscale image
    bit_planes = []
    for i in range(8):
        bit_planes.append((image >> i) & 1)
    return bit_planes

def reconstruct_image(bit_planes):
    # Reconstruct the image from bit planes
    reconstructed = np.zeros_like(bit_planes[0], dtype=np.uint8)
    for i, bit_plane in enumerate(bit_planes):
        reconstructed += (bit_plane << i)
    return reconstructed

target_image = load_and_convert_to_grayscale('imagesInput/image.png')
image_to_insert = load_and_convert_to_grayscale('imageWithHiddenText/ImageWithHiddenText.png')

# Resize image_to_insert to match target_image's size
image_to_insert = cv2.resize(image_to_insert, (target_image.shape[1], target_image.shape[0]))

# Extract bit planes
target_bit_planes = extract_bit_planes(target_image)
insert_bit_planes = extract_bit_planes(image_to_insert)

# Replace least significant bit-plane of target with that of image_to_insert
target_bit_planes[0] = insert_bit_planes[0]

# Reconstruct the modified image
modified_image = reconstruct_image(target_bit_planes)

# Plotting
plt.figure(figsize=(12, 6))
for i in range(8):
    plt.subplot(2, 5, i + 1)
    plt.imshow(target_bit_planes[i], cmap='gray')
    plt.title(f'Bit-Plane {i}')

plt.subplot(2, 5, 10)
plt.imshow(modified_image, cmap='gray')
plt.title('embedded Secret')
plt.show()
