FROM dustynv/ros:melodic-ros-base-l4t-r32.7.1



RUN apt-get update && apt-get install -y apt-utils && apt-get install -y curl


RUN DEBIAN_FRONTEND=noninteractive apt-get install -y ros-$ROS_DISTRO-filters ros-$ROS_DISTRO-joint-state-publisher ros-$ROS_DISTRO-robot-localization ros-$ROS_DISTRO-rtabmap-ros  ros-$ROS_DISTRO-depth-image-proc libuvc-dev 

WORKDIR /work/ros_ws

# copy source code
COPY /src src

# install dependencies
RUN bash -c 'source /ros_entrypoint.sh && rosdep install --from-paths src -r -y || true'
RUN sudo apt-get install -y ros-melodic-joy*
RUN apt-get install -y python-catkin-tools
RUN apt-get install -y libpcap-dev  
RUN apt-get install -y tmux && apt-get install -y vim && apt-get install -y git apt-get install -y alsa-utils
WORKDIR /work
