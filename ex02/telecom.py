from abc import ABC, abstractmethod
from enum import (Enum)
from typing import Dict


class Command(Enum):
    """
    Enumeration for telecom commands.
    """
    READY_FOR_LOADING = 'ready_for_loading'
    MOVING = 'moving'
    LOADING = 'loading'
    LOADED_OK = 'loaded_ok'
    LOADED_INVALID = 'loaded_invalid'
    MOVE = 'move'
    MOVED = 'moved'


class Telecom(object):

    def __init__(self, command: Command, payload=None, errors=None):
        assert isinstance(command, Command)
        self.command = command
        self.payload = payload
        self.errors= errors


class Exchanger(ABC):

    @abstractmethod
    def exchange(self, tm: Telecom) -> Telecom:
        pass
