from pathlib import Path
from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'Um facilitador para trabalhar com pickle files'
# para criar o packege
#python3 setup.py sdist bdist_wheel
# dist é o q fazemos o upload
# pip isntall twine
# twine upload dist/*

# Setting up
setup(
    name="picklefy",
    version=VERSION,
    author="Henrique Spencer)",
    author_email="<henriquespencer11@gmail.com>",
    description=DESCRIPTION,
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['pickle'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
)