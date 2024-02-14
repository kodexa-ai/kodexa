from kodexa.model.objects import ModelInteraction


class ModelInteractionManager:
    _instance = None

    def __new__(cls):
        """
        Create and return the singleton instance of ModelInteractionManager.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.model_interactions = []
        return cls._instance

    def clear_model_interactions(self):
        """
        Clear the list of model interactions.
        """
        self.model_interactions.clear()

    def add_model_interaction(self, interaction: ModelInteraction):
        """
        Add a model interaction to the list.

        Args:
            interaction (ModelInteraction): The model interaction to add.
        """
        self.model_interactions.append(interaction)

    def get_model_interactions(self):
        """
        Get the list of model interactions.

        Returns:
            list[ModelInteraction]: The list of model interactions.
        """
        return self.model_interactions.copy()
