import pytest

from kodexa.testing import ExtensionPackUtil, OptionException


def test_action_from_extension_pack():
    util = ExtensionPackUtil('tests/kodexa-action.yml')
    my_action = util.get_step('my-action')
    assert my_action.get_name() == 'Hello'


def test_valid_option():
    util = ExtensionPackUtil('tests/kodexa-action.yml')
    my_action = util.get_step('my-action', {'cheese': 'goo'})
    assert my_action.get_name() == 'Hello'


def test_invald_option():
    with pytest.raises(OptionException):
        util = ExtensionPackUtil('tests/kodexa-action.yml')
        my_action = util.get_step('my-action', {'nocheese': 'goo'})
        assert my_action.get_name() == 'Hello'
