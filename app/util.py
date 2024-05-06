import imagehash
from PIL import Image


def center_crop(image: Image.Image, width: int, height: int) -> Image.Image:
    """Crops the image to center and resize to width x height"""
    left = (image.width - width) / 2
    top = (image.height - height) / 2

    crop_box = (left, top, left + width, top + height)

    return image.crop(crop_box)


def calculate_hamming_distance(image_a: Image.Image, image_b: Image.Image) -> int:
    """Calculate the hamming distance between two images"""
    return imagehash.dhash(image_a) - imagehash.dhash(image_b)
