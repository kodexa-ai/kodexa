import pytest

from kodexa.testing import ExtensionPackUtil, OptionException, TestAction


def test_action_from_extension_pack():
    util = ExtensionPackUtil('tests/kodexa-action.yml')
    my_action = util.get_step('my-action')
    assert type(my_action) is TestAction


def test_valid_option():
    util = ExtensionPackUtil('tests/kodexa-action.yml')
    my_action = util.get_step('my-action', {'cheese': 'goo'})
    assert type(my_action) is TestAction


def test_invalid_option():
    with pytest.raises(OptionException):
        util = ExtensionPackUtil('tests/kodexa-action.yml')
        my_action = util.get_step('my-action', {'nocheese': 'goo'})
        assert type(my_action) is TestAction


def test_to_dict():
    util = ExtensionPackUtil('tests/kodexa-action.yml')
    my_action = util.get_step('my-action', {'cheese': 'goo'})
    action_dict = my_action.to_dict()
    assert action_dict['ref'] == "./my-action"
    assert action_dict['options'] == {'cheese': 'goo'}
