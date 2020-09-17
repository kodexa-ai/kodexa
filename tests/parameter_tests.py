from kodexa import Pipeline


def test_parameterized_pipeline():
    class ExampleStep:

        def __init__(self, my_value):
            self.my_value = my_value

        def get_name(self):
            return "Example Step"

        def process(self, document):
            document.metadata['example'] = self.my_value
            return document

    pipeline = Pipeline.from_text("Hello World")
    pipeline.add_step(ExampleStep, options={'my_value': '${example}'}, parameterized=True)
    context = pipeline.run(parameters={'example': 'testing'})

    assert context.output_document.metadata.example == "testing"
