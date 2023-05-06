if [ $# -eq 0 ]; then
    echo "usage: $0 <image_name> <interface>"
    exit
fi
IMAGE_NAME=$1
INTERFACE=$2
# spdp is important to avoid slowing down WiFi to 6Mbps (by avoiding multicast)
# check CYCLONE DDS doc for detail
# CYCLONEDDS_URI="<CycloneDDS><Domain><General><AllowMulticast>false</AllowMulticast><NetworkInterfaceAddress>"$INTERFACE"</NetworkInterfaceAddress></General><Discovery><Peers><Peer address=\"10.42.0.21\"/><Peer address=\"10.42.0.24\"/><Peer address=\"10.42.0.22\"/><Peer address=\"10.42.0.23\"/><Peer address=\"10.42.0.20\"/></Peers><ParticipantIndex>auto</ParticipantIndex><MaxAutoParticipantIndex>100</MaxAutoParticipantIndex></Discovery></Domain></CycloneDDS>"

# docker create -t --name ros2_wheeltec_robot -e CYCLONEDDS_URI=$CYCLONEDDS_URI --network host --ipc host --privileged --shm-size 8G -v `readlink -f ~/work-robot-local/ros2_wheeltec_robot/wheeltec-ros2-src/src`:/work/ros2_ws/src -v /dev:/dev $IMAGE_NAME bash
nvidia-docker create -t --name voice_robot -e CYCLONEDDS_URI=$CYCLONEDDS_URI --gpus all  --network host --ipc host --privileged --shm-size 8G -v `readlink -f ~/work-jm/wheeltec_robot/src`:/work/ros_ws/src -v /dev:/dev $IMAGE_NAME bash
