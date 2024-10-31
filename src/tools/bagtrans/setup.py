# Copyright (c) 2023, AgiBot Inc.
# All rights reserved.

from setuptools import setup

package_name = 'bagtrans'

with open("../VERSION", "r") as f:
    version = f.read().strip()

setup(
    name=package_name,
    app='bagtrans',
    version=version,
    author='Yu Guanlin',
    author_email='yuguanlin@agibot.com',
    description='transfer aimrt bag file to ros2 bag file',
    license='',
    entry_points={
        'console_scripts': [
            'bagtrans = bagtrans.main:main',
        ],
    },
    include_package_data=True,
)
