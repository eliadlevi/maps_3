from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation
from PIL import Image
import torch

# Load the pre-trained CLIPSeg model
def load_clipseg():
    model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")
    processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
    return model, processor

# Inference function
def perform_inference(image_path, model, processor):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(pixel_values=inputs["pixel_values"])
    segmentation = torch.argmax(outputs.logits, dim=1).squeeze().numpy()
    return segmentation
