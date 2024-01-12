import setuptools
with open("README.md","r") as fh:
    long_description=fh.read()
setuptools.setup(
    name='DataPrepKit6',
    version='1.6',
    author='Asmaa.Said.Abdelmosef',
    description='a comprehensive toolkit  ',
    long_description=' this packge designed design functions to seamlessly read data from various file formats, provide a data summary, handle missing values, and encode categorical data. Please see READme to know how to use each function ',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ]

)