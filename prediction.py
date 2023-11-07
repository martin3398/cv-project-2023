import cv2

from licenseplates import lpmodel

EXAMPLE_IMAGE_PATH = "License-Plates-5/test/images/b1a50a3824887ee2_jpg.rf.68a4fd34fce20184287592f2680f895b.jpg"

if __name__ == "__main__":
    model = lpmodel.load_model()

    test_image = cv2.imread(EXAMPLE_IMAGE_PATH)
    lpmodel.predict(model, test_image)
