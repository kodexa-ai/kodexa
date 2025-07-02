from kodexa import Document
from kodexa.model.objects import (
    DocumentTaxonValidation, Taxon, Taxonomy, TaxonValidation
)


def test_taxon_validations():
    document = Document.from_text("Hello, world!")

    taxonomy = Taxonomy(
        type="taxonomy", name="Testing", slug="testing", version="1.0.0"
    )
    person = Taxon(path="person", name="person", group=True)
    person_name = Taxon(path="person/name", name="name")
    person.children = [person_name]
    taxonomy.taxons = [person]

    validation_rule = TaxonValidation(
        name="NameRequired",
        description="Name is required",
        rule_formula="ifnull(name, '') != ''"
    )
    document_validation = DocumentTaxonValidation(
        taxonomy_ref="test/test-taxonomy:1.0.0",
        taxon_path="person",
        validation=validation_rule
    )

    document.set_validations([document_validation])

    validations = document.get_validations()

    assert len(validations) == 1
    assert validations[0].taxonomy_ref == "test/test-taxonomy:1.0.0"
    assert validations[0].taxon_path == "person"
    assert validations[0].validation.name == "NameRequired"
    assert validations[0].validation.description == "Name is required"
    assert validations[0].validation.rule_formula == "ifnull(name, '') != ''"


def test_date_validation_rules():
    document = Document.from_text("Invoice Date: 2023-12-25")
    taxonomy = Taxonomy(
        type="taxonomy",
        name="DateTesting",
        slug="date-testing",
        version="1.0.0"
    )
    invoice = Taxon(path="invoice", name="invoice", group=True)
    invoice_date = Taxon(path="invoice/date", name="date", taxon_type="DATE")
    due_date = Taxon(
        path="invoice/duedate", name="duedate", taxon_type="STRING"
    )
    birth_date = Taxon(
        path="invoice/birthdate", name="birthdate", taxon_type="DATE"
    )
    invoice.children = [invoice_date, due_date, birth_date]
    taxonomy.taxons = [invoice]

    required_validation = TaxonValidation(
        name="DateRequired",
        description="Date is required",
        rule_formula="!isBlank({date})"
    )
    format_validation = TaxonValidation(
        name="ValidDateFormat",
        description="Date must be valid format",
        rule_formula="isBlank({date}) || isdate({date})"
    )
    range_validation = TaxonValidation(
        name="DateRange",
        description="Date must be within valid range",
        rule_formula=(
            "isBlank({date}) || (isafterdate({date}, "
            "datemath(\"today - 30 days\")) && "
            "isbeforedate({date}, datemath(\"today + 30 days\")))"
        )
    )
    due_date_validation = TaxonValidation(
        name="DueDateAfterInvoice",
        description="Due date must be after invoice date",
        rule_formula=(
            "isBlank({duedate}) || isBlank({date}) || "
            "isBeforeDate({duedate}, datemath({date}, \"days\", 101))"
        )
    )
    birth_date_validation = TaxonValidation(
        name="BirthDatePast",
        description="Birth date must be in the past",
        rule_formula=(
            "isBlank({birthdate}) || (isdate({birthdate}) && "
            "isbeforedate({birthdate}, \"today\"))"
        )
    )
    leap_year_validation = TaxonValidation(
        name="LeapYearValidation",
        description="Leap year date validation",
        rule_formula="isBlank({date}) || isdate({date})"
    )

    document_validations = [
        DocumentTaxonValidation(
            taxonomy_ref="test/date-taxonomy:1.0.0",
            taxon_path="invoice/date",
            validation=required_validation
        ),
        DocumentTaxonValidation(
            taxonomy_ref="test/date-taxonomy:1.0.0",
            taxon_path="invoice/date",
            validation=format_validation
        ),
        DocumentTaxonValidation(
            taxonomy_ref="test/date-taxonomy:1.0.0",
            taxon_path="invoice/date",
            validation=range_validation
        ),
        DocumentTaxonValidation(
            taxonomy_ref="test/date-taxonomy:1.0.0",
            taxon_path="invoice/duedate",
            validation=due_date_validation
        ),
        DocumentTaxonValidation(
            taxonomy_ref="test/date-taxonomy:1.0.0",
            taxon_path="invoice/birthdate",
            validation=birth_date_validation
        ),
        DocumentTaxonValidation(
            taxonomy_ref="test/date-taxonomy:1.0.0",
            taxon_path="invoice/date",
            validation=leap_year_validation
        )
    ]

    document.set_validations(document_validations)
    validations = document.get_validations()

    assert len(validations) == 6

    date_validations = [
        v for v in validations if v.taxon_path == "invoice/date"
    ]
    assert len(date_validations) == 4

    due_date_validations = [
        v for v in validations if v.taxon_path == "invoice/duedate"
    ]
    assert len(due_date_validations) == 1

    birth_date_validations = [
        v for v in validations if v.taxon_path == "invoice/birthdate"
    ]
    assert len(birth_date_validations) == 1

    validation_names = [v.validation.name for v in validations]
    expected_names = [
        "DateRequired", "ValidDateFormat", "DateRange",
        "DueDateAfterInvoice", "BirthDatePast", "LeapYearValidation"
    ]
    assert all(name in validation_names for name in expected_names)

    assert any("isBlank" in v.validation.rule_formula for v in validations)
    assert any("isdate" in v.validation.rule_formula for v in validations)
    assert any("isafterdate" in v.validation.rule_formula for v in validations)
    assert any(
        "isbeforedate" in v.validation.rule_formula for v in validations
    )
    assert any("datemath" in v.validation.rule_formula for v in validations)
