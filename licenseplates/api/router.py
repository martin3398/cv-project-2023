import io

import cv2
import numpy as np
from fastapi import APIRouter, File, UploadFile
from PIL import Image
from starlette.responses import StreamingResponse

from licenseplates.model import boundingbox, lpmodel

router = APIRouter()


@router.get("/ping")
def ping():
    return {"ping": "pong"}


def load_image(file: UploadFile) -> np.ndarray:
    img = Image.open(io.BytesIO(file.file.read()))
    img = np.array(img)

    return img


def stream_result_img(img: np.ndarray) -> StreamingResponse:
    res, im_png = cv2.imencode(".png", img)

    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")


@router.post("/plot-bounding-box")
async def plot_bounding_box(file: UploadFile = File(...)):
    img = load_image(file)
    img = lpmodel.get_image_with_bounding_box(img)

    return stream_result_img(img)


@router.post("/crop-bounding-box")
async def crop_bounding_box(file: UploadFile = File(...)):
    img = load_image(file)
    img = lpmodel.get_cropped_image(img)

    return stream_result_img(img)


@router.post("/transform")
async def transform(file: UploadFile = File(...)):
    img = load_image(file)
    img = lpmodel.get_transformed_img(img)

    return stream_result_img(img)


@router.post("/preprocessing-steps")
async def preprocessing_steps(file: UploadFile = File(...)):
    img = load_image(file)
    img = lpmodel.get_preprocessed_image_steps(img)

    return stream_result_img(np.array(img))


@router.post("/read-text")
async def read_text(file: UploadFile = File(...)):
    img = load_image(file)
    text = lpmodel.get_license_text(img)

    return {"text": text}
