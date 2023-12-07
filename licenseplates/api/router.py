import io

import cv2
import numpy as np
from fastapi import APIRouter, File, UploadFile
from PIL import Image
from starlette.responses import StreamingResponse

from licenseplates.model import lpmodel

router = APIRouter()


@router.get("/ping")
def ping():
    return {"ping": "pong"}


@router.post("/bounding-box")
async def create_bounding_box(file: UploadFile = File(...)):
    img = Image.open(io.BytesIO(file.file.read()))
    img = np.array(img)

    res, im_png = cv2.imencode(".png", img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")


@router.post("/crop-bounding-box")
async def crop_bounding_box(file: UploadFile = File(...)):
    img = Image.open(io.BytesIO(file.file.read()))
    img = np.array(img)

    bounding_box_data = lpmodel.predict_bounding_box(img)
    img = lpmodel.add_bounding_box(img, bounding_box_data)

    res, im_png = cv2.imencode(".png", img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")


@router.post("/transform-hom")
async def transform_hom(file: UploadFile = File(...)):
    img = Image.open(io.BytesIO(file.file.read()))
    img = np.array(img)

    res, im_png = cv2.imencode(".png", img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")


@router.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    img = Image.open(io.BytesIO(file.file.read()))
    img = np.array(img)

    res, im_png = cv2.imencode(".png", img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")
