import colorsys
import io
import os
import difflib
from sys import platform
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat

from .compare_image_hash import compare_images
from . import colorgram
from .utils.logging import logger

DUPLICATE_TEXTURE_REPORT_IMAGE_WIDTH = 1000


def draw_text(image, text=[], color=(0, 0, 0), offset=(0, 0), line_space=10, font_size=12):
    if platform == 'darwin':
        _font = ImageFont.truetype(
            "/Library/Fonts/Arial.ttf", font_size, encoding="unic")
    else:
        _font = ImageFont.truetype("arial", font_size)

    draw = ImageDraw.Draw(image)
    for index, line in enumerate(text):
        draw.text((offset[0], offset[1]+(line_space*index)),
                  line, color, font=_font)
    return image


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


def formalize_image(data=None, source=None, output=None):
    """It would be used to formalize the image data for confluence page.
    """
    FIXED_WIDTH_MAX = 1280
    FIXED_WIDTH_MED = 870
    FIXED_WIDTH_SMALL = 300

    if source:
        im = Image.open(source)
    else:
        im = Image.open(io.BytesIO(data))

    if im.size[0] > FIXED_WIDTH_MED:
        wpercent = (FIXED_WIDTH_MAX / float(im.size[0]))
        hsize = int((float(im.size[1]) * float(wpercent)))
        im_back = im.resize((FIXED_WIDTH_MAX, hsize), Image.ANTIALIAS)
    elif im.size[0] < FIXED_WIDTH_MED and im.size[0] > FIXED_WIDTH_SMALL:
        im_back = Image.new(
            'RGB', (FIXED_WIDTH_MAX, im.size[1]), (182, 175, 159))
        pos = int((FIXED_WIDTH_MAX - im.size[0])/2), 0
        im_back.paste(im, pos)
    else:
        im_back = im
    if output:
        im_back.save(output)
    byteIO = io.BytesIO()
    im_back.save(byteIO, 'PNG')
    return byteIO.getvalue()


def draw_image_placeholder(size: tuple = (1280, 820), text: str = None, path: str = None):
    im_back = Image.new('RGB', size, (52, 52, 52))
    im_fore = Image.new('RGB', tuple(val - 4 for val in size), (84, 84, 84))
    im_back.paste(im_fore, box=(2, 2))

    _font_title = ImageFont.truetype("arial", 27)
    _font_title_02 = ImageFont.truetype("arial", 18)
    draw = ImageDraw.Draw(im_back)
    draw.text((60, 120), 'Placeholder - {}'.format(text),
              (128, 128, 128), font=_font_title)
    draw.text((60, 160), '{} x {}'.format(
        size[0], size[1]), (66, 66, 66), font=_font_title_02)
    if path:
        im_back.save(path)
    else:
        byteIO = io.BytesIO()
        im_back.save(byteIO, 'PNG')
        return byteIO.getvalue()


def get_image_metadata(path=None):
    """Parse image metadata: resolution & file size.

    Keyword Arguments:
        path {str} -- Represent the file full path. (default: {None})
    """
    return {
        'res': list(get_image_resolution(path=path)),
        'size': os.path.getsize(path)
    }


def get_image_resolution(path=None, data=None):
    """Get image resolution. output: (width, height)

    Arguments:
        path {str} -- Represent the full file path.
    """
    if path:
        im = Image.open(path)
    else:
        im = Image.open(io.BytesIO(data))
    return im.size


def resolve_alpha_channel_to_rgb(source):
    """copy the alpha channel to RGB

    Arguments:
        source {str} -- Represent the image path.
    """
    source_image = Image.open(source)
    if source_image.mode != 'LA' and source_image.mode != 'RGB':
        source_image.convert('RGBA')
        extrema = source_image.convert("L").getextrema()

        if extrema == (0, 0) or extrema == (255, 255):
            alpha = source_image.getdata(3)
            color_data = zip(alpha, alpha, alpha)
            source_image.putdata(list(color_data))
    return source_image


def merge_image(items=[], export_file=None, space=0, file_format='JPEG'):
    images = []
    for item in items:
        images.append(Image.open(item) if isinstance(item, str) else item)

    if len(set(image.size[0] for image in images)) != 1:
        raise ValueError('Images have different resolutions!')

    max_width = images[0].size[0]
    max_height = images[0].size[1]

    background = Image.new(
        "RGBA", (max_width*len(images) + (space*len(images)-1), max_height), (0, 0, 0, 0))

    for index, image in enumerate(images):
        background.paste(image, box=((index * max_width) + (index * space), 0),
                         mask=image.split()[3] if len(image.split()) > 3 else None)
    # Convert to RGB if the format is JPEG
    if file_format.lower() == 'jpeg':
        background = background.convert('RGB')

    if export_file:
        os.makedirs(os.path.dirname(export_file), exist_ok=True)
        background.save(export_file, file_format, quality=100)

    return background


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
    for index, image in enumerate(images):
        background.paste(image, box=(0, offset))
        offset += image.size[1] + space

    if export_file:
        os.makedirs(os.path.dirname(export_file), exist_ok=True)
        background.save(export_file, file_format, quality=100)

    return background


def resize_image(image=None, resolution=(512, 512)):
    img = Image.open(image) if isinstance(image, str) else image
    size = max(img.size)
    background = Image.new("RGB", (size, size), (0, 0, 0))
    if len(set(img.size)) > 1:
        background.paste(img, box=(0, 0), mask=img.split()[
                         3] if len(img.split()) > 3 else None)
    else:
        background = img

    background.thumbnail(resolution, Image.ANTIALIAS)
    return background


def brightness(image):
    img = Image.open(image) if isinstance(image, str) else image
    im = img.convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]


def get_image_hsv_by_palette(path, number=10, resize=(64, 64)):
    image = Image.open(path)
    image = resize_image(image, resolution=resize)
    images, colors = get_image_palette(image, number)

    images = [draw_blank_image(size=(int(resize[0]/index), resize[1]),
                               rgb=color.rgb, path=None) for index, color in enumerate(colors, start=1)]

    palette_image = merge_image_horizontal(
        images, space=0, file_format='PNG', bg=(0, 0, 0, 0))
    return convert_image_to_hsv(palette_image)


def convert_image_to_hsv(image):
    image = Image.open(image) if isinstance(image, str) else image
    image = image.convert('RGB')
    max_score = 0.0001
    for count, (r, g, b) in image.getcolors(image.size[0]*image.size[1]):
        # convert to HSV
        saturation = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)[1]
        y = min(abs(r*2104+g*4130+b*802+4096+131072) >> 13, 235)
        y = (y-16.0)/(235-16)

        # ignore high-level bright color
        if y > 0.9:
            continue
        score = (saturation+0.1)*count
        if score > max_score:
            max_score = score
            return colorsys.rgb_to_hsv(r, g, b)
    return None


def convert_image_to_la(path=None, target=None, resolution=(512, 512)):
    img = resize_image(image=path, resolution=resolution)
    background = Image.new("RGB", img.size, (0, 0, 0))
    background.paste(img, mask=img.split()[3] if len(
        img.split()) > 3 else None)  # 3 is the alpha channel
    img = background.convert('LA')
    if target:
        img.save(target)
    return img


def validate_grayscale_image(path):
    img = Image.open(path)
    img.thumbnail((16, 16), Image.ANTIALIAS)
    channel_counts = len(img.split())
    if channel_counts == 1:
        # LA mode image
        return True
    else:
        r_row = list(img.getdata(0))
        g_row = list(img.getdata(1))
        b_row = list(img.getdata(2))
        sm1 = difflib.SequenceMatcher(None, r_row, b_row)
        sim1 = sm1.ratio()
        return sim1 > 0.9


def is_grayscale_image(path):
    grayscale_image = Image.open(path).convert('L')
    rgb_grayscale_image = Image.new("RGBA", grayscale_image.size)
    rgb_grayscale_image.paste(grayscale_image)
    _, sim_value = compare_images(source=rgb_grayscale_image, target=path)
    logger.debug(sim_value)
    return True if sim_value > 0.9 else False


def get_image_palette(path, number, palette_size=(64,)*2):
    colors = colorgram.extract(path, number)
    images = [draw_blank_image(size=palette_size,
                               rgb=color.rgb, path=None) for color in colors]
    return images, colors


def convert_image_type(path=None, target=None, extension=None, resolution=None):
    img = resize_image(image=path, resolution=resolution)
    if extension:
        file_path, _ = os.path.splitext(target)
        target = '{}.{}'.format(file_path, extension)
    if target:
        img.save(target)
    return target


def convert_palette_to_la(source):
    try:
        source_image = Image.open(source)
        alpha_image = resolve_alpha_channel_to_rgb(source)
        merged_image = ImageChops.add_modulo(source_image, alpha_image)
        preview_image = ImageChops.add(source_image, alpha_image, scale=2.0)
        converted_image = Image.new('RGB', merged_image.size, (123, 123, 123))
        converted_image.paste(merged_image)

        converted_preview_image = Image.new(
            'RGB', preview_image.size, (123, 123, 123))
        converted_preview_image.paste(preview_image)
        # converted_image.convert('LA')
        return converted_image, converted_preview_image
    except Exception as e:
        print('invalid texture: {}'.format(source))
        print('exception: {}'.format(str(e)))
        raise ValueError('path:{}'.format(source))


def draw_images_by_group(image_clusters, hash_table, file_path):
    _thumbnail_size = (50, 50)
    _title_height = 10
    _separator_width = 2
    _hor_offset_initial = int(DUPLICATE_TEXTURE_REPORT_IMAGE_WIDTH / 2)
    _ver_offset = 20

    if platform == 'darwin':
        _font = ImageFont.truetype(
            "/Library/Fonts/Arial.ttf", 10, encoding="unic")
    else:
        _font = ImageFont.truetype("arial", 10)

    # caculate export image size
    # height
    _total_height = 100
    for image_group in image_clusters:
        _total_height += (_thumbnail_size[1] +
                          _title_height) * (len(image_group)-1)
    _total_height += len(image_clusters)*_separator_width*2

    image_canvas = Image.new(
        'RGB', (DUPLICATE_TEXTURE_REPORT_IMAGE_WIDTH, _total_height), (230, 230, 230))
    image_canvas_drawer = ImageDraw.Draw(image_canvas)
    for image_group in image_clusters:
        _hor_offset = 20
        _ver_offset += _separator_width + 2
        for index, texture_key in enumerate(image_group):
            # load texture
            texture_path = hash_table[texture_key]['path']
            texture, preview_texture = convert_palette_to_la(texture_path)
            if not texture:
                continue
            # resize texture
            preview_texture.thumbnail(_thumbnail_size, Image.ANTIALIAS)

            if index != 0:
                _hor_offset = _hor_offset_initial
            # draw text
            sub_image = Image.new(
                'RGB', (_hor_offset_initial,  _thumbnail_size[1]+_title_height), (230, 230, 230))
            sub_image.paste(preview_texture)
            draw = ImageDraw.Draw(sub_image)
            image_dir, image_file = os.path.split(texture_key)
            draw.text(
                (_thumbnail_size[1]+2, 0), 'PATH: {}'.format(image_dir), (0, 0, 0), font=_font)
            draw.text((_thumbnail_size[1]+2, _title_height), 'FILE: {} {}'.format(
                image_file, hash_table[texture_key]['res']), (0, 0, 0), font=_font)

            # merge image into canvas
            image_canvas.paste(sub_image, (_hor_offset, _ver_offset))
            if index >= 1:
                _ver_offset += _thumbnail_size[1]+_title_height
        image_canvas_drawer.line((0, _ver_offset, DUPLICATE_TEXTURE_REPORT_IMAGE_WIDTH,
                                  _ver_offset), fill=(0, 0, 0), width=_separator_width)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    image_canvas.save(file_path)


def calculate_releasing_memory(image_clusters, hash_table):
    total_size = 0
    total_files_numbers = 0
    for image_group in image_clusters:
        file_size = os.path.getsize(hash_table[image_group[0]]['path'])
        total_size += file_size * (len(image_group)-1)
        total_files_numbers += (len(image_group)-1)
    return total_size, total_files_numbers
