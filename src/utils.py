from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Collection


class Action(ABC):
    pass


class BaseGame(ABC):

    @abstractmethod
    def perform_action(self, **kwargs):
        pass

    @abstractmethod
    def to_move(self, **kwargs) -> bool:
        pass

    @abstractmethod
    def utility(self, **kwargs) -> float:
        pass

    @abstractmethod
    def actions(self, **kwargs) -> Collection[Action]:
        pass

    @abstractmethod
    def is_terminal(self) -> bool:
        pass

    @abstractmethod
    def copy(self):
        pass