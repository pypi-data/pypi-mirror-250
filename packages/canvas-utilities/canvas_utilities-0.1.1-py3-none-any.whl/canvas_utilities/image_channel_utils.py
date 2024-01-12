from enum import Enum

import numpy as np
from utils.logging import logger
from PIL import Image

from .image_utils import load_image


class ImageChannel(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


@load_image
def check_channel_texture(data):
    r, _, _ = data.split()
    logger.debug(f'max value: {np.array(r).max()}')
    return np.array(r).max() == 0


@load_image
def remove_image_channel_color(data,  channel: ImageChannel, output=None):
    r, g, b = data.split()
    if channel == ImageChannel.RED:
        r = r.point(lambda i: i * 0)
    elif channel == ImageChannel.GREEN:
        g = g.point(lambda i: i * 0)
    else:
        b = b.point(lambda i: i * 0)

    result = Image.merge('RGB', (r, g, b))
    if output:
        result.save(output)
    return result
