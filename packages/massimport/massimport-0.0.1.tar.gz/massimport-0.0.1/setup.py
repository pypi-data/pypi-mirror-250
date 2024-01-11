from setuptools import setup, find_packages
import os
os.system('export PYTHONPATH=~/module')

def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='massimport',
  version='0.0.1',
  author='Nikita_G',
  author_email='zailox@mail.ru',
  description='This module make imports faster',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=['requests>=2.25.1', 'beautifulsoup4'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
#  project_urls={
 #   'GitHub': 'ZailoxTT'
  #},
  python_requires='>=3.6'
)
