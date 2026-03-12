from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Boss1(Unit):
    move: int = 0
    hp: int = 18
    atk: int = 4
    atk_range: int = 3

    def __post_init__(self):
        super().__post_init__()

    def get_exp_reward(self):
        """Calculate experience reward for defeating Boss1 - gives bonus XP"""
        base_exp = 5
        level_bonus = self.level * 2
        boss_bonus = 15  # Extra 15 XP for defeating the boss
        return base_exp + level_bonus + boss_bonus
