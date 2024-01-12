from setuptools import setup

setup(name = 'hydromt_wff',
      version= '0.0.4',
      description= 'The package automates the pre-processing, data preparation, and set-up of Delft3D FM to simulate wadi flash floods',
      author= 'Aseel Moahmed',
      packages=['hydromt_wff'],
      package_data={'hydromt_wff': ['data/*.csv']},
      zip_safe=False)