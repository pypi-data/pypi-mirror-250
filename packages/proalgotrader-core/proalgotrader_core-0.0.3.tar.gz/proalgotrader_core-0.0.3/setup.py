from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

ext_modules = Extension('core.*', ['core/*.py']),

setup(
    name='proalgotrader_core',
    version='0.0.3',
    ext_modules=cythonize(ext_modules),
    packages=find_packages(),
    package_data={'core': ['*.so']},
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
