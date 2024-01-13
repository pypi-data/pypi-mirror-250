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

setup(
    name="proalgotrader_core",
    version="0.0.9.beta1",
    ext_modules=cythonize(ext_modules),
    package_data={"core": ["*.so"]},
    include_package_data=True,
    exclude_package_data={"core": ["*.py", "*.cpp", "__pycache__"]},
    install_requires=install_requires,
)
