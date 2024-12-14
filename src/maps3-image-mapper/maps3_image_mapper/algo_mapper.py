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
from std_msgs.msg import Int32MultiArray

class AlgoMapper(Node):
    def __init__(self):
        super().__init__("AlgoMapper")
        self.subscription = self.create_subscription(Int32MultiArray, 'processed_image_topic', self.segmentation_callback, 10)
        self.get_logger().info("AlgoMapper Node Initialized")


    # def algo_result_mapper(self, msg):
    #     try:
    #         self.get_logger().info('Received algo.')

    #         # Visualize the numeric segmentation mask over the original image
    #         plt.figure(figsize=(15, 10))
    #         # plt.imshow(image, alpha=0.8)  # Original image with some transparency
    #         plt.imshow(msg, alpha=0.5, cmap="tab20")  # Segmentation overlay with colormap
    #         plt.colorbar(label="Class Index")  # Color bar for numeric class representation
    #         plt.axis("off")
    #         plt.title("Segmentation Mask (Numeric Overlay)")
    #         plt.show()


    #     except Exception as e:
    #         self.get_logger().error(f'Failed to process image: {e}')

    def segmentation_callback(self, msg):
            try:
                # Reconstruct 2D array from the flattened array
                height = msg.layout.dim[0].size
                width = msg.layout.dim[1].size
                segmentation = np.array(msg.data, dtype=np.int32).reshape((height, width))

                # Display the segmentation result using OpenCV
                # Optional: Apply colormap for better visualization
                color_segmentation = cv2.applyColorMap((segmentation * 10).astype(np.uint8), cv2.COLORMAP_JET)
                cv2.imshow('Segmentation Result', color_segmentation)
                cv2.waitKey(1)
                self.get_logger().info('Displayed segmentation result.')
            except Exception as e:
                self.get_logger().error(f'Failed to process segmentation: {e}')

        

