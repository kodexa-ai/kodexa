Getting Started
============


Installation
-----------

You can install Kodexa using the pip command

    pip install kodexa

This will provide both the Python library to allow you to work with Kodexa Documents and an instance or Kodexa
as well as the command-line interface.

Connecting to your Kodexa Instance
----------

You connect to your Kodexa instance using an instance of the KodexaClient class.

.. code-block::

    from kodexa import *
    client = KodexaClient(url='https://app.kodexa.com','<API_TOKEN>')

