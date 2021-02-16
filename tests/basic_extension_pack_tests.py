from kodexa.testing import ExtensionPackUtil


def test_action_from_extension_pack():
    util = ExtensionPackUtil('kodexa-action.yml')
    my_action = util.get_step('my-action')
    assert my_action.get_name() == 'Hello'
