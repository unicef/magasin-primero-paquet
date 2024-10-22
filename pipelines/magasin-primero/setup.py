from setuptools import find_packages, setup

setup(
    name="magasin_primero",
    packages=find_packages(exclude=["magasin_primero_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
        "pandas",
        "fsspec",  
        "s3fs", 
        "primero-api"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
