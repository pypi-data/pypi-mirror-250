# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='progxec',
    version='0.1.8',
    author="Jaysheel",
    packages=find_packages(['progxec']),
    description="This python library can be used to call/execute other languages from python and store the results in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jaysheel-ops/progxec',
    install_requires=['os', 'subprocess'],
    python_requires=">=3.9",
)
