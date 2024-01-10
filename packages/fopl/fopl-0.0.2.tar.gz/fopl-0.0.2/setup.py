from setuptools import setup, find_packages
import pathlib

setup(
    name='fopl',  # Required
    version='0.0.2',
    description='Application example showing Internazionale football players using tkinter and cURL',
    license='Apache 2.0 License',
    author='Martina Baiardi',
    author_email='m.baiardi@unibo.it',
    packages=find_packages(),  # Required
    include_package_data=True,
    platforms = "Independant",
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only'
    ],
)
