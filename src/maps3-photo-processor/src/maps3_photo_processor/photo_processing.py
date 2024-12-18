from sensor_msgs.msg import Image
from rclpy.node import Node
from cv_bridge import CvBridge
from .clip_seg import ClipSegImageProcessing
from shared_interfaces.msg import SegmentationMask
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

class ImageProcessing(Node):
    def __init__(self):
        super().__init__("ImageProcessing")
        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            depth=10,
        )
        self.subscription = self.create_subscription(Image, 'image_topic', self.image_callback, qos)
        self.get_logger().info("ImageProcessing Node Initialized")
        self.publisher_ = self.create_publisher(SegmentationMask, 'processed_image_topic', qos)
        self.bridge = CvBridge()

    def image_callback(self, msg):
        self.get_logger().info("Got an image to process")

        labels = ["sidewalk", "road", "building","sky"]  # List of labels to detect

        try:

            # Convert the ROS Image message to an OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            self.get_logger().info('Received image.')
            segmentation_masks = ClipSegImageProcessing.segment_with_labels(cv_image, labels)

            num_labels, height, width = segmentation_masks.shape  # Extract dimensions
            flattened_mask = segmentation_masks.flatten().tolist()
            self.get_logger().info("algo finished running")

            outputMassage = SegmentationMask()
            outputMassage.height = height
            outputMassage.width = width
            outputMassage.num_labels = num_labels
            outputMassage.data = flattened_mask 

            self.publisher_.publish(outputMassage)
            self.get_logger().info("Published an algo results")
            
        except Exception as e:
            self.get_logger().error(f'Failed to process image: {e}')
 