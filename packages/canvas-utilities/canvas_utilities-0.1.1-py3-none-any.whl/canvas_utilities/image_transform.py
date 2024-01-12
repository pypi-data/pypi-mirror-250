import numpy as np
from PIL import Image


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=np.float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)


def transform_coefficients(image):

    img = Image.open(image)
    width, height = img.size
    m = -0.2
    xshift = abs(m) * width
    new_width = width + int(round(xshift))
    # img = img.transform((new_width, height), Image.AFFINE,
    #         (1, m, -xshift if m > 0 else 0, 0, 1, 0), Image.BICUBIC)
    # img.save(sys.argv[2])
    scale_factor = 130
    coeffs = find_coeffs(
        [(0, 0), (width, 0), (width, height), (0, height)],
        [(-(scale_factor), 0), (width+scale_factor, 0), (width, height), (0, height)])

    img = img.transform((width, height), Image.PERSPECTIVE, coeffs,
                        Image.BICUBIC)
    return img
