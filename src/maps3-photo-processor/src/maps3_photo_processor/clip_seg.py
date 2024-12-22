import torch
from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation
import torch.nn.functional as F
from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation
import torch

class ClipSegImageProcessing:
    def segment_with_labels(image, labels):
        # Load the CLIPSeg processor and model
        processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
        model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")

        # Preprocess the resized image and text prompts
        inputs = processor(
            text=labels,
            images=[image] * len(labels),  # Duplicate the image for each label
            return_tensors="pt",
        )

        inputs['pixel_values'] = F.interpolate(
            inputs['pixel_values'], size=(224, 224), mode="bilinear", align_corners=False
        )

        # Verify input tensor shape
        print(f"Input tensor shape: {inputs['pixel_values'].shape}")  # Expect [batch_size, 3, 224, 224]

        # Perform inference
        with torch.no_grad():
            outputs = model(**inputs)

        # Extract segmentation masks
        segmentation_masks = outputs.logits.sigmoid().cpu().numpy()  # Shape: [num_labels, H, W]
        print(f"Segmentation masks shape: {segmentation_masks.shape}")

        return segmentation_masks

# def display_results(labels, masks):
#     image_path = "/home/jellylapubuntu/python/maps_3/cityscapes/leftImg8bit/leftImg8bit/train/aachen/aachen_000035_000019_leftImg8bit.png"
#     image = Image.open(image_path).convert("RGB")
#     original_width, original_height = image.size  # Get the original image dimensions

#     plt.figure(figsize=(15, 5))

#     # Display the original image
#     plt.subplot(1, len(labels) + 1, 1)
#     plt.imshow(image)
#     plt.axis("off")
#     plt.title("Original Image")

#     # Resize and display each label's segmentation mask
#     for i, (label, mask) in enumerate(zip(labels, masks)):
#         # Resize the mask to the original image size
#         resized_mask = cv2.resize(mask, (original_width, original_height), interpolation=cv2.INTER_NEAREST)

#         plt.subplot(1, len(labels) + 1, i + 2)
#         plt.imshow(image)  # Display the original image
#         plt.imshow(resized_mask, cmap="jet", alpha=0.5)  # Overlay the resized mask
#         plt.axis("off")
#         plt.title(label)

#     plt.show()

# # # Main function
# if __name__ == "__main__":
#     image_path = "/home/jellylapubuntu/python/maps_3/cityscapes/leftImg8bit/leftImg8bit/train/aachen/aachen_000000_000019_leftImg8bit.png"  # Replace with your image path
#     labels = ["sidewalk", "road", "building","sky"]  # List of labels to detect

#     # Perform segmentation
#     labels, segmentation_masks = segment_with_labels(image_path, labels)

#     # Display the results
#     display_results(labels, segmentation_masks)

# TODO: cleanup the code