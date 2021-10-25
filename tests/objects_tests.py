import json
from datetime import datetime

from kodexa import *
from kodexa.model.objects import ExecutionEvent, ContentObject


def test_session():
    event = ExecutionEvent(**{"id": "123", "type": "STEP_UPDATE", "sessionId": "cheese", "token": "toke12"})
    print(event.dict(by_alias=True))


def test_event_2():
    with open('test_documents/event-2.json', 'r') as event1:
        raw = json.load(event1)
        event = ExecutionEvent(**raw)

    print(event)


def test_platform_store():
    # Configure Access Token and URL
    KodexaPlatform.set_access_token('0ae2686fbb994398a1ebeffc8d5cf3ba')
    KodexaPlatform.set_url('https://elnido.kodexa.ai')

    # store = KodexaPlatform.get_object_instance('philip-world/8a8a82137cb30893017cb31cd222001d-processing:1.0.0','store')

    data_store = KodexaPlatform.get_object_instance(
        'philip-world/8a8a82137cb30893017cb31cd222001d-extracted-data:1.0.0', 'store')
    print(data_store)


def test_content_datetime():
    co = ContentObject(**{'contentType': 'DOCUMENT'})
    co.created_on = datetime.now()

    print(co.json())
