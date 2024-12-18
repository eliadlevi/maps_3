import matplotlib.pyplot as plt
import numpy as np
from rclpy.node import Node
import cv2
from shared_interfaces.msg import SegmentationMask
from PIL import Image as PILImage
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy


class AlgoMapper(Node):
    def __init__(self):
        super().__init__("AlgoMapper")

        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            depth=10,
        )

        self.subscription = self.create_subscription(SegmentationMask, 'processed_image_topic', self.segmentation_callback, qos)
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
        image_path = './src/maps3-image-sender/resource/aachen_000157_000019_leftImg8bit.png'
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
