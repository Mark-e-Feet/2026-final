from dataclasses import dataclass


@dataclass
class Hose:
    x: int
    y: int
    team: str
    move: int = 6
    hp: int = 9
    color: tuple = None
    max_ap: int = 3
    ap: int = 0
    initiative: int = 10
    turn_started: bool = False
    move_delay: float = 0.25
    atk: int = 1
    atk_range: int = 1
    moves_remaining: int = 0
    attacks_remaining: int = 0

    def __post_init__(self):
        if self.color is None:
            self.color = (50, 150, 255) if self.team == 'player' else (200, 80, 80)
        if self.ap == 0:
            self.ap = self.max_ap
        self.moves_remaining = self.move
        self.attacks_remaining = 1

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
