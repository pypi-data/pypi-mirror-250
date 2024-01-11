from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="pts_keysight_e36154a_psu",
    version="0.0.2",
    author="Pass testing Solutions GmbH",
    description="Keysight E36154A PSU Driver and Diagnostic Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="shuparna@pass-testing.de",
    url="https://gitlab.com/pass-testing-solutions/keysight-e36154a-psu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    py_modules=["pts_keysight_e36154a_psu"],
    install_requires=["pyvisa==1.12.0", "pyvisa-py==0.5.3"],
    packages=find_packages(include=['pts_keysight_e36154a_psu']),
    include_package_data=True,
)
