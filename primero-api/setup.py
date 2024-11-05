from setuptools import setup, find_packages

import os
import re

def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'primero_api','version.py')
    with open(version_file) as f:
        version_line = f.read().strip()
        version_match = re.match(r"^__version__ = ['\"]([^'\"]*)['\"]", version_line)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")


setup(
    name='primero-api',
    version=get_version(),
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        'requests',
        'requests-cache',
        'requests-ratelimiter',
        'pandas',
        'pyarrow',
        'python-slugify',
    ],
    # development dependencies
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'pytest-mock',
            'flake8',
            'black',
            'isort',
            'mypy',
            'sphinx',
            'sphinx_rtd_theme',
            'requests_mock'
        ]
    },
    author='merlos',
    author_email='merlos@users.github.com',
    description='A simple client for consuming data from Primero API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/unicef/magasin-primero-paquet',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)