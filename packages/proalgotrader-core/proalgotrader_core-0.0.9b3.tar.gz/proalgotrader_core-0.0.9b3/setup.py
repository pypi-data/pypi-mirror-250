import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="proalgotrader_core",
    version="0.0.9.beta3",
    description="ProAlgoTrader core",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krunaldodiya/proalgotrader_core",
    author="Krunal Dodiya",
    author_email="kunal.dodiya1@gmail.com",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=[
        "python-dotenv"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
