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

