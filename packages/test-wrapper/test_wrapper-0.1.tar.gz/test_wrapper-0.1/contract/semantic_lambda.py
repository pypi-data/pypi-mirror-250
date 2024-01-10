import abc

"""
The application interface is the contract that all applications must implement to be served in the runloop.
TODO - pass some config to the application layer
"""

class SemanticLambdaInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "handle_input") and callable(subclass.handle_input))

    @abc.abstractmethod
    def handle_input(self, metadata: dict[str, str], input: list[str]) -> tuple[list[str], dict[str, str]]:
        """Handle the provided input in the context of app metadata and return a response."""
        raise NotImplementedError
