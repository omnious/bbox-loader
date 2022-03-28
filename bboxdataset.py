import torch
from PIL import Image, ImageFile
from bboxloader import BBoxList
from random import randrange
from os.path import join

ImageFile.LOAD_TRUNCATED_IMAGES = True


def letterbox_image(image: Image, size: int = 224):
    """
        Rescales the image in `image_path` to fit in a `size` x `size` image
        while keeping the aspect ratio of the original image by padding the
        shortest side with black pixels
    Parameters
    ----------------
    image: Image
        A PIL Image
    size: int
        Ouput size of the image
    center: bool
        Whether to center or not the image
    """
    input_size = image.size
    scale = float(size) / max(input_size)
    temp_size = tuple([int(x * scale) for x in input_size])
    temp_image = image.resize(temp_size, Image.LINEAR)
    out_image = Image.new("RGB", (size, size))
    offset = (
        int((size - temp_size[0]) / 2 + 0.5),
        int((size - temp_size[1]) / 2 + 0.5),
    )
    out_image.paste(temp_image, offset)
    return out_image


class BBoxDataset(torch.utils.data.Dataset):
    def __init__(self, data_root: str, data_path: str, size=224, transform=None):
        self.transform = transform
        self.size = size
        self.image_listing = BBoxList()
        self.image_listing.load(data_path)
        self.root = data_root

    def __len__(self):
        return len(self.image_listing)

    def __getitem__(self, idx):
        info = self.image_listing[idx]
        try:
            image = Image.open(join(self.root, info.path)).convert("RGB")
        except:
            print("ERROR: skipping image:", join(self.root, info.path))
            return self.__getitem__(randrange(0, self.__len__()))
        crop = image.crop((info.xmin, info.ymin, info.xmax, info.ymax))
        letterbox = letterbox_image(crop, size=self.size, center=True)
        if self.transform is not None:
            letterbox = self.transform(letterbox)
        return letterbox, 0
