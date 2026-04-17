from dataclasses import dataclass
from level_config import get_exp_required, get_class_stats, MAX_LEVEL


# Global flag for double XP mode
DOUBLE_XP_ENABLED = False

# Global flag for knight transformation mode
KNIGHTFALL_MODE = False


@dataclass
class Unit:
    x: int
    y: int
    team: str
    name: str = ""
    move: int = 3
    hp: int = 10
    max_hp: int = 10
    color: tuple = None
    max_ap: int = 3
    ap: int = 0
    initiative: int = 10
    turn_started: bool = False
    move_delay: float = 0.25
    atk: int = 3
    atk_range: int = 1
    moves_remaining: int = 0
    attacks_remaining: int = 0
    has_acted_this_phase: bool = False
    
    # Leveling system attributes
    level: int = 1
    exp: int = 0
    exp_to_next_level: int = 10
    kills: int = 0
    
    # Base stats for leveling calculations
    base_hp: int = 10
    base_atk: int = 3
    base_move: int = 3

    def __post_init__(self):
        if self.color is None:
            self.color = (50, 150, 255) if self.team == 'player' else (200, 80, 80)
        if self.ap == 0:
            self.ap = self.max_ap
        self.moves_remaining = self.move
        self.attacks_remaining = 1
        
        # Initialize base stats for leveling
        self.base_hp = self.hp
        self.max_hp = self.hp
        self.base_atk = self.atk
        self.base_move = self.move
        
        # Initialize level up announcement system
        self.level_up_announcement = False
        self.level_up_timer = 0.0
        
        # Healing system attributes
        self.heal_range: int = 1  # Healers can heal adjacent units
        self.heals_remaining: int = 1  # Healers get 1 heal per turn

    def spend_ap(self, cost: int) -> bool:
        if cost <= 0:
            return True
        if self.ap >= cost:
            self.ap -= cost
            return True
        return False

    def can_move(self, distance: int) -> bool:
        return self.moves_remaining >= distance

    def spend_move(self, distance: int) -> bool:
        if self.can_move(distance):
            self.moves_remaining -= distance
            return True
        return False

    def can_attack(self) -> bool:
        return self.attacks_remaining > 0
    
    def can_heal(self) -> bool:
        return self.heals_remaining > 0
    
    def spend_heal(self) -> bool:
        if self.can_heal():
            self.heals_remaining -= 1
            return True
        return False
    
    def reset_heals(self):
        self.heals_remaining = 1
    
    def get_heal_amount(self):
        """Calculate heal amount based on level (2 HP + 1 HP every 3 levels)"""
        base_heal = 2
        level_bonus = (self.level - 1) // 3  # +1 HP every 3 levels
        return base_heal + level_bonus

    def spend_attack(self) -> bool:
        if self.can_attack():
            self.attacks_remaining -= 1
            return True
        return False

    def reset_ap(self):
        self.ap = self.max_ap
        self.moves_remaining = self.move
        self.attacks_remaining = 1
        self.reset_heals()

    def take_damage(self, amount: int):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def gain_exp(self, amount: int):
        """Add experience points and check for level up"""
        if self.team != 'player':  # Only player units can level up
            return
        
        # Apply double XP if enabled
        if DOUBLE_XP_ENABLED:
            amount *= 2
            
        self.exp += amount
        
        # Check for level up - allow multiple level-ups per turn
        while self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        """Increase unit level and improve stats using configuration system"""
        # Check level cap
        if self.level >= MAX_LEVEL:
            return  # Can't level up anymore
            
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = get_exp_required(self.level + 1)
        
        # Get new stats from configuration
        class_name = self.__class__.__name__
        new_stats = get_class_stats(class_name, self.level)
        
        # Apply new stats
        self.max_hp = new_stats["hp"]
        self.hp = self.max_hp  # Full heal on level up
        self.atk = new_stats["atk"]
        self.move = new_stats["move"]
        self.atk_range = new_stats["range"]
        self.moves_remaining = self.move
        
        # Update base stats for future calculations
        self.base_hp = self.max_hp
        self.base_atk = self.atk
        self.base_move = self.move
        
        # Set level up announcement flag
        self.level_up_announcement = True
        self.level_up_timer = 3.0  # Show announcement for 3 seconds

    def get_exp_reward(self):
        """Calculate experience reward for defeating this unit"""
        base_exp = 5
        level_bonus = self.level * 2
        return base_exp + level_bonus

    def set_level(self, target_level: int):
        """Set unit to a specific level using configuration system"""
        if target_level < 1:
            target_level = 1
        elif target_level > MAX_LEVEL:
            target_level = MAX_LEVEL
            
        # Set level directly
        self.level = target_level
        
        # Get stats from configuration
        class_name = self.__class__.__name__
        new_stats = get_class_stats(class_name, target_level)
        
        # Apply new stats
        self.max_hp = new_stats["hp"]
        self.hp = self.max_hp  # Full health
        self.atk = new_stats["atk"]
        self.move = new_stats["move"]
        self.atk_range = new_stats["range"]
        self.moves_remaining = self.move
        
        # Update base stats for future calculations
        self.base_hp = self.max_hp
        self.base_atk = self.atk
        self.base_move = self.move
        
        # Set experience for current level
        self.exp = 0
        self.exp_to_next_level = get_exp_required(target_level + 1)
