from kodexa import KodexaClient


def test_basic_workspace_list():
    client = KodexaClient('https://dev1.kodexa.com', 'xxxx')

    doc_fam = # get a document family from a store
    workspace = client.workspaces.get('c5d7ca4d-bbc0-42ff-880c-1ee5a1be0ced')
    workspace.add_document_family(doc_fam)

    workspace.list_document_families()

    # There should be 1 there

    workspace.remove_document_family(doc_fam)

    workspace.list_document_families()

    # There should be 0 there


