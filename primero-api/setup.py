from setuptools import setup, find_packages

from primero_api.version import VERSION

setup(
    name='primero-api',
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        'requests',
        'requests-cache',
        'requests-ratelimiter',
        'pandas',
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