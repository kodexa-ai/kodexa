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
      packages=['kodexa', 'kodexa.connectors', 'kodexa.pipeline',
                'kodexa.model', 'kodexa.steps', 'kodexa.selectors',
                'kodexa.assistant', 'kodexa.platform', 'kodexa.testing', 'kodexa.cli'],
      install_requires=[
          'addict~=2.2.1',
          'requests',
          'msgpack~=1.0.0',
          'urllib3',
          'pyyaml',
          'ply',
          'click',
          'rich',
          'appdirs',
          'jsonpickle',
          'better_exceptions',
          'simpleeval',
          'pyfunctional',
          'pydantic_yaml'
      ],
      entry_points="""
        [console_scripts]
        kodexa=kodexa.cli.cli:cli
        """,
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 4 - Beta',

          # Indicate who your project is intended for.
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries',

          # Pick your license.  (It should match "license" above.)

          '''License :: OSI Approved :: Apache Software License''',  # noqa
          # noqa
          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3.9',
      ],
      package_data={
          # If any package contains *.j2
          '': ['*.j2', '*.j2.html'],
      },
      setup_requires=["pytest-runner"],
      tests_require=["pytest"])
