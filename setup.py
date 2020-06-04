from setuptools import setup, find_packages

setup(name='seeCer',
      version=2.0,
      author='oimq',
      url='https://github.com/oimq/seeCer',
      author_email='taep0q@gmail.com',
      description='Search the data from HBase',
      packages=find_packages(),
      install_requires=['happybase', 'elasticsearch'],
      zip_safe=False
      )