import setuptools
with open("README.md","r") as fh:
    long_description=fh.read()
setuptools.setup(
    name='DataPrepKit4',
    version='1.3',
    author='Asmaa.Said.Abdelmosef',
    description='a comprehensive toolkit  ',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ]

)