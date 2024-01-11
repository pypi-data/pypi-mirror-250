#!/usr/bin/env python
import re
from pathlib import Path

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with Path(__file__).parent.joinpath(*names).open(encoding=kwargs.get("encoding", "utf8")) as fh:
        return fh.read()


setup(
    name="luis-v-subtitler",
    version="0.1.9",
    license="MIT",
    description="A Python package to use AI to subtitle any video in any language",
    long_description="{}\n{}".format(
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub("", read("README.rst")),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author="Luis Antonio VASQUEZ REINA",
    author_email="luis.vasquez.work.contact@gmail.com",
    url="https://github.com/LuisAVasquez/python-luis-v-subtitler",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[path.stem for path in Path("src").glob("*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        # uncomment if you test on these interpreters:
        # "Programming Language :: Python :: Implementation :: IronPython",
        # "Programming Language :: Python :: Implementation :: Jython",
        # "Programming Language :: Python :: Implementation :: Stackless",
        "Topic :: Utilities",
    ],
    project_urls={
        "Documentation": "https://python-luis-v-subtitler.readthedocs.io/",
        "Changelog": "https://python-luis-v-subtitler.readthedocs.io/en/latest/changelog.html",
        "Issue Tracker": "https://github.com/LuisAVasquez/python-luis-v-subtitler/issues",
    },
    keywords=[
        # eg: "keyword1", "keyword2", "keyword3",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click",
        "moviepy==1.0.3",
        "pytube==15.0.0",
        "torch==1.13.1",
        "torchvision==0.14.1",
        "torchaudio==0.13.1",
        "torchtext==0.14.1",
        "torchdata==0.5.1",
        "pydub==0.25.1",
        "openai-whisper==20231117",
        "speechbrain==0.5.16",
        "accelerate==0.25.0",
        "optimum==1.16.0",
        # eg: "aspectlib==1.1.1", "six>=1.7",
    ],
    dependency_links=["git+https://github.com/m-bain/whisperX.git@e9c507ce5dea0f93318746411c03fed0926b70be"],
    extras_require={
        # eg:
        #   "rst": ["docutils>=0.11"],
        #   ":python_version=="2.6"": ["argparse"],
    },
    entry_points={
        "console_scripts": [
            "luis-v-subtitler = luis_v_subtitler.cli:main",
        ]
    },
)
