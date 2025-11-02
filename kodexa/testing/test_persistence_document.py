import pytest

from kodexa.model.model import Document, ProcessingStep
from kodexa.model.objects import DocumentKnowledgeFeature


@pytest.mark.parametrize("metadata", [{"step": "one"}, {}])
def test_processing_steps_persist_round_trip(tmp_path, metadata):
    doc_path = tmp_path / "processing_steps.kddb"

    doc = Document(kddb_path=str(doc_path), delete_on_close=False)
    try:
        steps = [
            ProcessingStep(name="step-1"),
            ProcessingStep(name="step-2", metadata=metadata),
        ]

        doc.set_steps(steps)
        doc.close()
        doc = None

        reopened = Document(kddb_path=str(doc_path), delete_on_close=False)
        try:
            loaded_steps = reopened.get_steps()

            assert [step.name for step in loaded_steps] == ["step-1", "step-2"]
            assert loaded_steps[1].metadata == metadata
        finally:
            reopened.close()
    finally:
        if doc is not None and doc.get_persistence():
            doc.close()


def test_document_knowledge_features_persist_round_trip(tmp_path):
    doc_path = tmp_path / "document_features.kddb"

    doc = Document(kddb_path=str(doc_path), delete_on_close=False)
    try:
        features = [
            DocumentKnowledgeFeature(
                knowledge_feature_ref="feature-1", properties={"score": 0.95}
            ),
            DocumentKnowledgeFeature(properties={"notes": "fallback"}),
        ]

        doc.set_document_knowledge_features(features)
        doc.close()
        doc = None

        reopened = Document(kddb_path=str(doc_path), delete_on_close=False)
        try:
            loaded_features = reopened.get_document_knowledge_features()

            assert [feature.knowledge_feature_ref for feature in loaded_features] == [
                "feature-1",
                None,
            ]
            assert loaded_features[0].properties == {"score": 0.95}
            assert loaded_features[1].properties == {"notes": "fallback"}
        finally:
            reopened.close()
    finally:
        if doc is not None and doc.get_persistence():
            doc.close()

