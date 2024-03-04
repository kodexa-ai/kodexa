from kodexa import KodexaPlatform


def test_token_handling():
    KodexaPlatform.set_access_token('test-token')
    KodexaPlatform.set_url('https://test.test.com')

    assert KodexaPlatform.get_access_token() == 'test-token'
    assert KodexaPlatform.get_url() == 'https://test.test.com'

    client = KodexaPlatform.get_client()
    assert client.access_token == 'test-token'
    assert client.base_url == 'https://test.test.com'
