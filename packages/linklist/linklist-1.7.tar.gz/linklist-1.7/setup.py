from setuptools import setup, Extension
import os 

name = os.name 
if name == 'nt': 
      args = ['/std:c++20']
else: 
      args = ['-std=c++20'] 

module0 = Extension('linked_list',
      sources = ['linked_list/pythonbind.cc'], 
      include_dirs = ['linked_list'],
      extra_compile_args=args
) 

setup(
      name = 'linklist',
      version = '1.7',
      description = 'Python package with a fast linked_list support. ',
      ext_modules = [module0],
      author = 'Cutie Deng',
      author_email = 'Dhdreamer@126.com', 
      url = 'https://github.com/CutieDeng/OrderStatisticTree',
      license = 'MIT',
      classifiers = [
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
      ],
      python_requires = '>=3.6',
)
