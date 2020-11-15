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

    def __init__(self, name: str, ref: str, subscription: str, parameters=None):
        if parameters is None:
            parameters = {}
        self.name: str = name
        self.ref: str = ref

        self.subscription: str = subscription
        self.parameters: Dict[str, Any] = parameters


class Workflow:

    def __init__(self):
        self.stores: List[WorkflowStore] = []
        self.pipelines: List[WorkflowPipeline] = []
        self.connectors: List[WorkflowConnector] = []
