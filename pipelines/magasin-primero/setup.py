from setuptools import find_packages, setup

import os
import re

def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'magasin_primero', 'version','version.py')
    with open(version_file) as f:
        version_line = f.read().strip()
        version_match = re.match(r"^__version__ = ['\"]([^'\"]*)['\"]", version_line)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")


setup(
    name="magasin_primero",
    version=get_version(),
    packages=find_packages(exclude=["magasin_primero_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-postgres",
        "pandas",
        "fsspec",  
        "s3fs",
        "adlfs", 
        "pyarrow",
        "primero-api"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
