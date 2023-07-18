import json
import os

from kodexa.model import Taxonomy
from kodexa.platform.client import TaxonomyEndpoint


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def test_serialization():
    taxonomy_json = open(os.path.join(get_test_directory(), 'example-taxonomy.json'), 'rb').read()

    taxonomy_dict = json.loads(taxonomy_json)

    def update_name(taxon):
        taxon['name'] = taxon['id']
        taxon['externalName'] = taxon['id']
        for child in taxon['children']:
            update_name(child)

    for taxon in taxonomy_dict['taxons']:
        update_name(taxon)

    taxonomy = TaxonomyEndpoint.model_validate(taxonomy_dict)

    assert taxonomy.find_taxon_by_path(
        '5a9f6c65-8226-4ac6-925b-a1fe91683e7c/4241d1ac-38eb-448b-a28c-9ba69f2f33de').label == 'TrancheName'

    new_taxonomy = Taxonomy.model_validate(taxonomy.dict())

    print(json.dumps(new_taxonomy.dict(), indent=4))
