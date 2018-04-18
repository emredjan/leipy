"""
A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='leipy',
    version='0.1.0',
    description='A python wrapper / client for GLEIF public API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/emredjan/leipy',
    author='emredjan',
    author_email='emredjan@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='lei gleif api api-wrapper',
    packages=find_packages(exclude=['tests*']),
    install_requires=['requests', 'python-dateutil'],
    python_requires='>=3.4',
)