from setuptools import setup, find_packages
from io import open
from os import path
import pathlib


# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text(encoding="utf-8")




setup(
    name='mudey-django',
    version='2.3',
    packages=find_packages(),
    description='CLI Django',
    author='Espero-Soft Informatiques',
    author_email='contact@espero-soft.com',
    long_description=README,
    long_description_content_type='text/markdown',
    # url='lien_vers_le_code_source',
    entry_points={
        'console_scripts': [
            'mudey-django = package.module:main',
        ],
    },
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'annotated-types>=0.6.0',
        'Django>=5.0',
        'inflect>=7.0.0',
        'questionary>=2.0.1',
        'colorama>=0.4.6'
    ],
)
