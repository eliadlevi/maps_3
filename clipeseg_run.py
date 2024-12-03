from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import torch

# Define the transformation pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize to fit within 224x224
    transforms.ToTensor(),  # Convert image to a tensor
])

# Load pre-trained CLIPSeg model and processor
processor = CLIPSegProcessor.from_pretrained(
    "CIDAS/clipseg-rd64-refined",
    size={"height": 224, "width": 224}  # Ensure processor resizes to 224x224
)
model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")

# Load an image
image_path = "/home/jellylapubuntu/python/maps_3/cityscapes/leftImg8bit/leftImg8bit/train/aachen/aachen_000172_000019_leftImg8bit.png"
image = Image.open(image_path).convert("RGB")

# Apply the transformations
image_resized = transform(image)
image_resized_pil = transforms.ToPILImage()(image_resized)

# Use a list of labels as text prompts
text_prompts = ["pavement"]

# Process the image and text prompts
inputs = processor(text=text_prompts, images=image_resized_pil, return_tensors="pt", padding=True, truncation=True)

# Check the shapes of processed inputs
print(f"Processor pixel_values shape: {inputs['pixel_values'].shape}")  # Should be [1, 3, 224, 224]
print(f"Processor input_ids shape: {inputs['input_ids'].shape}")  # Should match the number of text prompts

# Perform inference
with torch.no_grad():
    outputs = model(**inputs)
    segmentation_maps = torch.sigmoid(outputs.logits)  # Shape: [num_prompts, 1, H, W]

# Display results for each label
plt.figure(figsize=(15, 10))

for i, (prompt, segmentation) in enumerate(zip(text_prompts, segmentation_maps)):
    segmentation = segmentation[0].cpu().numpy()
    threshold = 0.5  # Apply a threshold to binarize
    segmentation_binary = (segmentation > threshold).astype("uint8")
    
    # Resize segmentation mask back to original image size
    segmentation_resized = Image.fromarray((segmentation_binary * 255).astype("uint8")).resize(image.size)

    # Plot results
    plt.subplot(2, 2, i + 1)
    plt.title(f"Prompt: {prompt}")
    plt.imshow(image)
    plt.imshow(segmentation_resized, alpha=0.6, cmap="jet")
    plt.axis("off")

plt.tight_layout()
plt.show()
