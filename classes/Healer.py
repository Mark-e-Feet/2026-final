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
        """Heal a target unit using the healer's level-based healing amount"""
        if target_unit and target_unit.hp < target_unit.max_hp:
            heal_amount = self.get_heal_amount()
            target_unit.hp = min(target_unit.hp + heal_amount, target_unit.max_hp)
            return True
        return False