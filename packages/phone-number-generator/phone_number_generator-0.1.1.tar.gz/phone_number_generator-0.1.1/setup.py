import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def readme():
    with open('README.md') as f:
        return f.read()


about = {}
with open(os.path.join(here, 'phone_number_generator', '__version__.py'), 'r') as f:
    exec(f.read(), about)

setup(name=about['__title__'],
      version=about['__version__'],
      description=about['__description__'],

      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.12',
],
    keywords='All countries phone number generator',
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[

],
    scripts=[],
    zip_safe=False)
