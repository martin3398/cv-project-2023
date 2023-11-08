import cv2
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

    _, mask = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)

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
