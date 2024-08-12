import json
from typing import Any, Dict, Final


class DevelopData:
    DEFAULT_FILE_NAME: Final[str] = "config/develop.json"

    def __init__(
        self, is_develop_mode: bool = False, file_name: str = DEFAULT_FILE_NAME
    ) -> None:
        """
        Constructor
        """
        self._develop_data: Dict[str, Any] = self._set_data_from_json(file_name)
        self._is_develop_mode: bool = is_develop_mode

        self._set_data_from_json(file_name)

    def _set_data_from_json(self, file_name: str) -> Dict[str, Any]:
        """
        Set data from json

        Parameters
        ----------
        file_name : str, optional
            Develop file name, by default DEFAULT_FILE_NAME

        Returns
        -------
        Dict[str, Any]
            Develop data
        """
        try:
            with open(file_name, mode="r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Develop file not found: {file_name}")
        except Exception as e:
            raise Exception(f"Error reading develop file: {file_name}, {e}")

    def is_develop_mode(self) -> bool:
        """
        Check if develop mode is enabled

        Returns
        -------
        bool
            True if develop mode is enabled
        """
        return self._is_develop_mode

    def get_value(self, key: str, default_value: Any = None) -> Any:
        """
        Get value from develop data
        If develop mode is disabled, return default value

        Parameters
        ----------
        key : str
            Key

        Returns
        -------
        Any
            Value
        """
        if not self._is_develop_mode:
            return default_value

        return self._develop_data.get(key, default_value)
