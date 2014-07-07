import os.path

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()

setup(name='iucr',
      version='0.0.1',
      description='Python package for working with Illinois Uniform Crime Reporting (IUCR) data.',
      long_description=readme,
      author='Geoff Hing',
      author_email='geoffhing@gmail.com',
      url='https://github.com/sc3/python-iucr',
      packages=['iucr'],
      package_data={'iucr': ['data/*.csv']},
      include_package_data=True,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          ],
     )
