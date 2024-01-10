from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="py-adspower",
    version="1.1",
    author="x2ice",
    author_email="q3fjq4u5@duck.com",
    description="This library implements AdsPower API specification",
    url="https://github.com/x2ice/py-adspower",
    packages=find_packages(),
    install_requires=["requests>=2.25.1"],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="adspower api",
    python_requires=">=3.8",
)
