from kodexa.model.objects import ExecutionEvent


def test_session():
    event = ExecutionEvent(**{"id": "123", "type": "STEP_UPDATE", "sessionId": "cheese", "token": "toke12"})
    print(event.dict(by_alias=True))
