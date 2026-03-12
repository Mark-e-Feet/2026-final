from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Mage(Unit):
    move: int = 2
    hp: int = 7
    atk: int = 4
    atk_range: int = 3

    def __post_init__(self):
        super().__post_init__()
