from setuptools import setup, find_packages

def get_version():
    return (open('primero_api/VERSION').read().strip())

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