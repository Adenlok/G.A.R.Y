# G.A.R.Y
This is Aden's storage for all G.A.R.Y related code 
**New Beginning Sequence**
1. Open Com Ports
```[bash]
sudo chmod 666 /dev/ttyACM0
sudo chmod 666 /dev/ttyUSB0
```

This allows for com devices to have permission to send and receive data make sure to check these are the correct com addressess if not you can check with 
```[bash]
ls /dev/ttyUSB* /dev/ttyACM*
```

2. Source ROS
3. ```[bash]
source /opt/ros/humble/setup.bash
cd ~/ros2_humble
source install/setup.bash
```
this make sure that all ros functions are enabled

3.Run the code
```[bash]
ros2 launch motor_control gary_launch.py
```
this launches the central brains of gary


Extras:
Make sure esp launchs after the rest of code reset by pressing EN button











