'''
:Author: Anil Gautam
:Contact: anilgautam1987@gmail.com
:Updated: Mon 20, 2017
'''

from distutils import core

core.setup(
  name='app_count',
  version='1.1.0',
  description='app count setup',
  author='Anil Gautam',
  author_email='anilgautam1987@gmail.com',
  url='https://github.com/anilgautam1987/apps_count.git',
  package_dir={},
  packages=[],
  scripts=[],
  data_files=[],
  install_requires=['requests=2.18.4',
                    'Flask=0.12.2',
                    'prettytable-0.7.2',
                    ],
)