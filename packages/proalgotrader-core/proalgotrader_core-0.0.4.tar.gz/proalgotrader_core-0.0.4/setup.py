import os

from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize


def get_ext(name, file):
    print(name, file)
    return Extension(name=name, sources=[file], language="c++")


packages = find_packages()

ext_modules = []

for package in packages:
    package_path = package.replace(".", os.path.sep)
    ext_modules.extend([get_ext(package, os.path.join(package_path, file)) for file in os.listdir(package_path) if file.endswith(".py")])

setup(
    name='proalgotrader_core',
    version='0.0.4',
    ext_modules=cythonize(ext_modules),
    packages=find_packages(),
    package_data={'core': ['*.so', '*.cpp']},
    include_package_data=True,
    exclude_package_data={'core': ['*.py']},
    install_requires=[
        "python-dotenv"
    ],
    entry_points={
        'console_scripts': [
            'proalgotrader_core = core.main:main',
        ],
    },
)
