import socket
from typing import Any, Callable

import rcrs_core.connection.rcrs_encoding_utils as rcrs_encoding_utils

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
                msg = rcrs_encoding_utils.read_msg(self.socket)
            except Exception as e:
                raise ServerError(f"Error reading from socket: {e}") from e
            try:
                self.agent_message_received(msg)
            except Exception as e:
                raise AgentError(f"Error agent calculation: {e}") from e

    def message_received(self, agent_message_received: Callable) -> None:
        self.agent_message_received = agent_message_received

    def send_msg(self, msg: Any) -> None:
        rcrs_encoding_utils.write_msg(msg, self.socket)
