from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mdBuilder',
    version='1.0.2',
    packages=setuptools.find_packages(),
    url='https://github.com/mill413/mdWriter',
    license='MIT',
    author='Mill Haruto',
    author_email='mill413@outlook.com',
    description='A tool to generate markdown easily',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
