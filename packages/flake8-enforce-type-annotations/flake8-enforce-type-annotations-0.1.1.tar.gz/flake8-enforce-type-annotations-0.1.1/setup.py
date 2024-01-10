from setuptools import setup, find_packages
from enforce_type_annotations.checker import Plugin


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="flake8-enforce-type-annotations",
    version=Plugin.version,
    author="Siva Narayanan",
    author_email="siva@fylehq.com",
    description="Flake8 plugin for enforcing type annotations.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["flake8", "type", "python", "enforce", "annotations"],
    url="https://github.com/fylein/flake8-kwargs-enforcer",
    packages=find_packages(
        include=["enforce_type_annotations*"]
    ),
    install_requires=[
        "flake8==7.0.0"
    ],
    entry_points={
        "flake8.extension": [
            "ETA = enforce_type_annotations.checker:Plugin",
        ],
    },
    classifiers=[
        "Topic :: Internet :: WWW/HTTP",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)