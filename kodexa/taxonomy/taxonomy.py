import random
from typing import List


class Taxon:

    def __init__(self, name: str, color: str = None):
        self.name: str = name
        self.color = "#" + ("%06x" % random.randint(0, 0xFFFFFF)) if color is None else color
        self.children: List[Taxon] = []


class Taxonomy:

    def __init__(self):
        self.taxons: List[Taxon] = []

    def add_taxon(self, name: str):
        self.taxons.append(Taxon(name))
