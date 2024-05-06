from PIL import Image
from fastapi import HTTPException

SUPPORTED_IMAGE_FORMATS = {
    "image/png": "PNG",
    "image/jpeg": "JPEG",
}


def validate_max_dimensions(image: Image.Image, width: int, height: int):
    """Crop parameters should not exceed image dimensions"""
    if image.width >= width and image.height >= height:
        return None

    raise HTTPException(
        status_code=400,
        detail=f"Image too small for given width/height. Image dimensions: {image.width}x{image.height} - Parameters given: {width}x{height}",
    )


def validate_image_type(content_type: str):
    """Only content types found in support dictionary are valid"""
    if content_type in SUPPORTED_IMAGE_FORMATS.keys():
        return None

    raise HTTPException(
        status_code=400,
        detail=f"Content-Type '{content_type}' not supported. Supported Content-Types: {SUPPORTED_IMAGE_FORMATS.keys()}",
    )
