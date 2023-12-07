import cv2

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


def get_license_text(img):
    license_plate_img = get_transformed_img(img)
    (content, _, _) = ocr.read_license_plate(license_plate_img)

    return content[0][1]
