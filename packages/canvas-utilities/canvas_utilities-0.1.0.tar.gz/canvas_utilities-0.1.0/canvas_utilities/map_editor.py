import io
from PIL import Image, ImageFilter
from .image_utils import reduce_opacity, image_bytes_loader
from .utils.io_helper import warm_up_path
from .utils.mime_types import GMimeTypes


class MapCanvas():
    def __init__(self, size=(1024, 1024)):
        self.image = Image.new("RGBA", size)

    def add(self, image_bytes, position, rotation):
        img = Image.open(io.BytesIO(image_bytes))
        img = img.rotate(rotation)
        image_array = img.split()
        width, height = img.size
        x, y = position
        new_position = (x-int(width/2), y-int(height/2))
        self.image.paste(img, box=new_position, mask=image_array[-1])

    def merge(self, image):
        image = image.resize(self.image.size)
        self.image.paste(image, box=(0, 0), mask=image.split()[-1])

    def add_filter(self, radius=2, alpha=0.5):
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius=2))
        self.image = reduce_opacity(self.image, alpha)

    def export(self, path):
        warm_up_path(path=path)
        self.image.save(path)

    def to_bytes(self, ext=GMimeTypes.WEBP.name):
        return image_bytes_loader(data=self.image, ext=ext)

    def show(self):
        self.image.show()
