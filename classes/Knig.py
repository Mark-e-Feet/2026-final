from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Knig(Unit):
    move: int = 4
    hp: int = 18
    atk: int = 6
    atk_range: int = 1

    def __post_init__(self):
        super().__post_init__()