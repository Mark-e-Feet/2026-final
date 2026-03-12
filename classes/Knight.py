from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Knight(Unit):
    move: int = 2
    hp: int = 12
    atk: int = 4
    atk_range: int = 1

    def __post_init__(self):
        super().__post_init__()
