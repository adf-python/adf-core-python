from __future__ import annotations

from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from bitarray import bitarray


class CommunicationMessage(ABC):
  def __init__(self, is_wireless_message: bool) -> None:
    self._is_wireless_message = is_wireless_message

  def is_wireless_message(self) -> bool:
    return self._is_wireless_message

  @abstractmethod
  def get_bit_size(self) -> int:
    raise NotImplementedError

  @abstractmethod
  def to_bits(self) -> bitarray:
    raise NotImplementedError

  @abstractmethod
  def __hash__(self) -> int:
    raise NotImplementedError
