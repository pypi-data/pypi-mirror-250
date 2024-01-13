import os

from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize


def get_ext(package: str, package_path: str, file: str) -> Extension:
    name = f"{package}.{file}".replace(".py", "")
    file = os.path.join(package_path, file)

    return Extension(name=name, sources=[file], language="c++")


packages = find_packages()

ext_modules = []

for package in packages:
    package_path = package.replace(".", os.path.sep)

    ext_modules.extend(
        [
            get_ext(package, package_path, file)
            for file in os.listdir(package_path)
            if file.endswith(".py")
        ]
    )

with open("requirements.txt") as fp:
    install_requires = fp.read().strip().split("\n")

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="proalgotrader_core",
    version="0.0.9.beta4",
    description="ProAlgoTrader core",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krunaldodiya/proalgotrader_core",
    author="Krunal Dodiya",
    author_email="kunal.dodiya1@gmail.com",
    ext_modules=cythonize(ext_modules),
    package_data={"core": ["*.so", "*/__init__.py"]},
    include_package_data=True,
    exclude_package_data={"core": ["*.py", "*.cpp", "__pycache__", "project"]},
    install_requires=install_requires,
)
