FROM osrf/ros:humble-ros-base

# Install dependencies
RUN apt-get update && apt-get install -y python3-pip python3-colcon-common-extensions

# Copy the workspace
COPY ./your_ros2_workspace /ros2_ws

# Build the workspace
WORKDIR /ros2_ws
RUN . /opt/ros/humble/setup.sh && colcon build

# Source ROS 2 setup files
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "source /ros2_ws/install/setup.bash" >> ~/.bashrc
SHELL ["/bin/bash", "-c"]

# Run the ROS 2 node
CMD ["ros2", "run", "maps3-image-mapper", "image_mapper"]
