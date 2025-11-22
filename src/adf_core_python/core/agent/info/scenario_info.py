from enum import IntEnum
from typing import TypeVar

from adf_core_python.core.config import Config

T = TypeVar("T")


class Mode(IntEnum):
  NON_PRECOMPUTE = 0
  PRECOMPUTED = 1
  PRECOMPUTATION = 2


class ScenarioInfoKeys:
  KERNEL_PERCEPTION = "kernel.perception"
  PERCEPTION_LOS_PRECISION_HP = "perception.los.precision.hp"
  CLEAR_REPAIR_RAD = "clear.repair.rad"
  FIRE_TANK_REFILL_HYDRANT_RATE = "fire.tank.refill_hydrant_rate"
  SCENARIO_AGENTS_PF = "scenario.agents.pf"
  SCENARIO_AGENTS_FS = "scenario.agents.fs"
  VOICE_MESSAGES_SIZE = "comms.channels.0.messages.size"
  FIRE_TANK_REFILL_RATE = "fire.tank.refill_rate"
  KERNEL_TIMESTEPS = "kernel.timesteps"
  FIRE_EXTINGUISH_MAX_SUM = "fire.extinguish.max-sum"
  COMMUNICATION_CHANNELS_MAX_PLATOON = "comms.channels.max.platoon"
  KERNEL_AGENTS_THINK_TIME = "kernel.agents.think-time"
  FIRE_TANK_MAXIMUM = "fire.tank.maximum"
  CLEAR_REPAIR_RATE = "clear.repair.rate"
  KERNEL_STARTUP_CONNECT_TIME = "kernel.startup.connect-time"
  KERNEL_HOST = "kernel.host"
  SCENARIO_AGENTS_AT = "scenario.agents.at"
  PERCEPTION_LOS_MAX_DISTANCE = "perception.los.max-distance"
  SCENARIO_AGENTS_FB = "scenario.agents.fb"
  SCENARIO_AGENTS_PO = "scenario.agents.po"
  KERNEL_COMMUNICATION_MODEL = "kernel.communication-model"
  PERCEPTION_LOS_PRECISION_DAMAGE = "perception.los.precision.damage"
  SCENARIO_AGENTS_AC = "scenario.agents.ac"
  COMMUNICATION_CHANNELS_MAX_OFFICE = "comms.channels.max.centre"
  FIRE_EXTINGUISH_MAX_DISTANCE = "fire.extinguish.max-distance"
  KERNEL_AGENTS_IGNOREUNTIL = "kernel.agents.ignoreuntil"
  CLEAR_REPAIR_DISTANCE = "clear.repair.distance"
  COMMUNICATION_CHANNELS_COUNT = "comms.channels.count"


class ScenarioInfo:
  def __init__(self, config: Config, mode: Mode):
    """
    Constructor

    Parameters
    ----------
    config : Config
        Configuration
    mode : Mode
        Mode of the scenario
    """
    self._config: Config = config
    self._mode: Mode = mode

  def set_config(self, config: Config) -> None:
    """
    Set the configuration

    Parameters
    ----------
    config : Config
        Configuration
    """
    self._config = config

  def get_config(self) -> Config:
    """
    Get the configuration

    Returns
    -------
    Config
        Configuration
    """
    return self._config

  def get_mode(self) -> Mode:
    """
    Get the mode of the scenario

    Returns
    -------
    Mode
        Mode of the scenario
    """
    return self._mode

  def get_value(self, key: str, default: T) -> T:
    """
    Get the value of the configuration

    Parameters
    ----------
    key : str
        Key of the configuration
    default : Any
        Default value of the configuration

    Returns
    -------
    Any
        Value of the configuration
    """
    value = self._config.get_value(key, default)
    if not isinstance(value, type(default)):
      try:
        return type(default)(value)  # type: ignore
      except (ValueError, TypeError):
        # 型変換に失敗した場合はそのままデフォルト値を返す
        return default
    return value
