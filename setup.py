import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smesx-python-interface", # Replace with your own username
    version="0.0.1",
    author="Maciejeg",
    author_email="maciek.majek2@gmail.com",
    description="A small package for sending sms via smskom's SmesX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Maciejeg/SmesX-Python-Interface",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)