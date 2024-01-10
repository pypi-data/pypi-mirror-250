from __future__ import print_function
from setuptools import setup, find_packages
import zzk

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="zzk",
    version=zzk.__version__,
    author="zhengzekang",
    author_email="1471616950@qq.com",
    description="zzk tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/damugongzai/zzk.git",
    py_modules=['zzk'],
    install_requires=[],
    classifiers=[
        "Topic :: Games/Entertainment ",
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Topic :: Games/Entertainment :: Board Games',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)