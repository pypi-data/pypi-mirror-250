from setuptools import find_packages, setup
from pathlib import Path
import codecs
types_of_encoding = ["utf8", "cp1252"]

setup(
    name="fprlib",
    version="1.1.0",
    description="Knjižnica za FPR",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description="https://github.com/DrKvass/fprlib",
    long_description_content_type="text/markdown",
    url="https://github.com/DrKvass/fprlib",
    author="Dr.Kvass",
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=["numpy","scipy","matplotlib","statistics","uncertainties"],
    python_required=">=3.11",
)
