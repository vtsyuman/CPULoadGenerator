from setuptools import setup
import os
description_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.rst')
with open(description_file) as df:
    description = df.readlines()
setup(
    name='cpu_loader',
    version='0.1.0',
    description=description,
    packages=['cpu_loader'],
    install_requires=['matplotlib', 'psutil', 'PyVirtualDisplay']  # apt-get install python3-tk Xvfb
)
