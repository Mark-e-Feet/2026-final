from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Horse(Unit):
    move: int = 6
    hp: int = 9
    atk: int = 1
    atk_range: int = 1

    def __post_init__(self):
        super().__post_init__()
