import cv2
from easyocr import easyocr

reader = None

PROCESSING_STEPS_TITLES = [
    "Upscaled Image",
    "Grayscale Image",
    "Denoised Image",
    "Otsu Thresholded Image",
    "Adaptive Thresholded Image",
]


def get_reader():
    global reader
    if reader is None:
        load_reader()
    return reader


def load_reader():
    global reader
    reader = easyocr.Reader(["en"], gpu=True)


def init_model():
    easyocr.Reader(["en"])


def upscale_image(img):
    return cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)


def grayscale_image(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def denoise_image(img):
    return cv2.GaussianBlur(img, (3, 3), 0)


def apply_otsu_thresholding(img):
    _, otsu_thresholded_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return otsu_thresholded_img


def apply_adaptive_thresholding(img):
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 27, 9)


def get_preprocessed_image_steps(img):
    upscaled_image = upscale_image(img)
    gray = grayscale_image(upscaled_image)
    denoised_image = denoise_image(gray)
    otsu_thresholded = apply_otsu_thresholding(denoised_image)
    adaptive_thresholded = apply_adaptive_thresholding(denoised_image)

    return [upscaled_image, gray, denoised_image, otsu_thresholded, adaptive_thresholded]


def get_preprocessed_image(img):
    return get_preprocessed_image_steps(img)[-1]


def get_text(img, reader=get_reader()):
    ocr_result = reader.readtext(img)

    return ocr_result[0][1]
