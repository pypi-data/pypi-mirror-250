from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ascii_ye',
    version='0.1',
    packages=['ascii_ye'],
    author="SamiSoft - Yemen",
    url="https://github.com/mr-sami-x/ascii_ye",
    description="ASCII_YE ​​is a library that encodes text with the ASCII type, a digital encoding used to encrypt data when making requests over the Internet.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)
