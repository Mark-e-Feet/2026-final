from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Soldier(Unit):
    move: int = 4
    hp: int = 8
    atk: int = 2
    atk_range: int = 2

    def __post_init__(self):
        super().__post_init__()