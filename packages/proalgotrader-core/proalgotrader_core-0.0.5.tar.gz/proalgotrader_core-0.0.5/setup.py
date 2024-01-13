import os

from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize


def get_ext(name: str, file: str) -> Extension:
    return Extension(name=name, sources=[file], language="c++")


packages = find_packages()

ext_modules = []

for package in packages:
    package_path = package.replace(".", os.path.sep)
    ext_modules.extend(
        [
            get_ext(package, os.path.join(package_path, file))
            for file in os.listdir(package_path)
            if file.endswith(".py")
        ]
    )

setup(
    name="proalgotrader_core",
    version="0.0.5",
    ext_modules=cythonize(ext_modules),
    packages=packages,
    package_data={"core": ["*.so"]},
    include_package_data=True,
    exclude_package_data={"core": ["*.py", "*.cpp"]},
    install_requires=["python-dotenv"],
    entry_points={
        "console_scripts": [
            "proalgotrader_core = core.main:main",
        ],
    },
)
