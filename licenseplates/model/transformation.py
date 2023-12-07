import cv2
import numpy as np


def detect_borders(cropped_img):
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

    corners_3d = np.hstack((corners, np.ones((4, 1))))
    transformed_corners = (rotation_matrix @ corners_3d.T).T

    x_min, x_max = np.min(transformed_corners[:, 0]), np.max(transformed_corners[:, 0])
    y_min, y_max = np.min(transformed_corners[:, 1]), np.max(transformed_corners[:, 1])
    x_min, x_max, y_min, y_max = map(int, [x_min, x_max, y_min, y_max])

    x_min, x_max = max(0, x_min), min(rotated_image.shape[1], x_max)
    y_min, y_max = max(0, y_min), min(rotated_image.shape[0], y_max)

    cropped_img = rotated_image[y_min:y_max, x_min:x_max]

    return cropped_img
