from setuptools import setup, Extension

module0 = Extension('linked_list',
      sources = ['linked_list/pythonbind.cc'], 
      include_dirs = ['linked_list'],
      extra_compile_args=["-std=c++20"])  

setup(
      name = 'linklist',
      version = '1.6',
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
