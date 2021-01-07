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
