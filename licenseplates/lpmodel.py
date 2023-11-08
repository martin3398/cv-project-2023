import cv2
import numpy as np
import ultralytics


def load_model():
    model = ultralytics.YOLO("finetuned-model.pt")

    return model


def predict_bounding_box(model, image):
    results = model(image)[0]

    lp_boxes = [box_data for box_data in results.boxes.data.tolist() if box_data[5] == 0]
    if not lp_boxes:
        raise ValueError("No license plate found")

    best_box = max(lp_boxes, key=lambda box: box[4])

    return {
        "bb": best_box[:4],
        "cropped_img": image[int(best_box[1]) : int(best_box[3]), int(best_box[0]) : int(best_box[2])],
        "confidence": best_box[4],
    }


def detect_borders(bounding_box_data):
    cropped_img = bounding_box_data["cropped_img"]
    gray_image = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

    # TODO: Use Canny edge detection, set edges to 0
    # TODO: maybe use 128 here?
    _, binary_image = cv2.threshold(gray_image, np.mean(gray_image), 255, cv2.THRESH_BINARY)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_image, 8, cv2.CV_32S)

    largest_area = 0
    largest_label = 0
    for label in range(1, num_labels):
        area = stats[label, cv2.CC_STAT_AREA]
        if area > largest_area:
            largest_area = area
            largest_label = label

    mask = np.zeros_like(binary_image)
    mask[labels == largest_label] = 255

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour = max(contours, key=cv2.contourArea)

    rect = cv2.minAreaRect(contour)

    box = cv2.boxPoints(rect).astype(int)

    return box


def transform_license_plate(image, borders):
    pass


def read_license_plate(image):
    pass


def get_license_text(image):
    model = load_model()
    bounding_box_data = predict_bounding_box(model, image)
    borders = detect_borders(bounding_box_data)
    license_plate = transform_license_plate(image, borders)
    content = read_license_plate(license_plate)

    return content
