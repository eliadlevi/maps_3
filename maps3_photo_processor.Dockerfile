FROM osrf/ros:humble-desktop

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

RUN pip install torch transformers

WORKDIR /ros2_ws

# Copy only the shared_interfaces package
COPY src/shared_interfaces src/shared_interfaces

# Copy only the maps3-image-mapper package
COPY src/maps3-photo-processor src/maps3-photo-processor

RUN . /opt/ros/humble/setup.sh && colcon build

# Source ROS 2 setup files
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "source /ros2_ws/install/setup.bash" >> ~/.bashrc
SHELL ["/bin/bash", "-c"]

# Run the ROS 2 node
CMD ["/bin/bash", "-c", "source /opt/ros/humble/setup.bash && source /ros2_ws/install/setup.bash && ros2 run maps3-photo-processor image_processing"]
