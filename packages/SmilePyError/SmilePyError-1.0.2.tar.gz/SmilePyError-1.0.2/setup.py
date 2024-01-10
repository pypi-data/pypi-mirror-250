#import setuptools
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="SmilePyError",
    version="1.0.2",
    author="Sitthykun LY",
    author_email="ly.sitthykun@gmail.com",
    description="python error class is, to make it simple structure",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/sitthykun/smilepyerror",
    packages=["smilepyerror"],
    include_package_data=True,
    classifiers=[
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
        	"Programming Language :: Python :: 3.11",
		"License :: OSI Approved :: MIT License",
        	"Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
    ],
)
