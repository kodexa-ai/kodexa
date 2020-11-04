from kodexa import Pipeline, LocalDocumentStore


def test_interesting_pipeline():
    training_documents = LocalDocumentStore('/tmp/test-store', force_initialize=True)

    # If we have a store, can we determine that we only want to process
    # documents that we haven't already got in the store

    def test_step(document):
        return document

    training_prep = Pipeline.from_text("hello world").to_store(training_documents)
    training_prep.add_step(test_step)
    training_prep.add_label('training_document')

    context = training_prep.run()

    assert training_documents.count() == 1
    assert training_documents.get_by_uuid(training_documents.list()[0]['uuid']) is not None
