from typing import List, Dict, Any, Optional


class WorkflowStore:

    def __init__(self, name: str, ref: str):
        self.name: str = name
        self.ref: str = ref


class WorkflowConnector:

    def __init__(self, name: str, ref: str, subscription: str = "true", target: Optional[str] = None, options=None,
                 download=False):
        if options is None:
            options = {}
        self.name: str = name
        self.ref: str = ref
        self.download = download
        self.subscription = subscription
        self.target: Optional[str] = target
        self.options: Dict[str, Any] = options


class WorkflowSchedule:
    pass


class CronSchedule(WorkflowSchedule):

    def __init__(self, name: str, cron: str):
        self.type: str = 'cron'
        self.name: str = name
        self.cron: str = cron

        
class WebSchedule(WorkflowSchedule):

    def __init__(self, name: str):
        self.type: str = 'web'
        self.name: str = name


class StorePublisher:

    def __init__(self, target_store: str, taxonomies: List[str]):
        self.targetStore = target_store
        self.taxonomies = taxonomies


class WorkflowPipeline:

    def __init__(self, name: str, ref: str, subscription: str, target: str = None, parameters=None, publishers=None):
        if parameters is None:
            parameters = {}
        if publishers is None:
            publishers = []
        self.publishers = publishers
        self.name: str = name
        self.ref: str = ref
        self.target: Optional[str] = target

        self.subscription: str = subscription
        self.parameters: Dict[str, Any] = parameters
        self.type = "pipeline"


class Workflow:

    def __init__(self, access_token: str, active=True):
        self.stores: List[WorkflowStore] = []
        self.pipelines: List[WorkflowPipeline] = []
        self.connectors: List[WorkflowConnector] = []
        self.schedules: List[WorkflowSchedule] = []
        self.access_token = access_token
        self.active = active

    def add_store(self, name: str, ref: str):
        self.stores.append(WorkflowStore(name, ref))

    def add_schedule(self, schedule: WorkflowSchedule):
        self.schedules.append(schedule)

    def add_connector(self, name: str, ref: str, subscription: str = "true", target: str = None, options=None,
                      download=False):
        self.connectors.append(WorkflowConnector(name, ref, subscription, target, options, download))

    def add_pipeline(self, name: str, ref: str, subscription: str = "true", target: str = None, parameters=None,
                     publishers=None):
        self.pipelines.append(WorkflowPipeline(name, ref, subscription, target, parameters, publishers))
