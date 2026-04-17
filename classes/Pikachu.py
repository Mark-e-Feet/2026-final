from classes.unit import Unit
from dataclasses import dataclass
from level_config import get_class_stats, get_exp_required


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
        # Apply level-specific stats
        self.apply_level_stats()

    def apply_level_stats(self):
        """Apply stats based on current level using level_config"""
        stats = get_class_stats("Pikachu", self.level)
        self.max_hp = stats["hp"]
        self.hp = stats["hp"]
        self.atk = stats["atk"]
        self.move = stats["move"]
        self.atk_range = stats["range"]
        self.exp_to_next_level = get_exp_required(self.level)

    def gain_exp(self, amount: int):
        """Add experience and check for level up"""
        self.exp += amount
        while self.exp >= self.exp_to_next_level and self.level < 20:  # Max level cap
            self.exp -= self.exp_to_next_level
            self.level_up()

    def level_up(self):
        """Level up - use level_config stats"""
        self.level += 1
        self.apply_level_stats()
        print(f"Pikachu leveled up to {self.level}! HP: {self.hp}, ATK: {self.atk}, Move: {self.move}, Range: {self.atk_range}")

    @classmethod
    def create_for_part(cls, x, y, team, part_level):
        """Create Pikachu with appropriate level for the given part"""
        pikachu = cls(x, y, team)
        
        # Set level based on part
        if part_level >= 18:  # Part 4 (levels 18-23)
            pikachu.level = 7
        elif part_level >= 12:  # Part 3 (levels 12-17)
            pikachu.level = 6
        elif part_level >= 6:   # Part 2 (levels 6-11)
            pikachu.level = 4
        else:                   # Part 1 (levels 1-5)
            pikachu.level = 1
        
        # Apply the appropriate stats for the level
        pikachu.apply_level_stats()
        return pikachu