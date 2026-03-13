from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Boss2(Unit):
    move: int = 3
    hp: int = 25
    atk: int = 5
    atk_range: int = 3

    def __post_init__(self):
        super().__post_init__()

    def get_exp_reward(self):
        """Calculate experience reward for defeating Boss2 - gives bonus XP"""
        base_exp = 5
        level_bonus = self.level * 3
        boss_bonus = 20  # Extra 20 XP for defeating the boss
        return base_exp + level_bonus + boss_bonus