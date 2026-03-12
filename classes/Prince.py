from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Prince(Unit):
    move: int = 4
    hp: int = 10
    atk: int = 3
    atk_range: int = 1

    def __post_init__(self):
        super().__post_init__()
