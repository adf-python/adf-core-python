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

    def __lt__(self, other):
        if isinstance(other, StandardMessagePriority):
            return self.value < other.value

    def __le__(self, other):
        if isinstance(other, StandardMessagePriority):
            return self.value <= other.value
