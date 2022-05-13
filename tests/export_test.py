import shutil

from kodexa import *
from kodexa.model.objects import Organization


def test_export():
    """Test export."""

    shutil.rmtree('/tmp/export_test')

    client = KodexaClient('https://dev1.kodexa.com', '60ad7b600f0a4565a8ee49330c8ce1a6')
    project = client.get_project('8a8a85687ffa6559017ffb7b256b00c8')
    client.export_project(project, '/tmp/export_test')

    import_test = client.organizations.find_by_slug('test-import')
    if import_test is not None:
        import_test.delete()

    organization = Organization(slug='test-import', name='Test Import')
    import_test = client.organizations.create(organization)

    client.import_project(import_test, '/tmp/export_test/Test Project')