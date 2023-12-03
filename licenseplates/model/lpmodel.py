import cv2
import numpy as np
import ultralytics
import pytesseract
from matplotlib import pyplot as plt

model = None
def get_model():
    global model
    if model is None:
        model = load_model()
    return model

def load_model():
    model = ultralytics.YOLO("finetuned-model.pt")

    return model


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

def add_bounding_box(image, bounding_box_data):
    x1, y1, x2, y2 = bounding_box_data["bb"]
    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)

    return image


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
    return box, rect


def transform_license_plate(image, rectangle, corners):
    width, height = rectangle[1][0], rectangle[1][1]
    angle = rectangle[-1]

    if width < height:
        angle -= 90
    
    rotation_matrix = cv2.getRotationMatrix2D(rectangle[0], angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))
    
    corners_3D = np.hstack((corners, np.ones((4,1))))
    transformed_corners = (rotation_matrix @ corners_3D.T).T

    x_min, x_max = np.min(transformed_corners[:,0]), np.max(transformed_corners[:,0])
    y_min, y_max = np.min(transformed_corners[:,1]), np.max(transformed_corners[:,1])
    x_min, x_max, y_min, y_max = map(int, [x_min, x_max, y_min, y_max])
    
    x_min, x_max = max(0, x_min), min(rotated_image.shape[1], x_max)
    y_min, y_max = max(0, y_min), min(rotated_image.shape[0], y_max)
    
    cropped_img = rotated_image[y_min:y_max,x_min:x_max]

    return cropped_img


def read_license_plate(image):
    upscaled_image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(upscaled_image, cv2.COLOR_BGR2GRAY)
    denoised_image = cv2.GaussianBlur(gray, (3, 3), 0)
    enhanced_image = cv2.equalizeHist(denoised_image)
    _, thresholded_image = cv2.threshold(enhanced_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Display images using Matplotlib without colormap
    plt.imshow(upscaled_image, cmap='gray')
    plt.title('Upscaled Image')
    plt.show()
    plt.imshow(gray, cmap='gray')
    plt.title('Grayscale Image')
    plt.show()
    plt.imshow(denoised_image, cmap='gray')
    plt.title('Denoised Image')
    plt.show()
    plt.imshow(enhanced_image, cmap='gray')
    plt.title('Enhanced Contrast Image')
    plt.show()
    plt.imshow(thresholded_image, cmap='gray')
    plt.title('Thresholded Image')
    plt.show()

    text = pytesseract.image_to_string(thresholded_image, lang='eng')
    return text


def get_license_text(image):
    model = load_model()
    bounding_box_data = predict_bounding_box(model, image)
    borders = detect_borders(bounding_box_data)
    license_plate = transform_license_plate(image, borders)
    content = read_license_plate(license_plate)

    return content
