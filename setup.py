#!/usr/bin/env python
import sys
import os
from jupyter_client.kernelspec import install_kernel_spec
from IPython.utils.tempdir import TemporaryDirectory
from os.path import dirname,abspath
from shutil import copy as file_copy
from setuptools import setup, find_packages


# This script to easily install the kernel spec has been taken from
# the Sebastian Gutsche implementation of the Singular Jupyter kernel,
# which can be read here
#  https://github.com/sebasguts/jupyter_kernel_singular
def install_my_kernel_spec(user=True):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755) # Starts off as 700, not user readable
        path_of_file = dirname( abspath(__file__) )
        file_copy(path_of_file + "/kernel.js", td)
        file_copy(path_of_file + "/kernel.json", td)
        print('Installing Jupyter kernel spec')
        install_kernel_spec(td, 'IMikrokosmos', user=user, replace=True)

def main(argv=None):
    install_my_kernel_spec()

if __name__ == '__main__':
    main()
    
# pip setup
setup( name='imikrokosmos'
     , description='A Jupyter kernel for the mikrokosmos lambda interpreter'
     , version='0.1.2'
     , url='https://github.com/M42/jupyter-mikrokosmos'
     , author='Mario Román'
     , author_email='mromang08@gmail.com'
     , license='GPLv3'
     , packages=['mikrokosmoskernel']
     )
