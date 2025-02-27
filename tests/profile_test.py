from kodexa import KodexaClient, KodexaPlatform
import os

def test_profile_default():
    """
    :assert: Checks if the default profile is set correctly
    """
    kodexa_url = os.getenv("URL") or "https://test.test.com"
    access_token = os.getenv("ACCESS_TOKEN") or "test-token"
    KodexaPlatform.configure(kodexa_url, access_token)
    assert KodexaPlatform.get_url() == kodexa_url and KodexaPlatform.get_access_token() == access_token


def test_profile_custom():
    """
    :assert: Checks if the custom profile is set correctly
    """
    kodexa_url = os.getenv("URL") or "https://test.test.com"
    access_token = os.getenv("ACCESS_TOKEN") or "test-token"
    profile = "dev-profile"
    KodexaPlatform.configure(kodexa_url, access_token, profile)
    assert KodexaPlatform.get_url(profile) == kodexa_url and KodexaPlatform.get_access_token(profile) == access_token


def test_kodexa_client_default_profile():
    kodexa_cli = KodexaClient()
    assert kodexa_cli.base_url == KodexaPlatform.get_url("default") and \
           kodexa_cli.access_token == KodexaPlatform.get_access_token("default")


def test_kodexa_client_custom_profile():
    kodexa_cli = KodexaClient(profile="dev-profile")
    assert kodexa_cli.base_url == KodexaPlatform.get_url("dev-profile") and \
           kodexa_cli.access_token == KodexaPlatform.get_access_token("dev-profile")


def test_customized_kodexe_client():
    kodexa_url = "https://test.test.com"
    access_token = "test-token"
    kodexa_cli = KodexaClient(kodexa_url, access_token)
    assert kodexa_cli.base_url == KodexaPlatform.get_url() and kodexa_cli.access_token == KodexaPlatform.get_access_token()
