from setuptools import setup
from setuptools import find_packages
from crpack import VERSION, AUTHOR

setup(
    name="crpack",
    version=VERSION,
    description="Quick start to create a package",
    author=AUTHOR,
    install_requires=["argparse"],
    packages=find_packages(exclude=("tests*", "testing*")),
    entry_points={
        "console_scripts": [
            "crpack = crpack.crpack:main",
        ],
    },
)
