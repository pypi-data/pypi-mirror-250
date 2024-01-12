"""Implemented a couple wrapper to parse the image hash value from a given file.
"""
import imagehash
from PIL import Image

HASH_SIZE = 8
HIGHFREQ_FACTOR = 8


def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))

    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)


def get_image_hash(path=None):
    source_image = Image.open(path) if isinstance(path, str) else path
    channel_counts = len(source_image.split())
    # define the box location of RGBA layers
    segments = [(0, 0),  # top/left
                (source_image.size[0], 0),  # top/right
                (0, source_image.size[1]),  # bot/left
                (source_image.size[0], source_image.size[1])]  # bot/right

    merged_image = Image.new(
        "RGB", (source_image.size[0]*2, source_image.size[1]*2), (0, 0, 0))
    for index in range(channel_counts):
        single_channel = source_image.getdata(index)
        data_trans = Image.new("RGB", source_image.size, (0)*3)
        data_trans.putdata(list(zip(*([single_channel]*3))))
        merged_image.paste(data_trans, box=segments[index], mask=None)

    return imagehash.phash(image=merged_image,
                           hash_size=HASH_SIZE,
                           highfreq_factor=HIGHFREQ_FACTOR)


def compare_images(source=None, target=None):
    """Compare two images and output the similarity value.

    Keyword Arguments:
        source {str} -- Represent the first image path (default: {None})
        target {str} -- Represent the second image path (default: {None})
        hash_mode {str} -- [description] (default: {'phash'})
    """
    source_hash = get_image_hash(path=source)
    target_hash = get_image_hash(path=target)
    similarity = 1 - (source_hash - target_hash)/len(source_hash.hash)**2
    return source_hash == target_hash, similarity
