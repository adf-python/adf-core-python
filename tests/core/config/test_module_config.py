import os

import pytest

from adf_core_python.core.config.module_config import ModuleConfig


class TestModuleConfig:
    def test_can_read_from_yaml(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, "module.yaml")
        config = ModuleConfig(config_file_path)
        assert (
            config.get_value("DefaultTacticsPoliceOffice.TargetAllocator")
            == "sample_team.module.complex.SamplePoliceTargetAllocator"
        )
        assert (
            config.get_value("DefaultTacticsPoliceOffice.CommandPicker")
            == "adf.impl.centralized.DefaultCommandPickerPolice"
        )
        assert (
            config.get_value("SampleSearch.PathPlanning.Ambulance")
            == "adf.impl.module.algorithm.DijkstraPathPlanning"
        )
        assert (
            config.get_value("SampleSearch.PathPlanning.Fire")
            == "adf.impl.module.algorithm.DijkstraPathPlanning"
        )
        assert (
            config.get_value("SampleSearch.PathPlanning.Police")
            == "adf.impl.module.algorithm.DijkstraPathPlanning"
        )
        assert (
            config.get_value("SampleSearch.Clustering.Ambulance")
            == "adf.impl.module.algorithm.KMeansClustering"
        )
        assert (
            config.get_value("SampleSearch.Clustering.Fire")
            == "adf.impl.module.algorithm.KMeansClustering"
        )
        assert (
            config.get_value("SampleSearch.Clustering.Police")
            == "adf.impl.module.algorithm.KMeansClustering"
        )

    def test_if_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            ModuleConfig("not_found.yaml")
