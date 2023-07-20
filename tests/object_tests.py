from kodexa.model.objects import Store
from kodexa.platform.client import StoreEndpoint


def test_store_ref():
    store = StoreEndpoint(ref='test', type="store", slug="test", name="test")

    assert 'ref' in store.to_dict()
