#!/usr/bin/env python3

import rclpy
from .algo_mapper import AlgoMapper

def main(args=None):
    rclpy.init(args=args)

    # node = ImageProcessingNode()
    node = AlgoMapper()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()
        


