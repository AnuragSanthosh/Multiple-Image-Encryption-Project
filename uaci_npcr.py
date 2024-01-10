import numpy as np
from PIL import Image

def calculate_uaci(original, encrypted):
    # Convert images to numpy arrays
    original_array = np.array(original, dtype=np.float32)
    encrypted_array = np.array(encrypted, dtype=np.float32)

    # Calculate UACI
    uaci = np.sum(np.abs(original_array - encrypted_array)) / np.sum(original_array + encrypted_array)

    return uaci

def calculate_npcr(original, encrypted):
    # Convert images to numpy arrays
    original_array = np.array(original)
    encrypted_array = np.array(encrypted)

    # Calculate NPCR
    npcr = np.sum(original_array != encrypted_array) / (original_array.size * 1.0)

    return npcr


original_image = Image.open("C:/Users/ANURAG/Pictures/single sample image/sampleimage.jpeg")
encrypted_image = Image.open("enc_0.png")


if original_image.size != encrypted_image.size:
    raise ValueError("Original and encrypted images must have the same dimensions.")


uaci_value = calculate_uaci(original_image, encrypted_image)
print(f"UACI: {uaci_value}")


npcr_value = calculate_npcr(original_image, encrypted_image)
print(f"NPCR: {npcr_value}")
