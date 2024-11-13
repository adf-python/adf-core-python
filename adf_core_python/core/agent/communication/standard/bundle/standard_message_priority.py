from enum import Enum


class StandardMessagePriority(Enum):
    """
    Standard message priorities.
    """

    LOW = 0
    NORMAL = 1
    HIGH = 2

    def __str__(self) -> str:
        return self.name.lower()

    def __lt__(self, other: object) -> bool:
        if isinstance(other, StandardMessagePriority):
            return self.value < other.value
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, StandardMessagePriority):
            return self.value <= other.value
        return NotImplemented
