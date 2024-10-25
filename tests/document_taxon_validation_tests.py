from kodexa import Document
from kodexa.model.objects import DocumentTaxonValidation, Taxon, Taxonomy, TaxonValidation


def test_taxon_validations():
    document = Document.from_text("Hello, world!")

    taxonomy = Taxonomy(type="taxonomy", name="Testing", slug="testing", version="1.0.0")
    person = Taxon(path="person", name="person", group=True)
    person_name = Taxon(path="person/name", name="name")
    person.children = [person_name]
    taxonomy.taxons = [person]

    validation_rule = TaxonValidation(name="NameRequired", description="Name is required", rule_formula="ifnull(name, '') != ''")
    document_validation = DocumentTaxonValidation(taxonomy_ref="test/test-taxonomy:1.0.0", taxon_path="person",
                                                  validation=validation_rule)

    document.set_validations([document_validation])

    validations  = document.get_validations()

    assert len(validations) == 1
    assert validations[0].taxonomy_ref == "test/test-taxonomy:1.0.0"
    assert validations[0].taxon_path == "person"
    assert validations[0].validation.name == "NameRequired"
    assert validations[0].validation.description == "Name is required"
    assert validations[0].validation.rule == "name is not None"
