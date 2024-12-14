from transformers import SegformerFeatureExtractor, SegformerForSemanticSegmentation
import torch
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Load pre-trained model and feature extractor
model_name = "nvidia/segformer-b1-finetuned-cityscapes-1024-1024"
feature_extractor = SegformerFeatureExtractor.from_pretrained(model_name)
model = SegformerForSemanticSegmentation.from_pretrained(model_name)

# Load and preprocess an image
image_path = "/home/jellylapubuntu/python/maps_3/cityscapes/leftImg8bit/leftImg8bit/train/aachen/aachen_000035_000019_leftImg8bit.png"
image = Image.open(image_path).convert("RGB")
inputs = feature_extractor(images=image, return_tensors="pt")

# Perform inference
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits  # Shape: [batch_size, num_classes, height, width]
    segmentation = torch.argmax(logits, dim=1).squeeze().cpu().numpy()

# Visualize the numeric segmentation mask over the original image
plt.figure(figsize=(15, 10))
plt.imshow(image, alpha=0.8)  # Original image with some transparency
plt.imshow(segmentation, alpha=0.5, cmap="tab20")  # Segmentation overlay with colormap
plt.colorbar(label="Class Index")  # Color bar for numeric class representation
plt.axis("off")
plt.title("Segmentation Mask (Numeric Overlay)")
plt.show()
