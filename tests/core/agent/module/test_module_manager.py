import os

from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.component.module.abstract_module import AbstractModule


class TestModuleManager:
    def test_can_get_module(self) -> None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, "module.yaml")
        config = ModuleConfig(config_file_path)
        config.set_value(
            "test_module",
            "adf_core_python.implement.module.algorithm.a_star_path_planning.AStarPathPlanning",
        )
        module_manager = self.create_module_manager(config)
        module = module_manager.get_module("test_module", "test_module")
        assert isinstance(module, AbstractModule)
        assert module.__class__.__name__ == "AStarPathPlanning"

    def create_module_manager(self, config: ModuleConfig) -> ModuleManager:
        return ModuleManager(
            None,  # type: ignore
            None,  # type: ignore
            None,  # type: ignore
            config,
            None,  # type: ignore
        )
