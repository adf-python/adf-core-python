import sys
from typing import Any, NoReturn

from rcrs_core.agents.agent import Agent as RCRSAgent
from rcrs_core.worldmodel.worldmodel import WorldModel

from adf_core_python.core.logger.logger import get_logger


class Agent(RCRSAgent):
    def __init__(self, is_precompute: bool, name: str) -> None:
        self.name = name
        self.connect_request_id = None
        self.world_model = WorldModel()
        self.config = None
        self.random = None
        self.agent_id = None
        self.precompute_flag = is_precompute
        self.logger = get_logger(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        )

    def handle_connect_error(self, msg: Any) -> NoReturn:
        self.logger.error(
            "Failed to connect agent: %s(request_id: %s)", msg.reason, msg.request_id
        )
        sys.exit(1)
