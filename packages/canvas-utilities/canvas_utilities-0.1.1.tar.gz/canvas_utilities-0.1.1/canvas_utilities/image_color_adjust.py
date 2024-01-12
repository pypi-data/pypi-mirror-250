from .image_utils import load_image
from PIL import Image
import cv2
import numpy as np


@load_image
def adjust_image_color_curve(data, lut_in=[0, 85, 160, 255], lut_out=[0, 66, 180, 255], output=None, is_grayscale=True):
    numpy_image = np.array(data)
    opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

    lut_8u = np.interp(np.arange(0, 256), lut_in, lut_out).astype(np.uint8)
    image_contrasted = cv2.LUT(opencv_image, lut_8u)

    if output:
        cv2.imwrite(output, image_contrasted)

    img = cv2.cvtColor(image_contrasted, cv2.IMREAD_GRAYSCALE if is_grayscale else cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)
