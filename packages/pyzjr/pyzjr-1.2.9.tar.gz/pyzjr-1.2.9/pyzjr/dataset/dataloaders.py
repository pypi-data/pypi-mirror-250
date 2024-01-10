import os
import torch
import random
import numpy as np
from tqdm import tqdm

from PIL import Image
from torch.utils.data import Dataset, DataLoader

__all__ = ["RepeatDataLoader", "BaseClsDataset", "VOCSegmentDataset", "seed_worker"]

class PyZjrDataset(Dataset):
    def __init__(self):
        super(PyZjrDataset, self).__init__()

def seed_worker(worker_id):
    # Set dataloader worker seed: https://pytorch.org/docs/stable/notes/randomness.html#dataloader
    worker_seed = torch.initial_seed() % 2 ** 32
    np.random.seed(worker_seed)
    random.seed(worker_seed)

class BaseClsDataset(PyZjrDataset):
    def __init__(self, file_txt, image_transform=None):
        super().__init__()
        file_txt_result = self._check_file_txt_is_path_or_list(file_txt)
        if self._check_file_txt_format(file_txt_result):
            self.file_txt = file_txt_result  # file_txt format: [path/to/xxx.jpg 0, path/to/xxx.jpg 1, ...]
        self.image_transform = image_transform

    def __len__(self):
        return len(self.file_txt)

    def _check_file_txt_is_path_or_list(self, txt_path):
        path_list = []
        if isinstance(txt_path, str):  # Check if txt_path is a string (path to a file)
            with open(txt_path, 'r') as file:
                lines = file.readlines()
                path_list.extend(line.strip() for line in lines)
        elif isinstance(txt_path, list):  # Check if txt_path is a list
            path_list.extend(item.strip() for item in txt_path)
        else:
            raise ValueError(f"Invalid input type. {txt_path} should be a string (file path) or a list.")
        return path_list

    def _check_file_txt_format(self, file_txt):
        for line in file_txt:
            parts = line.split()
            assert len(parts) == 2, f"BaseClsDataset: Invalid format in line: {line}"
            file_path, digit_label = parts
            assert os.path.exists(file_path), f"BaseClsDataset: File not found: {file_path}"
            assert digit_label.isdigit(), f"BaseClsDataset: Invalid digit label: {digit_label}"
        return True

    def __getitem__(self, idx):
        print(self.file_txt[idx])
        file_path, digit_label = self.file_txt[idx].split()
        raw_image = Image.open(file_path)
        image = raw_image.convert("RGB")
        if self.image_transform is not None:
            image = self.image_transform(image)
        return image, digit_label

class VOCSegmentDataset(PyZjrDataset):
    def __init__(self,voc_root='VOCdevkit',year='2007',image_transform=None, txt_path = "train.txt"):
        super(VOCSegmentDataset, self).__init__()
        assert year in ["2007","2012"], "year can only choose 2007 and 2012"
        root = os.path.join(voc_root, f"VOC{year}")
        assert os.path.exists(root), "path '{}' does not exist.".format(root)

        imgs_dir = os.path.join(root, 'JPEGImages')
        masks_dir = os.path.join(root, 'SegmentationClass')
        txt_path = os.path.join(root, "ImageSets", "Segmentation", txt_path)
        assert os.path.exists(txt_path), "file '{}' does not exist.".format(txt_path)
        with open(os.path.join(txt_path), "r") as f:
            file_names = [x.strip() for x in f.readlines() if len(x.strip()) > 0]

        self.images = [os.path.join(imgs_dir, x + ".jpg") for x in file_names]
        self.masks = [os.path.join(masks_dir, x + ".png") for x in file_names]
        assert (len(self.images) == len(self.masks))
        self.transforms = image_transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        """
        Args:
            index (int): Index
        Returns:
            tuple: (image, target) where target is the image segmentation.
        """
        img = Image.open(self.images[index]).convert("RGB")
        target = Image.open(self.masks[index]).convert("RGB")

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

class YOLOv5Dataset(PyZjrDataset):
    def __init__(self,
                 path,
                 img_size=640,
                 batch_size=2,
                 image_transform=None,
                 ):
        super().__init__()
        self.path = path
        self.img_size = img_size
        self.batch_size = batch_size
        self.transform = image_transform
        self.img_files = self._check_path_is_list(self.path)
        self.label_files = self.img_to_label_paths(self.img_files)

    def img_to_label_paths(self, img_paths):
        """
        1 Replace '/images/' with '/labels/'.
        2 Remove the file extension by calling. split ('.', 1) [0].
        3 Finally, add. txt to obtain the final label path.
        """
        sa, sb = f'{os.sep}images{os.sep}', f'{os.sep}labels{os.sep}'  # /images/, /labels/ substrings
        return [sb.join(x.rsplit(sa, 1)).rsplit('.', 1)[0] + '.txt' for x in img_paths]

    def _check_path_is_list(self, _path):
        img_path_list = []
        if isinstance(_path, list):
            img_path_list.extend(item.strip() for item in _path)














class RepeatDataLoader(DataLoader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._DataLoader__initialized = False
        if self.batch_sampler is None:
            self.sampler = Repeat_sampler(self.sampler)
        else:
            self.batch_sampler = Repeat_sampler(self.batch_sampler)
        self._DataLoader__initialized = True
        self.iterator = super().__iter__()

    def __len__(self):
        return len(self.sampler) if self.batch_sampler is None else len(self.batch_sampler.sampler)

    def __iter__(self):
        total_iterations = len(self)
        for i in tqdm(range(total_iterations), desc=f"Iteration", unit="iteration"):
            yield next(self.iterator)

class Repeat_sampler(object):
    """ Function to create a sampler that repeats forever.

    Args:
        sampler (Sampler)
    """
    def __init__(self, sampler):
        self.sampler = sampler

    def __iter__(self):
        while True:
            yield from iter(self.sampler)


