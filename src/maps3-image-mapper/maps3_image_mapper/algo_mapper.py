from transformers import SegformerFeatureExtractor, SegformerForSemanticSegmentation
import torch
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from sensor_msgs.msg import Image
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from std_msgs.msg import Float32MultiArray
from shared_interfaces.msg import SegmentationMask
from PIL import Image as PILImage

class AlgoMapper(Node):
    def __init__(self):
        super().__init__("AlgoMapper")
        self.subscription = self.create_subscription(SegmentationMask, 'processed_image_topic', self.segmentation_callback, 10)
        self.get_logger().info("AlgoMapper Node Initialized")

    def segmentation_callback(self, msg):
        self.get_logger().info("Segmentation received")

        # Extract message data
        height, width, num_labels = msg.height, msg.width, msg.num_labels
        segmentation_masks = np.array(msg.data, dtype=np.float32).reshape((num_labels, height, width))
        self.get_logger().info("Segmentation masks reshaped")

        # Combine all masks into a single mask using argmax
        combined_mask = np.argmax(segmentation_masks, axis=0)  # Shape: (height, width)

        # Load the original image
        image_path = "/home/jellylapubuntu/python/maps_3/cityscapes/leftImg8bit/leftImg8bit/train/aachen/aachen_000035_000019_leftImg8bit.png"
        image = PILImage.open(image_path).convert("RGB")
        original_width, original_height = image.size  # Get original image size
        
        resized_mask = cv2.resize(combined_mask, (original_width, original_height), interpolation=cv2.INTER_NEAREST)

        # Display the combined segmentation mask over the original image
        plt.figure(figsize=(15, 10))
        plt.imshow(image, alpha=0.8)  # Original image with transparency
        plt.imshow(resized_mask, alpha=0.5, cmap="tab20")  # Combined segmentation mask overlay
        plt.colorbar(label="Class Index")  # Color bar showing class indices
        plt.axis("off")
        plt.title("Combined Segmentation Mask")
        plt.show()
