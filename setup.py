import os
import uuid

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


with open('requirements.txt') as f:
    install_reqs = f.readlines()
    reqs = [str(ir) for ir in install_reqs]

with open(os.path.join(here, 'README.md')) as fp:
    long_description = fp.read()

setup(
    name='blockcertsonchaining',
    version='0.0.1',
    description='BlockChain-based issuing of Education Credentials',
    author='PAS',
    tests_require=[''],
    url='',
    license='MIT',
    author_email='',
    long_description=long_description,
    packages=find_packages(),
    install_requires=reqs
)
