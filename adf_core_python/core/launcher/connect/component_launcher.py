import socket
import time

from structlog import BoundLogger

from adf_core_python.core.agent.agent import Agent
from adf_core_python.core.launcher.connect.connection import Connection
from adf_core_python.core.launcher.connect.error.agent_error import AgentError
from adf_core_python.core.launcher.connect.error.server_error import ServerError


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
        except AgentError as e:
            self.logger.exception(
                f"Agent error: {e}",
                exception=str(e),
            )
        except ServerError as e:
            if isinstance(e.__cause__, EOFError):
                self.logger.info(
                    f"Connection closed by server (request_id={_request_id})"
                )
            else:
                self.logger.exception("Server error", exception=str(e))

    def generate_request_id(self) -> int:
        self.request_id += 1
        return self.request_id

    def check_kernel_connection(
        self, timeout: int = 30, retry_interval: float = 5.0
    ) -> bool:
        """Attempts to connect to the kernel multiple times within the specified timeout period.

        Args:
            timeout (int): Total timeout duration in seconds
            retry_interval (float): Interval between retry attempts in seconds

        Returns:
            bool: True if connection successful, False otherwise
        """
        start_time = time.time()
        attempt = 1

        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(retry_interval)
                result = sock.connect_ex((self.host, self.port))
                sock.close()

                if result == 0:
                    self.logger.info(
                        f"Successfully connected to kernel (attempt: {attempt})"
                    )
                    return True

                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout:
                    self.logger.error(
                        f"Timeout: Could not connect to kernel within {timeout} seconds (attempts: {attempt})"
                    )
                    return False

                self.logger.debug(
                    f"Connection attempt {attempt} failed - retrying in {retry_interval} seconds"
                )
                time.sleep(retry_interval)
                attempt += 1

            except Exception as e:
                self.logger.error(f"Error while checking kernel connection: {e}")
                return False
