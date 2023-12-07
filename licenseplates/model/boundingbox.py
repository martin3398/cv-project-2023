import ultralytics

model = None


def get_model():
    global model
    if model is None:
        load_model()
    return model


def load_model():
    global model
    model = ultralytics.YOLO("finetuned-model.pt")


def predict_bounding_box(image, model=get_model()):
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
