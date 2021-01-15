import random
from typing import List, Optional


class Taxon:

    def __init__(self, label: str, name: str, id: Optional[str] = None, color: Optional[str] = None):
        self.id = id
        self.name: str = name
        self.label: str = label
        self.color = "#" + ("%06x" % random.randint(0, 0xFFFFFF)) if color is None else color
        self.children: List[Taxon] = []


class Taxonomy:

    def __init__(self, taxonomy_type='CONTENT', enabled=True):
        self.taxons: List[Taxon] = []
        self.taxonomy_type = taxonomy_type
        self.enabled = enabled

    def add_taxon(self, label: str, name: str):
        self.taxons.append(Taxon(label, name))


class RemoteTaxonomy:

    def __init__(self, ref: str):
        from kodexa import KodexaPlatform
        url = f"{KodexaPlatform.get_url()}/api/taxonomies/{ref.replace(':', '/')}"

        import requests
        response = requests.get(url,
                                headers={"x-access-token": KodexaPlatform.get_access_token(),
                                         "content-type": "application/json"})

        self.taxonomy_type = response.json()['taxonomyType']
        self.enabled = response.json()['enabled']

        self.taxons: List[Taxon] = []

        def build_taxons(json_taxons, taxons):
            for json_taxon in json_taxons:
                new_taxon = Taxon(label=json_taxon['label'], name=json_taxon['name'], id=json_taxon['id'],
                                  color=json_taxon['color'])

                if 'children' in json_taxon:
                    build_taxons(json_taxon['children'], new_taxon.children)

                taxons.append(new_taxon)

        build_taxons(response.json()['taxons'], self.taxons)
