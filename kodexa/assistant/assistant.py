class Assistant:

    def __init__(self, full_description=None):
        self.required_stores = []
        self.workflows = []
        self.processing_taxonomies = []
        self.services = []

        self.full_description = full_description

    def add_store(self, name: str, title: str, description: str, store_type: str):
        self.required_stores.append({
            'name': name,
            'title': title,
            'description': description,
            'storeType': store_type
        })

    def add_workflow(self, ref: str, parameters=None):
        self.workflows.append({
            'ref': ref,
            'parameters': parameters
        })

    def add_processing_taxonomy(self, ref: str):
        self.processing_taxonomies.append({
            'ref': ref
        })

    def add_service(self, slug, service):
        service.slug = slug
        self.services.append(service)
