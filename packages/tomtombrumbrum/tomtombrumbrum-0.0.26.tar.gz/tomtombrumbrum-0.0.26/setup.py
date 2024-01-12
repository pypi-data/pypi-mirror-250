
from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    LONG_DESCRIPTION = f.read()

VERSION = '0.0.26'
DESCRIPTION = 'TomTom API library'

# Setting up
setup(
    name="tomtombrumbrum",
    version=VERSION,
    author="Gabriele Trevisan",
    author_email="<gabriele.3vi@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'tomtom', 'api', 'drive'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)