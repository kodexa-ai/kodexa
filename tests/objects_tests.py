import json

from kodexa.model.objects import ExecutionEvent


def test_session():
    event = ExecutionEvent(**{"id": "123", "type": "STEP_UPDATE", "sessionId": "cheese", "token": "toke12"})
    print(event.dict(by_alias=True))


def test_event_2():
    with open('test_documents/event-2.json', 'r') as event1:

        raw = json.load(event1)


        event = ExecutionEvent(**raw)


    print(event)