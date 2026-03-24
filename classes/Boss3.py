from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Boss3(Unit):
    move: int = 0
    hp: int = 29
    atk: int = 2
    atk_range: int = 24

    def __post_init__(self):
        super().__post_init__()

    def get_exp_reward(self):
        """Calculate experience reward for defeating Boss3 - gives bonus XP"""
        base_exp = 5
        level_bonus = self.level * 3
        boss_bonus = 25  # Extra 25 XP for defeating the boss
        return base_exp + level_bonus + boss_bonus