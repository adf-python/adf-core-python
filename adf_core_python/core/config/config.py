from typing import Any, Optional

from yaml import safe_load


class Config:
    def __init__(self, config_file: Optional[str] = None) -> None:
        self.config: dict[str, Any] = {}
        if config_file:
            self.config = self.read_from_yaml(config_file)
            self.config = self.flatten(self.config)

    def set_value(self, key: str, value: Any):
        self.config[key] = value

    def get_value(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def read_from_yaml(self, file_name: str) -> dict[str, Any]:
        try:
            with open(file_name, mode="r", encoding="utf-8") as file:
                data = safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {file_name}")
        except Exception as e:
            raise Exception(f"Error reading config file: {file_name}, {e}")

        return data

    def flatten(
        self, data: dict[str, Any], parent_key: str = "", sep: str = "."
    ) -> dict[str, Any]:
        flatten_data = {}
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                flatten_data.update(self.flatten(value, new_key, sep=sep))
            else:
                flatten_data[new_key] = value
        return flatten_data

    def __str__(self) -> str:
        return str(self.config)
