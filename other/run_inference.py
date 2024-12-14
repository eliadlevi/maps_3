import os
import matplotlib.pyplot as plt
from models.clipseg_inference import load_clipseg, perform_inference

# Paths
image_dir = "path/to/cityscapes/leftImg8bit/val/aachen"
output_dir = "results/segmentation_masks"
os.makedirs(output_dir, exist_ok=True)

# Load CLIPSeg model and processor
model, processor = load_clipseg()

# Perform inference on all images in the folder
image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(".png")]

for image_path in image_paths:
    segmentation = perform_inference(image_path, model, processor)

    # Save or visualize results
    output_path = os.path.join(output_dir, os.path.basename(image_path).replace(".png", "_segmentation.png"))
    plt.imsave(output_path, segmentation, cmap="jet")
    print(f"Saved segmentation for {os.path.basename(image_path)}")
