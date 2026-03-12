from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Archer(Unit):
    move: int = 3
    hp: int = 8
    atk: int = 2
    atk_range: int = 3

    def __post_init__(self):
        super().__post_init__()
