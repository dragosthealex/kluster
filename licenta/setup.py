from setuptools import setup

setup(name='Kluster',
      version='1.0',
      description='Kluster licenta',
      author='Jon Barbaru',
      author_email='jonbarbaru@gmail.com',
      packages=['licenta'],
      entry_points={
        'console_scripts': [
            'client=licenta.client:main',
            'provider_server=licenta.provider_server:main',
            'tracker=licenta.tracker:main'
        ],
      }
      )
