from typing import TYPE_CHECKING

from adf_core_python.core.component.abstract_loader import AbstractLoader
from adf_core_python.implement.tactics.default_tactics_ambulance_team import (
    DefaultTacticsAmbulanceTeam,
)

if TYPE_CHECKING:
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


class DefaultLoader(AbstractLoader):
    def get_tactics_ambulance_team(self) -> TacticsAmbulanceTeam:
        return DefaultTacticsAmbulanceTeam()

    # def get_tactics_fire_brigade(self) -> TacticsFireBrigade:
    #     pass

    # def get_tactics_police_force(self) -> TacticsPoliceForce:
    #     pass

    # def get_tactics_ambulance_centre(self) -> TacticsAmbulanceCenter:
    #     pass

    # def get_tactics_fire_station(self) -> TacticsFireStation:
    #     pass

    # def get_tactics_police_office(self) -> TacticsPoliceOffice:
    #     pass
