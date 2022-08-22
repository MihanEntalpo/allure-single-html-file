#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages


CMD = "allure-combine"
PACKAGE_NAME = "allure_combine"
CMD_FOR_SHORT = "ac"


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name=PACKAGE_NAME,
    version='1.0.8',
    author='MihanEntalpo, Sine.wang',
    author_email='mihanentalpo@yandex.ru, sinecelia.wang@gmail.com',
    maintainer='Sine.wang',
    maintainer_email='sinecelia.wang@gmail.com',
    license='MIT',
    url='https://github.com/MihanEntalpo/allure-single-html-file',
    description='Generate single HTML file from allure report.',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'build', 'dist']),
    package_data={"allure_combine": ["sinon-*.js"]},
    python_requires='>=3.6',
    install_requires=['bs4>=0.0.1'],
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            f'{CMD} = allure_combine.combine:main',
            f'{CMD_FOR_SHORT} = allure_combine.combine:main',
        ]
    },
)
