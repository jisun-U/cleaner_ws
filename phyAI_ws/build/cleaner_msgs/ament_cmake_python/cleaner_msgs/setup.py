from setuptools import find_packages
from setuptools import setup

setup(
    name='cleaner_msgs',
    version='0.0.1',
    packages=find_packages(
        include=('cleaner_msgs', 'cleaner_msgs.*')),
)
