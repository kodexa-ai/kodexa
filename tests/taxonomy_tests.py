import json
import os

from kodexa.model import Taxonomy


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def test_serialization():
    taxonomy_json = open(os.path.join(get_test_directory(), 'example-taxonomy.json'), 'rb').read()

    taxonomy_dict = json.loads(taxonomy_json)
    def update_name(taxon):
        taxon['name'] = taxon['id']
        for child in taxon['children']:
            update_name(child)

    for taxon in taxonomy_dict['taxons']:
        update_name(taxon)

    taxonomy = Taxonomy.parse_obj(taxonomy_dict)


    new_taxonomy = Taxonomy.parse_obj(taxonomy.dict())

    print(json.dumps(new_taxonomy.dict()))
