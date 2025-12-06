# G.A.R.Y
This is Aden's storage for all G.A.R.Y related code 

**Open a port for Communication**

ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888

**Raspberry Pi Hotspot**

To turn on the hotspot run the following code:

  nmcli connection up MyHotspot
  
To autostart run: 

  nmcli connection modify Hotspot connection.autoconnect yes


To turn off the thotspot run the following code:

  nmcli connection down MyHotspot
