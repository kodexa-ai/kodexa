---
title: Kodexa Client
---

The Kodexa client is a Python library that allows you to connect to a Kodexa instance and work with the resources, assistants and models
that are available.

# Installation

The client is available on [PyPi](https://pypi.org/project/kodexa/) and can be installed using pip:

```bash
pip install kodexa~=6.0.0b
```

# Setting up Kodexa Client

By default when you instantiate a Kodexa client it will connect to the Kodexa instance that has
been configured in your environment.

The client will use the following environment variables to determine the connection details:


* `KODEXA_URL` - The URL of the Kodexa instance
* `KODEXA_ACCESS_TOKEN` - The access token to use to connect to the Kodexa instance

You can also specify a different Kodexa instance to connect to.

```python
client = KodexaClient('https://my-kodexa-instance.com', 'xxxx-xxxx-xxxx-xxxx')
```

```api-parameters
Server URL, String, The URL of the server; it needs to include the protocol and port (if needed)
Access Token, String, The Access Token to use
```

# First Steps with the Client

Once you have a client you can start to work with the resources that are available on the server.

The client object has a number of methods that allow you to work with the resources that are available on the server, for
example if you want to work with organizations then you can use:

```python
client.orgnizations.list()
```
