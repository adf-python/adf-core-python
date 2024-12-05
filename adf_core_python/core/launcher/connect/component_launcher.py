import socket

from structlog import BoundLogger

from adf_core_python.core.agent.agent import Agent
from adf_core_python.core.launcher.connect.connection import Connection


class ComponentLauncher:
    def __init__(self, host: str, port: int, logger: BoundLogger) -> None:
        self.request_id = 0
        self.port = port
        self.host = host
        self.logger = logger

    def make_connection(self) -> Connection:
        return Connection(self.host, self.port)

    def connect(self, agent: Agent, _request_id: int) -> None:
        connection = self.make_connection()
        try:
            connection.connect()
        except socket.timeout:
            self.logger.warning(f"Connection to {self.host}:{self.port} timed out")
            return
        except socket.error as e:
            self.logger.exception(
                f"Failed to connect to {self.host}:{self.port}", exception=str(e)
            )
            return

        connection.message_received(agent.message_received)
        agent.set_send_msg(connection.send_msg)
        agent.start_up(_request_id)

        try:
            connection.parse_message_from_kernel()
        except Exception as e:
            self.logger.exception(
                f"Agent threw an exception {e}",
                exception=str(e),
            )

    def generate_request_id(self) -> int:
        self.request_id += 1
        return self.request_id
