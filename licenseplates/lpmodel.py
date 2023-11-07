import ultralytics


def load_model():
    model = ultralytics.YOLO("finetuned-model.pt")

    return model


def predict(model, image):
    results = model(image)

    return results
