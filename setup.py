import sys
from codecs import open
from os import path
from setuptools import setup, find_packages

install_requires = [
    'grpcio',
    'grpcio-tools',
    'googleapis-common-protos'
]
exclude_packages = ['tests']

MAJOR = sys.version_info[0]
MINOR = sys.version_info[1]

# only include the async grpc client for python 3.6+
if MAJOR == 3 and MINOR >= 6:
    install_requires.append('aiogrpc')
else:
    # exclude the async_client
    exclude_packages.append('*.aio')

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lndgrpclib',
    packages=find_packages(exclude=exclude_packages),
    install_requires=install_requires,
    python_requires='>=3.8',
    version='0.6.8',
    description='An GRPC Client Library for LND (Lightning Network Deamon)',
    long_description=long_description,
    author='Mintblok',
    author_email='stub@mintblok.com',
    url='https://github.com/mintblok/lndgrpc',
    download_url='https://mintblock.net/project/lndgrpc.0.6.8.tar.gz',
    keywords=['lndgrpc', 'lnd grpc', 'lnd grpc lib', 'lnd grpc library', 'lnd grpc client', 'lnd grpc python', 'lightning network daemon grpc', 'lightning network daemon python', 'bitcoin lightning network daemon'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',        
    ],
)
