from setuptools import setup

setup(name='git_collate',
      version='0.1.0',
      packages=['git_collate'],
      entry_points={
          'console_scripts': [
              'git-collate=git_collate.collate:collate'
          ]
      },
      )
