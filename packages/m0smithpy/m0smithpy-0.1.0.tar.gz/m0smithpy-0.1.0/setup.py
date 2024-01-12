from setuptools import setup, find_packages
setup(
    name="m0smithpy",
    version="0.1.0",
    packages=find_packages(),
    description="Helper functions and missing functions from the Python core",
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"

    ], 
    python_requires=">=3.6"
)