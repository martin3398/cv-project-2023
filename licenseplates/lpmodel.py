import ultralytics


def load_model():
    model = ultralytics.YOLO("finetuned-model.pt")

    return model


def predict_bounding_box(model, image):
    results = model(image)

    return results


def detect_borders(image, bounding_box):
    pass


def transform_license_plate(image, borders):
    pass


def read_license_plate(image):
    pass


def get_license_text(image):
    model = load_model()
    bounding_box = predict_bounding_box(model, image)
    borders = detect_borders(image, bounding_box)
    license_plate = transform_license_plate(image, borders)
    content = read_license_plate(license_plate)

    return content
