import socket

from rcrs_core.agents.agent import Agent
from structlog import BoundLogger

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
        self.logger.bind(agent_id=agent.get_id())

        self.logger.info(
            f"{agent.__class__.__name__} connecting to {self.host}:{self.port} request_id: {_request_id}"
        )
        connection = self.make_connection()
        try:
            connection.connect()
            # ソケットが使用しているPORT番号を取得
            if connection.socket is not None:
                self.logger.info(
                    f"Connected to {self.host}:{self.port} on port {connection.socket.getsockname()[1]}"
                )
        except socket.timeout:
            self.logger.warning(f"Connection to {self.host}:{self.port} timed out")
            return
        except socket.error:
            self.logger.error(f"Failed to connect to {self.host}:{self.port}")
            return

        connection.message_received(agent.message_received)
        agent.set_send_msg(connection.send_msg)
        agent.start_up(_request_id)

        try:
            connection.parse_message_from_kernel()
        except Exception as e:
            self.logger.error(f"Failed to connect agent: {self.host}:{self.port} {e}")

    def generate_request_id(self) -> int:
        self.request_id += 1
        return self.request_id
