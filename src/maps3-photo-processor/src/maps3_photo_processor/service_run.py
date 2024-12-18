#!/usr/bin/env python3

import rclpy
from .photo_processing import ImageProcessing

def main(args=None):
    rclpy.init(args=args)
    subscriber = ImageProcessing()
    rclpy.spin(subscriber)
    rclpy.shutdown()


