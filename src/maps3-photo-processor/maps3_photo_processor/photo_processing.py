from transformers import SegformerFeatureExtractor, SegformerForSemanticSegmentation
import torch
from PIL import Image as PILImage
import matplotlib.pyplot as plt
import numpy as np
from sensor_msgs.msg import Image
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
import cv2
from std_msgs.msg import Int32MultiArray, MultiArrayDimension

class ImageProcessing(Node):
    def __init__(self):
        super().__init__("ImageProcessing")
        self.subscription = self.create_subscription(Image, 'image_topic', self.image_callback, 10)
        self.get_logger().info("ImageProcessing Node Initialized")
        self.publisher_ = self.create_publisher(Int32MultiArray, 'processed_image_topic', 10)
        self.bridge = CvBridge()

    def image_callback(self, msg):
        try:
            # Convert the ROS Image message to an OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            self.get_logger().info('Received image.')
            algo_result = self.image_algo_proccessing(cv_image)

            height, width = 256, 256

            # Create Int32MultiArray message
            array_algo_result = Int32MultiArray()
            array_algo_result.layout.dim.append(MultiArrayDimension(label="height", size=height, stride=width * height))
            array_algo_result.layout.dim.append(MultiArrayDimension(label="width", size=width, stride=width))
            array_algo_result.data = algo_result.flatten().tolist()  # Flatten the 2D array
            
            # Publish the message
            self.publisher_.publish(array_algo_result)
            self.get_logger().info("Published an algo results")

            # Display the image using OpenCV (optional)


        except Exception as e:
            self.get_logger().error(f'Failed to process image: {e}')

 
    def image_algo_proccessing(self, image):
        # Load pre-trained model and feature extractor
        model_name = "nvidia/segformer-b1-finetuned-cityscapes-1024-1024"
        feature_extractor = SegformerFeatureExtractor.from_pretrained(model_name)
        model = SegformerForSemanticSegmentation.from_pretrained(model_name)

        # Load and preprocess an image
        image_path = "/home/jellylapubuntu/python/maps_3/cityscapes/leftImg8bit/leftImg8bit/train/aachen/aachen_000035_000019_leftImg8bit.png"
        image = PILImage.open(image_path).convert("RGB")
        inputs = feature_extractor(images=image, return_tensors="pt")

        # Perform inference
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits  # Shape: [batch_size, num_classes, height, width]
            segmentation = torch.argmax(logits, dim=1).squeeze().cpu().numpy()
        
        return segmentation


        

