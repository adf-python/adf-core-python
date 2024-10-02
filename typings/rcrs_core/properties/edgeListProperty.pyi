"""
This type stub file was generated by pyright.
"""

from typing import List
from rcrs_core.properties.property import Property
from rcrs_core.entities.edge import Edge

class EdgeListProperty(Property):
    def __init__(self, urn) -> None:
        ...
    
    def get_fields(self): # -> None:
        ...
    
    def set_fields(self, data): # -> None:
        ...
    
    def set_value(self, _value: List[Edge]): # -> None:
        ...
    
    def set_edges(self, _edges: List[Edge]): # -> None:
        ...
    
    def add_edge(self, _edge): # -> None:
        ...
    
    def clear_edges(self): # -> None:
        ...
    
    def take_value(self, _value): # -> None:
        ...
    
    def copy(self): # -> EdgeListProperty:
        ...
    


