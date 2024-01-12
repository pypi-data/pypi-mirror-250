
import cv2
import imutils
import blend_modes
from .utils.logging import logger
import numpy as np


def cv_apply_blur(source, output, blur_kernel_size=(5, 5)):
    """ Adds a blur to the given image, using the kernel size
        defined in settings. """
    img = cv2.imread(source, cv2.IMREAD_UNCHANGED)
    logger.debug(f'[CV2-GaussionBlur]: {source}')
    blurred = cv2.GaussianBlur(src=img,
                               ksize=blur_kernel_size,
                               sigmaX=0)
    if output:
        cv2.imwrite(output, blurred)

    return blurred


def cv_canny_image(source, output=None, scale=1, canny1=20, canny2=20):
    # compute the ratio of the old height to the new height, and resize it
    img = cv2.imread(source, cv2.IMREAD_GRAYSCALE)
    height, _ = img.shape
    image = imutils.resize(img, height=int(
        scale*height), inter=cv2.INTER_NEAREST)

    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    # convert the image to grayscale, blur it, and find edges in the image
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(img, (5, 5), 0)
    edged = cv2.Canny(gray, canny1, canny2)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    if output:
        cv2.imwrite(output, edged)
    return edged


def cv_blend_images(source, target, output, opacity=0.7):
    """Blend two images.

    Args:
        source (str): Represent the background image path.
        target (str): Represent the foreground image path.
        output (str): Represent the output path.
        opacity (float, optional): The opacity of the foreground that is blended onto the background. Defaults to 0.7.
    """
    # Import background image
    background_img_float = cv2.imread(source, -1).astype(float)

    # Import foreground image
    foreground_img_float = cv2.imread(target, -1).astype(float)

    # Blend images
    # The opacity of the foreground that is blended onto the background is 70 %.
    blended_img_float = blend_modes.soft_light(
        background_img_float, foreground_img_float, opacity)
    cv2.imwrite(output, blended_img_float)


def cv_enhance_edge(source, output, canny1=20, canny2=20, edge_opacity=1.0):
    background_img = cv2.imread(source, cv2.IMREAD_GRAYSCALE)
    canny_img = cv_canny_image(source=source, canny1=canny1, canny2=canny2)
    background_img = cv2.cvtColor(background_img, cv2.COLOR_GRAY2RGBA)
    canny_img = cv2.cvtColor(canny_img, cv2.COLOR_GRAY2RGBA)

    blended_img = blend_modes.lighten_only(background_img.astype(
        float), canny_img.astype(float), edge_opacity)
    blended_img = blended_img.astype(np.uint8)
    blended_img = cv2.cvtColor(blended_img, cv2.IMREAD_GRAYSCALE)

    if output:
        cv2.imwrite(output, blended_img)
    return blended_img

    # def get_contours(path=None, size=(100, 100)):
    #     im = cv2.imread(path)
    #     imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #     _, thresh = cv2.threshold(imgray, 180, 255, 0)
    #     contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #     image_data = np.zeros(size, np.uint8)
    #     cv2.drawContours(image_data, contours, -1, 255, 1)
    #     gray_array = []
    #     for row in image_data:
    #         gray_array.extend(map(lambda item: 1 if item > 0 else 0, row))

    #     opt_array = []
    #     counter = 1
    #     current_value = gray_array[0]
    #     for item in gray_array[1:]:
    #         if item != current_value:
    #             opt_array.append([current_value, counter])
    #             current_value = item
    #             counter = 1
    #         else:
    #             counter += 1

    #     return opt_array

    #     # plt.imshow(image_data, cmap='gray', vmin=0, vmax=255)
    #     # plt.show()

    # def get_contours_from_folder(path=None, pattern=None):
    #     results = []
    #     search_pattern = os.path.join(path, pattern)
    #     files = glob.glob(f"{search_pattern}*.*")
    #     for item in files:
    #         img = Image.open(item)
    #         # key_name = os.path.basename(os.path.splitext(item)[0])
    #         results.append(get_contours(path=item, size=img.size))
    #     return results
