from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

with open("README.md" , "r") as f:
  long_description = f.read()
  
setup(
  name='bstq',
  version='1.0.1',
  description='Comphrensive Library for Binary Search Trees.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/omkashyap007/Binary-Search-Tree-Library/tree/master',  
  author='Om Kashyap',
  author_email='omkashyapcric@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='bst,binary search tree,binarytree,binary tree', 
  packages=find_packages(),
  install_requires=[''] 
)