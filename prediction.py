import glob
import os

import cv2
from matplotlib import pyplot as plt

from licenseplates.model import lpmodel

EXAMPLE_IMAGE_PATH = "License-Plates-5/test/images"
RESULT_IMAGE_PATH = "License-Plates-5/output"
SAVE_INFO = False
PLOT_GRAPHS = True


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
        axes[i // cols, i % cols].imshow(images[i], cmap="gray")
        axes[i // cols, i % cols].set_title(titles[i])
        axes[i // cols, i % cols].axis("off")

    plt.tight_layout()
    plt.show()


def save_images(curr_img_index, images, titles):
    full_path = os.path.join(RESULT_IMAGE_PATH, f"img-{curr_img_index}")
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    for image, title in zip(images, titles):
        updated_title = title.replace(" ", "_").lower() + ".jpg"
        img_path = os.path.join(full_path, updated_title)
        cv2.imwrite(img_path, image)


def save_lp_text(curr_img_index, lp_text):
    full_path = os.path.join(RESULT_IMAGE_PATH, f"img-{curr_img_index}")
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    file_path = os.path.join(full_path, "license_plate_result.txt")
    with open(file_path, "w") as file:
        file.write(lp_text)


if __name__ == "__main__":
    test_img_paths = glob.glob(os.path.join(EXAMPLE_IMAGE_PATH, "*.jpg"))

    images = []
    titles = []

    lower_bound = 36
    upper_bound = lower_bound + 1
    for idx, img_path in enumerate(test_img_paths[lower_bound:upper_bound]):
        print("Index of current image: ", lower_bound + idx)
        test_image = cv2.imread(img_path)

        # Predict bounding box
        bounding_box_data = lpmodel.predict_bounding_box(image=test_image, model=lpmodel.load_model())
        x1, y1, x2, y2 = bounding_box_data["bb"]
        bb_image = test_image.copy()
        cv2.rectangle(bb_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)
        images.append(bb_image)
        titles.append("Original Image w Bounding Box")

        # Detect borders
        border_edges, border_rect = lpmodel.detect_borders(bounding_box_data)
        border_image = bounding_box_data["cropped_img"].copy()
        cv2.drawContours(border_image, [border_edges], 0, (0, 255, 0), 2)
        images.append(border_image)
        titles.append("Original Cropped Image")

        # Transform image
        transformed_image = lpmodel.transform_license_plate(
            image=bounding_box_data["cropped_img"], rectangle=border_rect, corners=border_edges
        )
        images.append(transformed_image)
        titles.append("Transformed Image")

        # Read license plate
        lp_result, add_images, add_titles = lpmodel.read_license_plate(image=transformed_image)
        print(lp_result[0][1])

        images = images + add_images
        titles = titles + add_titles

        if PLOT_GRAPHS is True:
            plot_images(images, titles)

        if SAVE_INFO is True:
            save_images(lower_bound + idx, images, titles)
            save_lp_text(lower_bound + idx, lp_result[0][1])
