# easys_a1
Easys is an open source underwater robot. This repository contains the hardware and ROS 2 software needed to control the platform.

[-> Document Page](https://hrjp.notion.site/Easys-A1-Document-211281df162280af8de3f84531e12f15)

## Software
### Target Environment
- Raspberry Pi 4 (4 GB RAM or higher) as the onboard computer
- Ubuntu 22.04
- ROS 2 Humble
If you are using Docker, the scripts under `setup_env/` provide build and run helpers.

### Install dependency packages (rasberry pi)
- [ms5837_bar_ros](git clone https://github.com/tasada038/ms5837_bar_ros)
- [bno055](https://github.com/flynneva/bno055)

### Install dependency packages (remote PC)
- [yolov8_ros](https://github.com/mgonzs13/yolov8_ros)
- [rviz_2d_overlay_plugins](https://github.com/teamspatzenhirn/rviz_2d_overlay_plugins)

### Installation (robot and remote PC)
```bash
cd <your_ros2_workspace>/src
git clone https://github.com/tamago117/easys_a1.git
cd ..
rosdep install --from-paths src --ignore-src -r -y
pip install -r src/easys_a1/requirements.txt
colcon build --symlink-install
```

### Launching
#### On the robot
```bash
ros2 launch easys_ros easys_control.launch.py
```

#### On the remote PC
```bash
ros2 launch easys_ros remote_control.launch.py
```

## Simulator
The Gazebo-based simulator is available at [Easys_sim](https://github.com/easysur/Easys_sim).
