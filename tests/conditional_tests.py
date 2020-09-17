from kodexa import Pipeline


def test_basic_conditional():
    def add_to_context(document, context):
        context.context['test_value'] = True
        return document

    def test_match(document, context):
        document.metadata['matched'] = True
        return document

    def test_miss(document, context):
        document.metadata['matched'] = False
        return document

    pipeline = Pipeline.from_text("Text Message")
    pipeline.add_step(add_to_context)
    pipeline.add_step(test_match, condition="context.test_value == True")
    context = pipeline.run()
    assert context.output_document.metadata.matched is True

    pipeline = Pipeline.from_text("Text Message")
    pipeline.add_step(add_to_context)
    pipeline.add_step(test_miss, condition="context.test_value == True")
    context = pipeline.run()
    print(context.output_document.metadata)
    assert context.output_document.metadata.matched is False


def test_enabled():
    def test_match(document, context):
        document.metadata['matched'] = True
        return document

    pipeline = Pipeline.from_text("Text Message")
    pipeline.add_step(test_match, enabled=True)
    context = pipeline.run()
    assert context.output_document.metadata.matched is True

    pipeline = Pipeline.from_text("Text Message")
    pipeline.add_step(test_match, enabled=False)
    context = pipeline.run()
    print(context.output_document.metadata)
    assert 'matched' not in context.output_document.metadata
