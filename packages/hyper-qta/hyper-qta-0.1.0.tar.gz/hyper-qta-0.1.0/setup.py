#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['test/']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


packages = [
    'hyper',
    'hyper.http20',
    'hyper.common',
    'hyper.http11',
]
BASE_DIR = os.path.realpath(os.path.dirname(__file__))
VERSION = "1.0.0"


def replace_version_py(version):
    version_py = os.path.join(BASE_DIR, 'hyper', '__init__.py')
    new_content = ""
    with open(version_py, 'r') as fd:
        content = fd.read()
        new_content = re.sub(r'[\'"](\d+\.\d+.\d+)[\'"]', "'{}'".format(version), content)
    with open(version_py, 'w') as fd:
        fd.write(new_content)


def generate_version():
    version = VERSION
    if os.path.isfile(os.path.join(BASE_DIR, "version.txt")):
        with open("version.txt", "r") as fd:
            content = fd.read().strip()
            if content:
                version = content
    replace_version_py(version)
    return version


def parse_requirements():
    reqs = []
    if os.path.isfile(os.path.join(BASE_DIR, "requirements.txt")):
        with open(os.path.join(BASE_DIR, "requirements.txt"), 'r') as fd:
            for line in fd.readlines():
                line = line.strip()
                if line:
                    reqs.append(line)
    return reqs


setup(
    name='hyper-qta',
    version=generate_version(),
    description='HTTP/2 Client for Python',
    long_description=open('README.rst').read() + '\n\n' + open('HISTORY.rst').read(),
    author='qta',
    url='http://hyper.rtfd.org',
    packages=packages,
    package_data={'': ['LICENSE', 'README.rst', 'CONTRIBUTORS.rst', 'HISTORY.rst', 'NOTICES', '*.txt', '*.TXT']},
    data_files=[(".", ["requirements.txt", "version.txt"])],
    package_dir={'hyper': 'hyper'},
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    install_requires=parse_requirements(),
    tests_require=['pytest', 'requests', 'mock'],
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'hyper = hyper.cli:main',
        ],
    },
    extras_require={
        'fast': ['pycohttpparser'],
        # Fallback to good SSL on bad Python versions.
        ':python_full_version < "2.7.9"': [
            'pyOpenSSL>=0.15', 'service_identity>=14.0.0'
        ],
        # PyPy with bad SSL modules will likely also need the cryptography
        # module at lower than 1.0, because it doesn't support CFFI v1.0 yet.
        ':platform_python_implementation == "PyPy" and python_full_version < "2.7.9"': [
            'cryptography<1.0'
        ],
        ':python_version == "2.7" or python_version == "3.3"': ['enum34>=1.0.4, <2']
    }
)
