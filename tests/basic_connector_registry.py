import tempfile

from kodexa import connectors


def test_connector_registry():
    print(connectors.get_connectors())
    connector = connectors.get_connector("folder", {"path": tempfile.gettempdir()})

    assert connector is not None
    print(connector)
