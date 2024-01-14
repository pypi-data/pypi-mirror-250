# Define Base Class for Models
from abc import ABC, abstractmethod


# Define Base Class for State Object for all Models
class ModelStateBase(ABC):
    """Class to maintain the state during a model execution."""

    def __init__(self, timetable, dataset):
        self.stats = {}

    def set_stat(self, key: str, val):
        self.stats[key] = val


class Model(ABC):
    """Base class for all models."""

    @abstractmethod
    def state_class(self):
        """The class that maintains state for this model."""
        ...

    @abstractmethod
    def price_method(self):
        """The method that calculates price."""
        ...

    def price(self, timetable, dataset):
        """Calculate price of contract.

        Parameters:
            timetable (dict): timetable for the contract.
            dataset (dict): dataset for the model.

        Returns:
            price (float): price of contract
            stats (dict): stats such as standard error

        """

        model_state = (self.state_class())(timetable, dataset)
        price = self.price_method()(
            timetable["events"], model_state, dataset, timetable["expressions"]
        )

        return price, model_state.stats
