#!/usr/bin/env python3

import rclpy
from .image_publisher import ImagePublisher

def main(args=None):
    rclpy.init(args=args)
    publisher = ImagePublisher()
    rclpy.spin(publisher)
    rclpy.shutdown()     


