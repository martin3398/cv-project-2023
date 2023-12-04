import glob
import os

import cv2
from matplotlib import pyplot as plt

from licenseplates.model import lpmodel

EXAMPLE_IMAGE_PATH = "License-Plates-5/test/images"

def plot_images(images, titles):
    num_images = len(images)

    # Create a subplot grid based on the number of images
    rows = 2  # You can adjust the number of rows and columns based on your preference
    cols = (num_images + 1) // rows

    fig, axes = plt.subplots(rows, cols, figsize=(12, 8))

    # Flatten the axes if there is only one row
    if rows == 1:
        axes = axes.reshape(1, -1)

    for i in range(num_images):
        axes[i // cols, i % cols].imshow(images[i], cmap='gray')
        axes[i // cols, i % cols].set_title(titles[i])
        axes[i // cols, i % cols].axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    test_img_paths = glob.glob(os.path.join(EXAMPLE_IMAGE_PATH, "*.jpg"))

    for idx, img_path in enumerate(test_img_paths[4:50]):
        print("current img index: ", idx)
        test_image = cv2.imread(img_path)

        bounding_box_data = lpmodel.predict_bounding_box(image=test_image, model=lpmodel.load_model())
        x1, y1, x2, y2 = bounding_box_data["bb"]
        bb_image = test_image.copy()
        cv2.rectangle(bb_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)
        plt.imshow(bb_image)
        plt.show()

        border_edges, border_rect = lpmodel.detect_borders(bounding_box_data)
        border_image = bounding_box_data["cropped_img"].copy()
        # cv2.drawContours(border_image, [border_edges], 0, (0, 255, 0), 2)
        # plt.imshow(border_image)
        # plt.show()

        transformed_image = lpmodel.transform_license_plate(image=bounding_box_data["cropped_img"], rectangle=border_rect, corners=border_edges)
        # plt.imshow(transformed_image)
        # plt.show()

        lp_text, images, titles = lpmodel.read_license_plate(image=transformed_image)
        print(lp_text)

        plot_images(images, titles)
