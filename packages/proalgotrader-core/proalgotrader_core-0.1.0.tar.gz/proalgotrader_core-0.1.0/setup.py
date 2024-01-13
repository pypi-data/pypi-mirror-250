from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as fp:
    install_requires = fp.read().strip().split("\n")

setup(
    name="proalgotrader_core",
    version="0.1.0",
    description="ProAlgoTrader core",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krunaldodiya/proalgotrader_core",
    author="Krunal Dodiya",
    author_email="kunal.dodiya1@gmail.com",
    include_package_data=True,
    package_data={"": ["*.so"]},
    packages=find_packages(exclude=["project"]),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
