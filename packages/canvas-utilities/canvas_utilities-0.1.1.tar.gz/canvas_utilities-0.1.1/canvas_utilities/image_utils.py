import colorsys

from numpy import ndarray
import io
import os
import cv2
from functools import wraps

import wrapt
from colorthief import ColorThief
from PIL import Image, ImageEnhance, ImageFilter
from skimage import io as ski_io
from .utils.decorator import required_params
from .utils.io_helper import warm_up_path

ARG_DATA = 'data'
ARG_INDEX = 'index'
ARG_OUTPUT = 'output'
ARG_PATH = 'path'

IMAGE_FORMAT_MAPPING = {
    'JPG': 'JPEG'
}


def grayscale_image_darkness(img: ndarray):
    """Calculate the image darkness value.

    Args:
        img (ndarray): Represent the grayscale image data.

    Returns:
        float: Represent the mean value
    """
    # blur = cv2.blur(img, (5, 5))
    return cv2.mean(img)[0] / 255


@wrapt.decorator
def load_image(wrapped, instance, args, kwargs):
    """A handy decorater to initialize image data. It also could
    help to validate the paths for file and output folder.

    Raises:
        GErrorInvalidParam: Represent the error when missing 'data' param in function.


    """
    # validate the required parameter
    if ARG_DATA not in kwargs:
        raise ValueError(f'Missing parameter:[{ARG_DATA}]')

    # load image data if the specified param was an absolute file path
    if isinstance(kwargs[ARG_DATA], str) and os.path.isfile(kwargs[ARG_DATA]):
        kwargs[ARG_DATA] = Image.open(kwargs[ARG_DATA])

    # if the output path was specified in the parameters
    # it would check and create the output directory
    if ARG_OUTPUT in kwargs:
        warm_up_path(path=kwargs[ARG_OUTPUT])

    return wrapped(**kwargs)


def load_image_data_array(func):
    @wraps(func)
    @required_params(ARG_DATA)
    def wrapper(**kwargs):

        # load image data if the specified param was an absolute file path
        if isinstance(kwargs[ARG_DATA], str) and os.path.isfile(kwargs[ARG_DATA]):
            kwargs[ARG_DATA] = ski_io.imread(kwargs[ARG_DATA], as_gray=True)

        # if the output path was specified in the parameters
        # it would check and create the output directory
        if ARG_OUTPUT in kwargs:
            warm_up_path(path=kwargs[ARG_OUTPUT])

        return func(**kwargs)
    return wrapper

# @load_image
# def square_image(data=None):
#     size = max(data.size)
#     return ImageOps.fit(data, (size, size), Image.ANTIALIAS)


@load_image
def square_image(data=None, fill_color=(0, 0, 0, 0), size=None):
    """Convert image to square size.

    Args:
        data (str or PIL.Image): Represent the image data. It could accept the file path. Or
                                 specify the image data directly.
        fill_color (tuple or Hex str): Represent the background color. Defaults to (0, 0, 0, 0).
                                       It could accept the hex str when mode was 'RGB'/'L'

    Returns:
        [type]: [description]
    """
    size = size or max(data.size)
    new_im = Image.new(mode=data.mode, size=(size, size), color=fill_color)
    new_im.show()
    new_im.paste(
        data, (int((size - data.size[0]) / 2), int((size - data.size[1]) / 2)))
    return new_im


def image_outline(image):
    return image.filter(ImageFilter.FIND_EDGES)


@load_image
def image_bytes_loader(data=None, ext='WEBP'):
    byteIO = io.BytesIO()
    data.save(byteIO, ext)
    return byteIO.getvalue()


def add_border(data=None, width=40):
    size = max(data.size) + width*2
    background = Image.new("RGB", (size, size), (0, 0, 0))
    background.paste(data, box=(width, width))
    return background


def reduce_opacity(im, opacity):
    """
    Returns an image with reduced opacity.
    Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879
    """
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


@load_image
def resize_image(data=None, max_size=512):
    size = max(data.size)
    ratio = max_size / size
    resolution = (round(data.size[0]*ratio), round(data.size[1]*ratio))
    data.thumbnail(resolution, Image.ANTIALIAS)
    return data


def convert_image_to_la(source=None, target=None):
    img = Image.open(source) if isinstance(source, str) else source
    background = Image.new("RGB", img.size, (0, 0, 0))
    background.paste(img, mask=img.split()[3] if len(
        img.split()) > 3 else None)  # 3 is the alpha channel
    img = background.convert('LA')
    if target:
        img.save(target)
    return img


def get_image_hsv_by_palette(path, number=10, resize=(64, 64)):
    color_thief = ColorThief(path)
    colors = color_thief.get_palette(color_count=3)
    images = [draw_blank_image(size=(int(resize[0]/index), resize[1]),
                               rgb=color, path=None) for index, color in enumerate(colors, start=1)]

    palette_image = merge_image_horizontal(
        images, space=0, file_format='PNG', bg=(0, 0, 0, 0))
    return convert_image_to_hsv(palette_image, resize)


@load_image
def get_image_palette_colors(data):
    """Get color lists by rankings.

    Args:
        data (str): Represent the image path/image object.

    Returns:
        [type]: [description]
    """
    colors = data.getcolors()
    opt_colors = filter(lambda item: item[1][3] > 0, colors)
    opt_colors = sorted(opt_colors, key=lambda item: item[0], reverse=True)
    return list(map(lambda item: '#%02x%02x%02x' % (item[1][0], item[1][1], item[1][2]), opt_colors))
    # colors = colorgram.extract(path, count)
    # return set(map(lambda item: '#%02x%02x%02x' % item.rgb, colors))
    # color_thief = ColorThief(path)
    # colors = color_thief.get_palette(color_count=count)
    # return set(map(lambda item: '#%02x%02x%02x' % item, colors))


def get_dominant_color(image, size=(200, 200)):
    """
    Find a PIL image's dominant color, returning an (r, g, b) tuple.
    """
    image = Image.open(image) if isinstance(image, str) else image
    image = image.convert('RGBA')

    # Shrink the image, so we don't spend too long analysing color
    # frequencies. We're not interpolating so should be quick.
    image.thumbnail(size)

    max_score = 0
    dominant_color = None

    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # Skip 100% transparent pixels
        if a == 0:
            continue

        # Get color saturation, 0-1
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]

        # Calculate luminance - integer YUV conversion from
        # http://en.wikipedia.org/wiki/YUV
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)

        # Rescale luminance from 16-235 to 0-1
        y = (y - 16.0) / (235 - 16)

        # Ignore the brightest colors
        if y > 0.9:
            continue

        # Calculate the score, preferring highly saturated colors.
        # Add 0.1 to the saturation so we don't completely ignore grayscale
        # colors by multiplying the count by zero, but still give them a low
        # weight.
        score = (saturation + 0.1) * count

        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)

    return dominant_color


def convert_image_to_hsv(image, size):
    rbg_values = get_dominant_color(image, size)
    return colorsys.rgb_to_hsv(*rbg_values)


def draw_blank_image(size: tuple, rgb: tuple, path: str = None):
    """
    Draw an image with the given information.

    Arguments:
        size {tuple} -- Represent the (width,height) of the new image
        rgb {list} -- Represent the HEX color value
        path {str} -- Represent the file path
    """

    # init canvas
    im = Image.new('RGB', size, rgb)
    if path and os.path.isfile(path):
        im.save(path)
    return im


def merge_image_horizontal(items=[], export_file=None, space=0, file_format='JPEG', bg=(0, 0, 0)):
    images = []
    for item in items:
        images.append(Image.open(item) if isinstance(item, str) else item)

    max_width = 0
    max_height = 0
    for image in images:
        if image.size[1] > max_height:
            max_height = image.size[1]
        max_width += image.size[0]
    # add space
    max_width += space * (len(images) - 1)

    background = Image.new("RGB" if len(
        bg) <= 3 else "RGBA", (max_width, max_height), bg)
    offset = 0
    for _, image in enumerate(images):
        background.paste(image, box=(offset, 0))
        offset += image.size[0] + space

    if export_file:
        os.makedirs(os.path.dirname(export_file), exist_ok=True)
        background.save(export_file, file_format, quality=100)

    return background


def merge_image_vertical(items=[], export_file=None, space=0, file_format='JPEG', bg=(0, 0, 0)):
    images = []
    for item in items:
        images.append(Image.open(item) if isinstance(item, str) else item)

    max_width = 0
    max_height = 0
    for image in images:
        if image.size[0] > max_width:
            max_width = image.size[0]
        max_height += image.size[1]
    # add space
    max_height += space * (len(images) - 1)

    background = Image.new("RGB", (max_width, max_height), bg)
    offset = 0
    for image in images:
        background.paste(image, box=(0, offset))
        offset += image.size[1] + space

    if export_file:
        os.makedirs(os.path.dirname(export_file), exist_ok=True)
        background.save(export_file, file_format, quality=100)

    return background


def merge_image(foreground: Image.Image, background: Image.Image, box=(0, 0)):
    result = Image.new("RGB", background.size, (0, 0, 0))
    result.paste(background, (0, 0), background)  # 3 is the alpha channel
    result.paste(foreground, (0, 0), foreground)  # 3 is the alpha channel
    return result


def build_image_identity_by_hue(path, size=(128, 128)):
    image = get_image_hsv_by_palette(path=path, resize=size)
    return {ARG_INDEX: image[0]*1000, ARG_PATH: path}


@load_image
def convert_image_to_hex_color_array(data=None):
    width, height = data.size
    pixels = data.convert('RGB').load()
    colors = list()
    for i in range(width):
        row = list()
        for j in range(height):
            r, g, b = pixels[j, i]
            row.append('#%02x%02x%02x' % (r, g, b))
        colors.append(row)

    return colors, data.size
