from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import torch

# Define the transformation pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize image to 224x224
    transforms.ToTensor(),          # Convert image to a tensor
])

# Load pre-trained CLIPSeg model and processor
model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")
processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")

# Load an image
image_path = "/home/jellylapubuntu/python/maps_3/cityscapes/leftImg8bit/leftImg8bit/train/aachen/aachen_000171_000019_leftImg8bit.png"
image = Image.open(image_path).convert("RGB")

# Apply the transformations
image_resized = transform(image)
print(f"Transformed image shape: {image_resized.shape}")  # Shape should be [3, 224, 224]

# Convert back to PIL image for processor
image_resized_pil = transforms.ToPILImage()(image_resized)

# Use the text prompt "sidewalk"
text_prompt = ["sidewalk"]

# Preprocess the input using the processor
inputs = processor(text=text_prompt, images=image_resized_pil, return_tensors="pt")
print(f"Processor output shape: {inputs['pixel_values'].shape}")  # Should be [1, 3, 224, 224]

# Perform inference
with torch.no_grad():
    outputs = model(**inputs)
    segmentation = torch.sigmoid(outputs.logits)

# Resize segmentation mask back to the original image size for visualization
segmentation = segmentation[0][0].cpu().numpy()
segmentation_resized = Image.fromarray((segmentation * 255).astype('uint8')).resize(image.size)

# Display results
plt.figure(figsize=(12, 6))

# Original Image
plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(image)
plt.axis("off")

# Segmentation Mask
plt.subplot(1, 2, 2)
plt.title("Segmentation: Sidewalk")
plt.imshow(image)
plt.imshow(segmentation_resized, alpha=0.6, cmap="jet")  # Overlay mask
plt.axis("off")

plt.show()
