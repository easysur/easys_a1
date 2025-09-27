import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'easys_ros'

data_files = [
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
]

launch_files = glob(os.path.join('launch', '*.py'))
if launch_files:
    data_files.append(('share/' + package_name + '/launch', launch_files))

config_files = glob(os.path.join('config', '*'))
if config_files:
    data_files.append(('share/' + package_name + '/config', config_files))

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(include=[package_name, package_name + '.*']),
    data_files=data_files,
    install_requires=['setuptools', 'adafruit-circuitpython-pca9685'],
    zip_safe=True,
    maintainer='egrt1',
    maintainer_email='egrt1@todo.todo',
    description='Easys A1 robot control nodes and launch files for ROS 2.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joy2cmd = easys_ros.joy2cmd:main',
            'thruster_controller = easys_ros.thruster_controller:main',
            'easys_controller = easys_ros.easys_controller:main',
            'thruster_output_converter = easys_ros.thruster_output_converter:main',
            'arm_controller = easys_ros.arm_controller:main',
            'light_controller = easys_ros.light_controller:main',
        ],
    },
)
