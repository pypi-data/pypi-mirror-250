import setuptools
with open("README.md","r") as fh:
    long_description=fh.read()
setuptools.setup(
    name='DataPrepKit5',
    version='1.5',
    author='Asmaa.Said.Abdelmosef',
    description='a comprehensive toolkit  ',
    long_description=' hi this packge for you ',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ]

)