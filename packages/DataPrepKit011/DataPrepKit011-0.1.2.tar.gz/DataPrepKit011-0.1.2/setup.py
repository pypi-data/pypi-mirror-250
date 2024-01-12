import setuptools
with open("README.md","r") as fh:
    long_description=fh.read()
setuptools.setup(
    name='DataPrepKit011',
    version='0.1.2',
    author='Asmaa.Said.Abdelmosef',
    description='a comprehensive toolkit  ',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ]

)