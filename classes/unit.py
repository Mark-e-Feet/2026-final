from dataclasses import dataclass


@dataclass
class Unit:
    x: int
    y: int
    team: str
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

    def spend_attack(self) -> bool:
        if self.can_attack():
            self.attacks_remaining -= 1
            return True
        return False

    def reset_ap(self):
        self.ap = self.max_ap
        self.moves_remaining = self.move
        self.attacks_remaining = 1

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
            
        self.exp += amount
        # Check for level up
        while self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        """Increase unit level and improve stats"""
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)  # Increase exp requirement
        
        # Improve stats
        hp_increase = max(1, int(self.base_hp * 0.1))  # 10% of base HP
        atk_increase = max(1, int(self.base_atk * 0.15))  # 15% of base attack
        
        self.base_hp += hp_increase
        self.base_atk += atk_increase
        
        # Apply new stats
        self.max_hp = self.base_hp
        self.hp = self.max_hp  # Full heal on level up
        self.atk = self.base_atk
        
        # Increase movement every 3 levels
        if self.level % 3 == 0:
            self.base_move += 1
            self.move = self.base_move
            self.moves_remaining = self.move
        
        # Set level up announcement flag
        self.level_up_announcement = True
        self.level_up_timer = 3.0  # Show announcement for 3 seconds

    def get_exp_reward(self):
        """Calculate experience reward for defeating this unit"""
        base_exp = 5
        level_bonus = self.level * 2
        return base_exp + level_bonus
