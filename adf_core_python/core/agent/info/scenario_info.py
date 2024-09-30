from enum import Enum
from typing import Any

from adf_core_python.core.config.config import Config


class Mode(Enum):
    NON_PRECOMPUTE = 0
    PRECOMPUTED = 1
    PRECOMPUTATION = 2


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

    def get_value(self, key: str, default: Any) -> Any:
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
        return self._config.get_value(key, default)
