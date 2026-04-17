from classes.unit import Unit
from dataclasses import dataclass


@dataclass
class Pikachu(Unit):
    move: int = 4
    hp: int = 8
    atk: int = 4
    atk_range: int = 3
    level: int = 1
    exp: int = 0
    exp_to_next_level: int = 10
    max_hp: int = 8

    def __post_init__(self):
        super().__post_init__()
        self.name = "Pikachu"

    def gain_exp(self, amount: int):
        """Add experience and check for level up"""
        self.exp += amount
        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level_up()

    def level_up(self):
        """Level up - increase stats"""
        self.level += 1
        self.max_hp += 2
        self.hp = self.max_hp
        self.atk += 1
        self.atk_range += 1
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        print(f"Pikachu leveled up to {self.level}! HP: {self.hp}, ATK: {self.atk}, Range: {self.atk_range}")