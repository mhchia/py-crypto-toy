from abc import ABC, abstractmethod


class GroupElement(ABC):
    @property
    def identity(self) -> "GroupElement":
        ...

    @abstractmethod
    def operate(self, other: "GroupElement") -> "GroupElement":
        ...

    @abstractmethod
    def inverse(self) -> "GroupElement":
        ...
