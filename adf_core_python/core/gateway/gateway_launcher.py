import socket

from structlog import BoundLogger

from adf_core_python.core.gateway.gateway_agent import GatewayAgent
from adf_core_python.core.launcher.connect.connection import Connection


class GatewayLauncher:
    def __init__(self, host: str, port: int, logger: BoundLogger) -> None:
        self.host = host
        self.port = port
        self.logger = logger
        pass

    def make_connection(self) -> Connection:
        return Connection(self.host, self.port)

    def connect(self, gateway_agent: GatewayAgent) -> None:
        self.logger.info(
            f"{gateway_agent.__class__.__name__} connecting to {self.host}:{self.port}"
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
        except socket.error as e:
            self.logger.error(f"Failed to connect to {self.host}:{self.port}")
            self.logger.error(e)
            return

        connection.message_received(gateway_agent.message_received)
        gateway_agent.set_send_msg(connection.send_msg)

        try:
            connection.parse_message_from_kernel()
        except Exception as e:
            self.logger.error(f"Failed to connect agent: {self.host}:{self.port} {e}")
