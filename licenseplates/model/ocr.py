import cv2
from easyocr import easyocr


def init_model():
    easyocr.Reader(["en"])


def read_license_plate(image):
    upscaled_image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(upscaled_image, cv2.COLOR_BGR2GRAY)
    denoised_image = cv2.GaussianBlur(gray, (3, 3), 0)
    _, otsu_thresholding = cv2.threshold(denoised_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    adaptive_thresholding = cv2.adaptiveThreshold(
        denoised_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 27, 9
    )

    images_to_plot = [upscaled_image, gray, denoised_image, otsu_thresholding, adaptive_thresholding]
    titles = [
        "Upscaled Image",
        "Grayscale Image",
        "Denoised Image",
        "Otsu Thresholded Image",
        "Adaptive Thresholded Image",
    ]

    # result = pytesseract.image_to_string(adaptive_thresholding, lang='eng')
    reader = easyocr.Reader(["en"], gpu=True)
    result = reader.readtext(adaptive_thresholding)

    return result, images_to_plot, titles
