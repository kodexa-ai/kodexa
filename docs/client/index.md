
The Kodexa client is a Python class that you can use to interact with an instance of Kodexa.

The purpose of the client is to allow scripting of any tasks, however, it is also the foundation
on which all the current processing logic in Kodexa is built.

## Setting up Kodexa Client

By default, when you instantiate a Kodexa client it will connect to the Kodexa instance that has
been configured in your environment.

The client will use the following environment variables to determine the connection details:


* `KODEXA_URL` - The URL of the Kodexa instance
* `KODEXA_ACCESS_TOKEN` - The access token to use to connect to the Kodexa instance

You can also specify a different Kodexa instance to connect to.

```python
from kodexa.platform import KodexaClient

client = KodexaClient('https://my-kodexa-instance.com', 'xxxx-xxxx-xxxx-xxxx')
```

```api-parameters
Server URL, String, The URL of the server; it needs to include the protocol and port (if needed)
Access Token, String, The Access Token to use
```


