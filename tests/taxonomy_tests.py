import json
import os

from kodexa import Taxonomy


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def test_serialization():
    taxonomy_json = open(os.path.join(get_test_directory(), 'example-taxonomy.json'), 'rb').read()
    taxonomy = Taxonomy.from_dict(json.loads(taxonomy_json))

    new_taxonomy = Taxonomy.from_dict(taxonomy.to_dict())

    print(json.dumps(new_taxonomy.to_dict()))
