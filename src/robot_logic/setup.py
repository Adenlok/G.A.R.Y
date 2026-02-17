import os
from glob import glob
from setuptools import setup

package_name = 'robot_logic'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aden',
    maintainer_email='aden@todo.todo',
    description='Brain node for robot control',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # CHANGE 'brain_node' below to match your filename!
            'brain = robot_logic.robot_logic:main',
        ],
    },
)