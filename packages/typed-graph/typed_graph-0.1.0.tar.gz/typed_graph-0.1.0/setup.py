import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='typed_graph',
    version='0.1.0',
    description = 'Staticly typed graph library',
    author='lcabyg',
    author_email = "lcabyg@build.aau.dk",
    long_description=read('README.md'),
    keywords = "lcabyg build LCAbyg lca",
    url='https://hg.buildsrv.dk/typed_graph/typed_graph',
    license_files = ('LICENSE',),
    packages=['typed_graph'],
    classifiers = [
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)