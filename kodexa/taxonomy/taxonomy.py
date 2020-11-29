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

    def __init__(self):
        self.taxons: List[Taxon] = []

    def add_taxon(self, label: str, name: str):
        self.taxons.append(Taxon(label, name))
