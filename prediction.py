import cv2
from matplotlib import pyplot as plt

from licenseplates import lpmodel

EXAMPLE_IMAGE_PATH = "License-Plates-5/test/images/bbcac63e32bd8137_jpg.rf.ef4704b0ada4fbbf613143abf52f6f86.jpg"

if __name__ == "__main__":
    test_image = cv2.imread(EXAMPLE_IMAGE_PATH)

    bounding_box_data = lpmodel.predict_bounding_box(lpmodel.load_model(), test_image)
    x1, y1, x2, y2 = bounding_box_data["bb"]
    bb_image = test_image.copy()
    cv2.rectangle(bb_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)
    plt.imshow(bb_image)
    plt.show()

    border_edges = lpmodel.detect_borders(bounding_box_data)
    border_image = bounding_box_data["cropped_img"].copy()
    cv2.drawContours(border_image, [border_edges], 0, (0, 255, 0), 2)
    plt.imshow(border_image)
    plt.show()
