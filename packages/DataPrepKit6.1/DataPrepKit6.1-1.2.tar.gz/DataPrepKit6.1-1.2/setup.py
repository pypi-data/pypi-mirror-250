import setuptools
with open("README.md","r") as fh:
    long_description=fh.read()
setuptools.setup(
    name='DataPrepKit6.1',
    version='1.02',
    author='Asmaa.Said.Abdelmosef',
    description='a comprehensive toolkit  ',
    long_description=' this packge designed  to seamlessly read data from various file formats, provide a data summary, handle missing values, and encode categorical data. Please see README file to know how to use each function ',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ]

)