from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from adf_core_python.core.agent.info import AgentInfo, ScenarioInfo, WorldInfo


class ChannelSubscriber(ABC):
  @abstractmethod
  def subscribe(
    self,
    agent_info: AgentInfo,
    world_info: WorldInfo,
    scenario_info: ScenarioInfo,
  ) -> list[int]:
    """
    Subscribe to the channel.

    Parameters
    ----------
    agent_info : AgentInfo
        The agent info.
    world_info : WorldInfo
        The world info.
    scenario_info : ScenarioInfo
        The scenario info.

    Returns
    -------
    list[int]
        The list of subscribed channels.
    """
    pass
