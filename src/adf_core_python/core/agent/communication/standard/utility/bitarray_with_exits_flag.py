from typing import Optional

from bitarray import bitarray

IS_EXIST_FLAG = 1
IS_NOT_EXIST_FLAG = 0


def write_with_exist_flag(
  bit_array: bitarray, value: Optional[int], bit_size: int
) -> None:
  """
  Write value to bit_array with an exist flag.
  If value is None, write IS_NOT_EXIST_FLAG to bit_array.
  If value is not None, write IS_EXIST_FLAG to bit_array and then write value to bit_array.

  PARAMETERS
  ----------
  bit_array: bitarray
      The bitarray to write to.
  value: Optional[int]
      The value to write.
  bit_size: int
      The number of bits to use to write value.

  RAISES
  ------
  ValueError
      If value is too large to fit into bit_size bits.
  """
  if value is None:
    bit_array.extend([IS_NOT_EXIST_FLAG])
  else:
    bit_array.extend([IS_EXIST_FLAG])
    bit_value = bitarray(f"{value:0{bit_size}b}")
    if len(bit_value) > bit_size:
      raise ValueError(f"Value {value} is too large to fit into {bit_size} bits")
    bit_array.extend(bit_value)


def read_with_exist_flag(bit_array: bitarray, size: int) -> Optional[int]:
  """
  Read value from bit_array with an exist flag.
  If the first bit is IS_NOT_EXIST_FLAG, return None.
  If the first bit is IS_EXIST_FLAG, read and return value from bit_array.

  PARAMETERS
  ----------
  bit_array: bitarray
      The bitarray to read from.
  size: int
      The number of bits to read to get value.

  RETURNS
  -------
  Optional[int]
      The value read from bit_array.

  RAISES
  ------
  ValueError
      If the first bit is not IS_EXIST_FLAG or IS_NOT_EXIST_FLAG.
  """
  exist_flag = bit_array.pop(0)
  if exist_flag == IS_NOT_EXIST_FLAG:
    return None
  elif exist_flag == IS_EXIST_FLAG:
    value = int(bit_array[:size].to01(), 2)
    del bit_array[:size]
    return value
  else:
    raise ValueError("Invalid exist flag")
