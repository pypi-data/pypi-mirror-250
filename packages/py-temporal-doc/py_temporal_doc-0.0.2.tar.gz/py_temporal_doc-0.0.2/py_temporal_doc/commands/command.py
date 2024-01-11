from abc import ABC, abstractmethod

from click import MultiCommand


class Command(ABC):
    """
    Command Abstract class
    All commands CLI should use this as a base class
    """

    __command_list: list[MultiCommand] = None

    @abstractmethod
    def execute(self) -> None:
        """
        Abstract method for command entry point
        """
        pass
