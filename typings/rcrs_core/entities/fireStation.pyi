"""
This type stub file was generated by pyright.
"""

from rcrs_core.entities.building import Building

class FireStationEntity(Building):
    urn = ...
    def __init__(self, entity_id) -> None:
        ...
    
    def copy_impl(self): # -> FireStationEntity:
        ...
    
    def get_entity_name(self): # -> Literal['Fire Station']:
        ...
    
    def set_entity(self, properties): # -> None:
        ...
    


