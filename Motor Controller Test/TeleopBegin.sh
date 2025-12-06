#!/bin/bash

ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888 &

python3 L298n.py