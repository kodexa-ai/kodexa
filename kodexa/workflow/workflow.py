from typing import List, Dict, Any


class WorkflowStore:

    def __init__(self, name: str, ref: str):
        self.name: str = name
        self.ref: str = ref


class WorkflowConnector:

    def __init__(self, name: str, ref: str, options=None):
        if options is None:
            options = {}
        self.name: str = name
        self.ref: str = ref
        self.options: Dict[str, Any] = options


class WorkflowPipeline:

    def __init__(self, name: str, ref: str, subscription: str, target: str = None, parameters=None):
        if parameters is None:
            parameters = {}
        self.name: str = name
        self.ref: str = ref

        self.subscription: str = subscription
        self.parameters: Dict[str, Any] = parameters


class Workflow:

    def __init__(self, access_token:str):
        self.stores: List[WorkflowStore] = []
        self.pipelines: List[WorkflowPipeline] = []
        self.connectors: List[WorkflowConnector] = []
        self.access_token = access_token

    def add_store(self, name: str, ref: str):
        self.stores.append(WorkflowStore(name, ref))

    def add_pipeline(self, name: str, ref: str, subscription: str = "*", target: str = None, parameters=None):
        self.pipelines.append(WorkflowPipeline(name, ref, subscription, target, parameters))
