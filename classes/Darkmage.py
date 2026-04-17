from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Darkmage(Unit):
    move: int = 2
    hp: int = 10
    atk: int = 3
    atk_range: int = 3

    def __post_init__(self):
        super().__post_init__()