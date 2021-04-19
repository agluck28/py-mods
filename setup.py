import setuptools

long_description =  "Collection of pacakges used to interface with mongo and influx databases"

setuptools.setup(
    name="doingthings",
    version="0.0.1",
    author="Me",
    description="Packages and Things",
    long_description=long_description,
    url="http://localhost",
    packages=setuptools.find_packages(),
    classifers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operation System :: OS Independent"
    ],
    python_requires='>=3.7',
)

if __name__ == "__main__":
    print(setuptools.find_packages())