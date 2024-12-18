from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('ImagePublisher')
        self.publisher = self.create_publisher(Image, 'image_topic', 10)
        self.timer = self.create_timer(5.0, self.publish_image)  # Publish every 30 second
        self.bridge = CvBridge()
        self.image_path = './src/maps3-image-sender/resource/aachen_000157_000019_leftImg8bit.png'
        self.get_logger().info('ImagePublisher Node started.')

    def publish_image(self):
        # Read the image from a file
        cv_image = cv2.imread(self.image_path)
        if cv_image is None:
            self.get_logger().error(f'Could not load image from {self.image_path}')
            return

        try:
            # Convert the OpenCV image to a ROS Image message
            ros_image = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')
            self.publisher.publish(ros_image)
            self.get_logger().info('Published image.')
        except Exception as e:
            self.get_logger().error(f'Failed to publish image: {e}')
