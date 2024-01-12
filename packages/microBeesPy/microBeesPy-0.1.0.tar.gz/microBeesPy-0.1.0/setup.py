from setuptools import find_packages, setup
import os
import sys
here = lambda *a: os.path.join(os.path.dirname(__file__), *a)

readme = open(here('README.md')).read()
requirements = [x.strip() for x in open(here('requirements.txt')).readlines()]

setup(
    name='microBeesPy',
    packages=find_packages(),
    version='0.1.0',
    long_description=readme,
    keywords='microbees',
    long_description_content_type="text/markdown",
    description='microBees Python Library',
    author_email="developers@microbees.com",
    author='@microBeesTech',
    url='https://github.com/microBeesTech/pythonSDK/',
    license='MIT',
    install_requires=requirements,
    zip_safe=False,
    platforms=["any"],
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["microBeesPy"],                    # Name of the python package
)