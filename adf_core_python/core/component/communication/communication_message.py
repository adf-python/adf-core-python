from abc import ABC, abstractmethod


class CommunicationMessage(ABC):
    def __init__(self, is_wireless_message: bool) -> None:
        self._is_wireless_message = is_wireless_message

    def is_wireless_message(self) -> bool:
        return self._is_wireless_message

    @abstractmethod
    def get_byte_size(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def to_bytes(self) -> bytes:
        raise NotImplementedError

    # TODO: Implement the toBitOutputStream and getCheckKey methods
