import io

import cv2
from matplotlib import pyplot as plt
from PIL import Image

from licenseplates.model import boundingbox, ocr, transformation


def init_modules():
    boundingbox.load_model()
    ocr.init_model()


def get_image_with_bounding_box(img):
    bounding_box_data = boundingbox.predict_bounding_box(img)

    x1, y1, x2, y2 = bounding_box_data["bb"]
    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 1)

    return img


def get_cropped_image(img):
    bounding_box_data = boundingbox.predict_bounding_box(img)

    return bounding_box_data["cropped_img"]


def get_transformed_img(img):
    cropped_img = get_cropped_image(img)
    border_edges, border_rect = transformation.detect_borders(cropped_img)

    return transformation.transform_license_plate(cropped_img, border_rect, border_edges)


def get_preprocessed_image_steps(img):
    transformed_img = get_transformed_img(img)
    (upscaled_image, _, denoised_image, otsu_thresholded, adaptive_thresholded) = ocr.get_preprocessed_image_steps(
        transformed_img
    )

    fig, axes = plt.subplots(2, 2, figsize=(12, 6))
    fig.set_facecolor("lightgray")

    axes = axes.flatten()
    for i, (img, title) in enumerate(
        [
            (upscaled_image, "Upscaled Image"),
            (denoised_image, "Denoised Image"),
            (otsu_thresholded, "Otsu Thresholded Image"),
            (adaptive_thresholded, "Adaptive Thresholded Image"),
        ]
    ):
        axes[i].imshow(img, cmap="gray")
        axes[i].set_title(title, fontsize=24)
        axes[i].axis("off")

    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)

    return Image.open(buf)


def get_preprocessed_image(img):
    transformed_img = get_transformed_img(img)
    return ocr.get_preprocessed_image(transformed_img)


def get_license_text(img):
    preprocessed_img = get_preprocessed_image(img)

    return ocr.get_text(preprocessed_img)
