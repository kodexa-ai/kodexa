from kodexa import Pipeline, LocalDocumentStore, LocalModelStore


def test_interesting_pipeline():
    training_documents = LocalDocumentStore('/tmp/test-store', force_initialize=True)

    # If we have a store, can we determine that we only want to process
    # documents that we haven't already got in the store

    def test_step(document):
        return document

    def test_model_store(document, context):
        context.get_store('my-model-store').put('cheese.txt', 'so cheesy'.encode('ascii'))
        return document

    training_prep = Pipeline.from_text("hello world", apply_lineage=False).to_store(training_documents)
    training_prep.add_step(test_step)
    training_prep.add_label('training_document')

    training_prep.run()

    assert training_documents.count() == 1

    model_store = LocalModelStore('/tmp/my-model')
    training_pipeline = Pipeline.from_store(training_documents)
    training_pipeline.add_store('my-model-store', model_store)
    training_pipeline.add_step(test_model_store)

    training_pipeline.run()

    assert model_store.get('cheese.txt').read().decode('ascii') == 'so cheesy'
