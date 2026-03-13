from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Srodman(Unit):
    move: int = 4
    hp: int = 11
    atk: int = 2
    atk_range: int = 1

    def __post_init__(self):
        super().__post_init__()