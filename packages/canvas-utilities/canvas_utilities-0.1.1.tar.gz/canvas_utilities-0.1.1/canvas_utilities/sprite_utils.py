import os
import numpy as np
from PIL import Image
import glob

from .image_utils import load_image, resize_image


@load_image
def splite(data=None, grid: tuple = (1, 1), name: str = None, output: str = None, ext='png', repeat: int = 1, bg_color="#FF0000"):
    unit_width = int(data.size[0] / grid[0])
    unit_height = int(data.size[1] / grid[1])
    images = []
    frame = 1
    for _ in range(repeat):
        for row in range(grid[1]):  # loop rows
            step = 0
            y_start = row * unit_height
            y_end = y_start + unit_height
            for _ in range(grid[0]):  # loop columns
                region = data.crop(
                    (step, y_start, step + unit_width, y_end)).convert("P")
                pallette = region.getpalette()
                bg = Image.new("P", (unit_width, unit_height), color=bg_color)
                bg.putpalette(pallette)
                bg.paste(region, (0, 0))
                images.append(bg)
                step += unit_width
                frame += 1

    if output:
        for img in images:
            img.save(os.path.join(output, f'{name}_{frame:03}.{ext}'))
    else:
        return images


def to_gif(images: list = [], output=None, start=0, step=1, fps=6.25, loop=0):
    """Generate image sequence into a gif animation file

    Args:
        images ([Image], optional): Represent the image sequences data. Defaults to [].
        output (str, optional): Represent the output path. Defaults to None.
        fps (float, optional): Represent the gif FPS. Defaults to 6.25.
        loop (int, optional): Represent the loop settings. e.g.,
                              0: Looping infinity
                              1: Play once
    """

    # convert image path to Image object

    if isinstance(images[0], str):
        images = [Image.open(item) for item in images]

    opt_images = []
    for index in range(start, len(images), step):
        opt_images.append(images[index])

    opt_images[0].save(output, format='GIF',
                       append_images=opt_images[1:],
                       save_all=True,
                       optimize=False,
                       loop=loop,
                       fps=fps)


def gif_to_sequence(source, output, mode='RGB'):
    img = Image.open(source)
    img_palette = img.getpalette()
    index = 0
    try:
        while 1:
            img.putpalette(img_palette)
            img_data = Image.new(mode, img.size)
            img_data.paste(img)
            img_data.save(os.path.join(output, f'{index:03d}.png'))

            index += 1
            img.seek(img.tell() + 1)

    except EOFError:
        pass  # end of sequence


def gif_to_dataset_array(source, mode='RGB'):
    img = Image.open(source)
    img_palette = img.getpalette()
    index = 0
    dataset = []
    try:
        while 1:
            img.putpalette(img_palette)
            img_data = Image.new(mode, img.size)
            img_data.paste(img)
            dataset.append(np.array(img_data)[:, :, 0].T)
            index += 1
            img.seek(img.tell() + 1)

    except EOFError:
        pass  # end of sequence

    return dataset


def generate_sprites_from_directory(img_path, output, unit_size=512):

    frames = []
    for img in glob.glob(img_path):
        frames.append(Image.open(img))

    total_images = int(len(frames)/2)-7

    print(total_images)

    # calculate row numbers
    row_numbers = int(total_images ** 0.5)
    # if row_numbers ** 2 < total_images:
    #     row_numbers += 1
    # calculate sprite image size
    sprite_size = row_numbers * unit_size

    sprite_im = Image.new('RGB', (sprite_size, sprite_size), color='#000')

    index = 0
    for i in range(0, (sprite_size+unit_size), unit_size):
        for j in range(0, (sprite_size+unit_size), unit_size):
            if index >= total_images:
                break
            im = frames[index]
            img = resize_image(data=im, max_size=unit_size)
            sprite_im.paste(im, (j, i))
            index += 1

    sprite_im.save(output)
