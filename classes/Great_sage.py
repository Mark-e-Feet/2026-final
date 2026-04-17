from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Great_sage(Unit):
    move: int = 4
    hp: int = 16
    atk: int = 5
    atk_range: int = 5

    def __post_init__(self):
        super().__post_init__()