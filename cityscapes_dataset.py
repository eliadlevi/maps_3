import os
import numpy as np
import torch
from torch.utils.data import Dataset
from PIL import Image

class CityscapesDataset(Dataset):
    def __init__(self, image_dir, label_dir, transform=None):
        self.image_dir = image_dir
        self.label_dir = label_dir
        self.transform = transform
        self.image_paths = []
        self.label_paths = []
        for city in os.listdir(image_dir):
            city_img_dir = os.path.join(image_dir, city)
            city_label_dir = os.path.join(label_dir, city)
            for file_name in os.listdir(city_img_dir):
                if file_name.endswith("_leftImg8bit.png"):
                    self.image_paths.append(os.path.join(city_img_dir, file_name))
                    label_name = file_name.replace("_leftImg8bit.png", "_gtFine_labelIds.png")
                    self.label_paths.append(os.path.join(city_label_dir, label_name))

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert("RGB")
        label = Image.open(self.label_paths[idx])  # Load label image

        if self.transform:
            image = self.transform(image)

        # Convert label to a NumPy array
        label = torch.tensor(np.array(label), dtype=torch.long)  # Convert label to tensor

        return image, label

