import os
import tempfile
import hashlib

from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from PIL import Image

from app.validators import validate_image_type, validate_max_dimensions
from app.util import center_crop, calculate_hamming_distance

api = FastAPI()


DEFAULT_ERROR_MSG = "There was a problem processing the image."

DHASH_VARIATION_CUTOFF = 10


@api.get("/")
def root():
    return {"info": "Welcome to image api service"}


@api.post("/crop")
def crop(image_file: UploadFile, width: int, height: int, bg_tasks: BackgroundTasks):
    """Crop to the center of an image, given width and height"""
    try:
        validate_image_type(image_file.content_type)

        suffix = image_file.filename.split(".")[-1]
        image = Image.open(image_file.file)

        validate_max_dimensions(image, width, height)

        cropped_image = center_crop(image, width, height)

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}")
        bg_tasks.add_task(os.unlink, tmp.name)

        cropped_image.save(tmp, format=image.format)
        tmp.close()

        return FileResponse(
            tmp.name, filename=image_file.filename, media_type=image_file.content_type
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail=DEFAULT_ERROR_MSG)
    finally:
        image_file.file.close()


@api.post("/difference")
def difference(image_a: UploadFile, image_b: UploadFile):
    """Calculate a difference score between two images.

    Values in the range of 0-1 can be considered variations in an image.
    Anything above 1, is considered a different image.
    """
    try:
        return {
            "score": calculate_hamming_distance(
                Image.open(image_a.file), Image.open(image_b.file)
            )
            / DHASH_VARIATION_CUTOFF
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail=DEFAULT_ERROR_MSG)
    finally:
        image_a.file.close()
        image_b.file.close()


@api.post("/hash")
def hash(image_file: UploadFile):
    """Calculate the sha256 hash of an image"""
    try:
        return {"sha256": hashlib.file_digest(image_file.file, "sha256").hexdigest()}
    except Exception:
        raise HTTPException(status_code=500, detail=DEFAULT_ERROR_MSG)
    finally:
        image_file.file.close()
