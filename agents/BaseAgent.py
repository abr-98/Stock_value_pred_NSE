from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Base class for all agents.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, **kwargs):
        """
        Execute agent logic.
        Must return a structured signal.
        """
        raise NotImplementedError
