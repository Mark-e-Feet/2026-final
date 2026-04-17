from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Ballistician(Unit):
    move: int = 1
    hp: int = 6
    atk: int = 2
    atk_range: int = 10

    def __post_init__(self):
        super().__post_init__()