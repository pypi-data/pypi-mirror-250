
import math

import numpy as np
from PIL import Image
from skimage import filters

from .image_utils import load_image


def find_coeffs(source_coords, target_coords):
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])
    A = np.matrix(matrix, dtype=np.float)
    B = np.array(source_coords).reshape(8)
    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)


@load_image
def make_shadow(data=None, scale=0.16, erosion_iteration=3, preview=False):
    """Generate shadow to the given image.

    Arguments:
        image {str} -- represent the image path.

    Keyword Arguments:
        scale {float} -- Represent the shadow scale value (default: {0.16})
        erosion_iteration {int} -- Represent the erosion iteration (default: {3})
        preview {bool} -- Represent the flag showing origin image on top of the shadow (default: {False})

    Returns:
        [Image] -- Shadow image data
    """
    # keep image width and height
    width, height = data.size
    # calculate the length of the shadow
    length = int(height*scale)
    # make a canvas background, it would be exporting image size
    ground = Image.new('LA', (width*2, height*2), (0, 0))
    # calcualte the xshift value to the end of shadow: Rectangle to Trapezoid
    xshift = int(math.sqrt(length))
    # calcuate the coeffs mapping points
    coeffs = find_coeffs(
        [(0, 0), (width, 0), (width, height), (0, height)],
        [(xshift, 0), ((width-xshift), 0), (width, height+length), (0, height+length)])
    # transform iamge
    data = data.transform((width, int((height+length)/2)),
                          Image.PERSPECTIVE,
                          coeffs,
                          Image.BICUBIC)
    # get image alpha channel
    alpha = data.split()[-1]
    # set alpha channel to 'black'
    gray_img = alpha.point(lambda x: 255 if x < 10 else 0, '1')
    # apply erosion optimizing on the edge of mask, the shadow shape
    # would be smaller than the original image
    erosion_img_mask = filters.edges.binary_erosion(np.array(alpha),
                                                    iterations=erosion_iteration)
    # apply shadow on the canvas ground
    ground.paste(gray_img, (int(width/2), int(height/2 - length/2)),
                 mask=Image.fromarray(erosion_img_mask))

    if preview:
        erosion_img = filters.edges.binary_erosion(
            np.array(data.split()[3]), iterations=1)
        ground.paste(data, (int(width/2), int(height/2)),
                     mask=Image.fromarray(erosion_img))

    return ground
