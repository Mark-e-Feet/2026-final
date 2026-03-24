from classes.unit import Unit
from dataclasses import dataclass

@dataclass
class Healer(Unit):
    move: int = 4
    hp: int = 6
    max_hp: int = 6  # Add max_hp for healing calculations
    atk: int = 0
    atk_range: int = 0

    def __post_init__(self):
        super().__post_init__()

    def heal(self, target_unit):
        """Heal a target unit for 1 HP"""
        if target_unit and target_unit.hp < target_unit.max_hp:
            target_unit.hp = min(target_unit.hp + 1, target_unit.max_hp)
            return True
        return False