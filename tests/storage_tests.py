def test_load_engine():
    """
    Test the engine loading
    """
    from kodexa.model.db.engine import DocumentDBEngine
    engine = DocumentDBEngine()
    engine.load_structure()
