import os
from glob import glob
from setuptools import setup

package_name = 'motor_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # This line installs your launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aden',
    maintainer_email='aden@todo.todo',
    description='Motor control and bridge for Arduino',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # format: 'executable_name = package_name.file_name:main'
            'driver = motor_control.motor_node:main'
        ],
    },
)