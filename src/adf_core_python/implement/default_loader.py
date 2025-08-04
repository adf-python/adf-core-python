from adf_core_python.core.component.abstract_loader import AbstractLoader
from adf_core_python.core.component.tactics.tactics_ambulance_center import (
    TacticsAmbulanceCenter,
)
from adf_core_python.core.component.tactics.tactics_ambulance_team import (
    TacticsAmbulanceTeam,
)
from adf_core_python.core.component.tactics.tactics_fire_brigade import (
    TacticsFireBrigade,
)
from adf_core_python.core.component.tactics.tactics_fire_station import (
    TacticsFireStation,
)
from adf_core_python.core.component.tactics.tactics_police_force import (
    TacticsPoliceForce,
)
from adf_core_python.core.component.tactics.tactics_police_office import (
    TacticsPoliceOffice,
)
from adf_core_python.implement.tactics.default_tactics_ambulance_center import (
    DefaultTacticsAmbulanceCenter,
)
from adf_core_python.implement.tactics.default_tactics_ambulance_team import (
    DefaultTacticsAmbulanceTeam,
)
from adf_core_python.implement.tactics.default_tactics_fire_brigade import (
    DefaultTacticsFireBrigade,
)
from adf_core_python.implement.tactics.default_tactics_fire_station import (
    DefaultTacticsFireStation,
)
from adf_core_python.implement.tactics.default_tactics_police_force import (
    DefaultTacticsPoliceForce,
)
from adf_core_python.implement.tactics.default_tactics_police_office import (
    DefaultTacticsPoliceOffice,
)


class DefaultLoader(AbstractLoader):
    def get_tactics_ambulance_team(self) -> TacticsAmbulanceTeam:
        return DefaultTacticsAmbulanceTeam()

    def get_tactics_fire_brigade(self) -> TacticsFireBrigade:
        return DefaultTacticsFireBrigade()

    def get_tactics_police_force(self) -> TacticsPoliceForce:
        return DefaultTacticsPoliceForce()

    def get_tactics_ambulance_center(self) -> TacticsAmbulanceCenter:
        return DefaultTacticsAmbulanceCenter()

    def get_tactics_fire_station(self) -> TacticsFireStation:
        return DefaultTacticsFireStation()

    def get_tactics_police_office(self) -> TacticsPoliceOffice:
        return DefaultTacticsPoliceOffice()
