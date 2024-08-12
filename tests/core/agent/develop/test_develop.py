import os

import pytest

from adf_core_python.core.agent.develop.develop_data import DevelopData


class TestDevelopData:
    def test_can_read_from_yaml(self) -> None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        develop_file_path = os.path.join(script_dir, "develop.json")
        develop_data = DevelopData(True, develop_file_path)
        print(develop_data._develop_data)

        assert develop_data.get_value("string") == "test"
        assert develop_data.get_value("number") == 1
        assert develop_data.get_value("boolean") is True
        assert develop_data.get_value("dict") == {"test": "test"}
        assert develop_data.get_value("array") == ["test", "test"]

    def test_if_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError):
            DevelopData(True, "not_found.json")
