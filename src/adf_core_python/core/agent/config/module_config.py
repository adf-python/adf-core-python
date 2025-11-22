from typing import Any, Final

from rcrscore.config import Config
from yaml import safe_load


class ModuleConfig(Config):
  DEFAULT_CONFIG_FILE_NAME: Final[str] = "config/module.yaml"

  def __init__(self, config_file_name: str = DEFAULT_CONFIG_FILE_NAME):
    """
    Constructor

    Parameters
    ----------
    config_file_name : str, optional
        Configuration file name, by default DEFAULT_CONFIG_FILE_NAME

    Raises
    ------
    FileNotFoundError
        If config file not found
    Exception
        If error reading config file

    Examples
    --------
    >>> config = ModuleConfig("config/module.yaml")
    >>> config.get_value("DefaultTacticsPoliceOffice.TargetAllocator")
    "sample_team.module.complex.SamplePoliceTargetAllocator"
    """
    super().__init__()
    data = self._read_from_yaml(config_file_name)
    flatten_data = self._flatten(data)
    for key, value in flatten_data.items():
      self.set_value(key, value)

  def _read_from_yaml(self, file_name: str) -> dict[str, Any]:
    """
    Read configuration from yaml file

    Parameters
    ----------
    file_name : str
        Configuration file name

    Returns
    -------
    dict[str, Any]
        Configuration data
    """
    try:
      with open(file_name, mode="r", encoding="utf-8") as file:
        data = safe_load(file)
    except FileNotFoundError:
      raise FileNotFoundError(f"Config file not found: {file_name}")
    except Exception as e:
      raise Exception(f"Error reading config file: {file_name}, {e}")

    return data

  def _flatten(
    self, data: dict[str, Any], parent_key: str = "", sep: str = "."
  ) -> dict[str, Any]:
    """
    Flatten nested dictionary to a single level dictionary

    Parameters
    ----------
    data : dict[str, Any]
        Nested dictionary
    parent_key : str, optional
        Parent key, by default ""
    sep : str, optional
        Separator, by default "."

    Returns
    -------
    dict[str, Any]
        Flattened dictionary
    """
    flatten_data: dict[str, Any] = {}
    for key, value in data.items():
      new_key = f"{parent_key}{sep}{key}" if parent_key else key
      if isinstance(value, dict):
        v: dict[str, Any] = value
        flatten_data.update(self._flatten(v, new_key, sep=sep))
      else:
        flatten_data[new_key] = value
    return flatten_data
