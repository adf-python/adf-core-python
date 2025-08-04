import socket
from typing import Any, Callable

from rcrscore.proto import RCRSProto_pb2

from adf_core_python.core.launcher.connect.error.agent_error import AgentError
from adf_core_python.core.launcher.connect.error.server_error import ServerError


class Connection:
  def __init__(self, host: str, port: int) -> None:
    self.socket: socket.socket
    self.agent = None
    self.buffer_size: int = 4096
    self.data_buffer: bytes = b""
    self.host = host
    self.port = port

  def connect(self) -> None:
    """
    Connect to the kernel

    Raises
    ------
    socket.timeout
        If the connection times out
    socket.error
        If there is an error connecting to the socket

    """
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((self.host, self.port))

  def parse_message_from_kernel(self) -> None:
    """
    Parse messages from the kernel

    Raises
    ------
    ServerError
        If there is an error reading from the socket
    AgentError
        If there is an error in the agent calculation
    """
    while True:
      try:
        msg = Connection._read_msg(self.socket)
      except Exception as e:
        raise ServerError(f"Error reading from socket: {e}") from e
      try:
        self.agent_message_received(msg)
      except Exception as e:
        raise AgentError(f"Error agent calculation: {e}") from e

  def message_received(self, agent_message_received: Callable) -> None:
    self.agent_message_received = agent_message_received

  def send_msg(self, msg: Any) -> None:
    Connection._write_msg(msg, self.socket)

  @staticmethod
  def _write_int32(value, sock):
    b = [
      ((value >> 24) & 0xFF),
      ((value >> 16) & 0xFF),
      ((value >> 8) & 0xFF),
      (value & 0xFF),
    ]

    sock.sendall(bytes(b))

  @staticmethod
  def _readnbytes(sock, n):
    buff = b""
    while n > 0:
      b = sock.recv(n)
      buff += b
      if len(b) == 0:
        raise EOFError  # peer socket has received a SH_WR shutdown
      n -= len(b)
    return buff

  @staticmethod
  def _read_int32(sock):
    byte_array = Connection._readnbytes(sock, 4)
    value = int(
      ((byte_array[0]) << 24)
      + ((byte_array[1]) << 16)
      + ((byte_array[2]) << 8)
      + (byte_array[3])
    )
    return value

  @staticmethod
  def _write_msg(msg, sock):
    out = msg.SerializeToString()
    Connection._write_int32(len(out), sock)

    sock.sendall(out)

  @staticmethod
  def _read_msg(sock):
    # await reader.read(1)
    size = Connection._read_int32(sock)
    content = Connection._readnbytes(sock, size)
    message = RCRSProto_pb2.MessageProto()
    message.ParseFromString(bytes(content))
    return message
