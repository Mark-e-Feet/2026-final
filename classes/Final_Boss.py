from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Final_Boss(Unit):
    move: int = 0
    hp: int = 80
    atk: int = 7
    atk_range: int = 10

    def __post_init__(self):
        super().__post_init__()