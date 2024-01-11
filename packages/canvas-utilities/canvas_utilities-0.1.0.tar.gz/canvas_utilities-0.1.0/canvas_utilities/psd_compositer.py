"""The collection of utility tools for PSD file modifications.

Note:
In order to extract images from 32bit PSD files PIL/Pillow must be built with LITTLECMS or LITTLECMS2 support.
"""
import io
import os
import re
from .utils.logging import logger

from psd_tools import PSDImage
from psd_tools import compose as psd_compose
from psd_tools.psd import PSD

from .image_utils import image_bytes_loader


def compose_psd_by_layers(psd_file, folder, filter_pattern, visible_only):
    """Perform the layer/group composing to the psd file.


    Args:
        psd_file {str} -- Represent the psd file path.
        filter_pattern {str} -- Represent the layer filter pattern.
        output_folder {str} -- |Represent the output folder.
                               |(1) google drive-> folderID
                               |(2) the absolute path in local drive)
        visible_only {bool} -- |Represent the flag ignoring invisible layers/groups

    Example:
        Below structure psd file would export two png files that were named as: Slider_01.png & Slider_02.png
        Notes: The invisible layer/group will be ignored when composing.
        >=======================
        |Slider_01
        |Slider_02
        |_Background_Label
        |_Background_Image
        |_Background_SolidColor

    """

    BACKGROUND_PATTERN = 'Background'

    is_google_drive_file = not os.path.isabs(psd_file)

    # load psd file data from google drive OR local harddrive folder
    psd = PSDImage.open(psd_file)

    # resolve the background layers
    background_layers = [layer for layer in psd if layer.is_group() and re.match(
        f"^{BACKGROUND_PATTERN}.*", layer.name, re.IGNORECASE)]
    # resolve the composing slide layers
    slides = [layer for layer in psd if layer.is_group() and re.match(
        f"^{filter_pattern}_.*", layer.name, re.IGNORECASE)]

    slide_name_lists = []

    for slide in slides:

        if not slide.visible and visible_only:
            logger.debug(f'Skip slide: {slide.name} | visibility = False')

            continue
        else:
            slide.visible = True

        logger.debug(f'Composing slide: {slide.name}')

        slide_image = psd_compose(
            layers=[*background_layers, slide], layer_filter=None)

        # resolve slide name
        base_name = os.path.splitext(os.path.basename(psd_file))[0]
        slide_name = f'{base_name}_{slide.name}.png'

        # export image to local folder
        slide_image.save(os.path.join(folder, slide_name))
        slide_name_lists.append(slide_name)

    return slide_name_lists
