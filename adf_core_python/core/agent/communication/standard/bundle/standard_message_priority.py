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
