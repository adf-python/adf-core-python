from abc import ABC, abstractmethod


class AbstractLoader(ABC):
    def __init__(self) -> None:
        self._team_name: str = ""

    def get_team_name(self) -> str:
        return self._team_name

    def set_team_name(self, team_name: str) -> None:
        self._team_name = team_name

    # TODO: Add more abstract methods here
    @abstractmethod
    def get_tactics_ambulance_team(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_tactics_fire_brigade(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_tactics_police_force(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_tactics_ambulance_centre(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_tactics_fire_station(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_tactics_police_office(self) -> None:
        raise NotImplementedError
