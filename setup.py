#!/usr/bin/env python

import os

from setuptools import setup

dir_path = os.path.dirname(os.path.realpath(__file__))
version_file = open(os.path.join(dir_path, 'VERSION'))
version = version_file.read().strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='kodexa',
      version=version,
      author='Kodexa',
      description='Kodexa Content Framework',
      author_email='support@kodexa.io',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://www.github.com/kodexa-ai/kodexa',
      packages=['kodexa', 'kodexa.connectors', 'kodexa.mixins', 'kodexa.sinks', 'kodexa.pipeline',
                'kodexa.stores', 'kodexa.model', 'kodexa.extractors', 'kodexa.steps', 'kodexa.cloud', 'kodexa_cloud',
                'kodexa_cloud'],
      install_requires=[
          'addict==2.2.1',
          'requests==2.23.0',
          'msgpack==1.0.0',
          'urllib3==1.25.8',
          'pydantic==1.4'
      ],
      setup_requires=["pytest-runner"],
      tests_require=["pytest"])
