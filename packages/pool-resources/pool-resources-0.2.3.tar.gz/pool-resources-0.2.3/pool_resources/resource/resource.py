"""Resource module"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar

T1 = TypeVar("T1")
T2 = TypeVar("T2")

class Resource(ABC):
    """Resource abstract class"""
    @abstractmethod
    def enable(self, item: T1 | T2) -> T1 | T2:
        """Enables the resource"""

    def disable(self, item: T1 | T2) -> T1 | T2:
        """Disables the resource"""
