from dataclasses import dataclass


@dataclass
class Unit:
    x: int
    y: int
    team: str
    move: int = 3
    hp: int = 10
    color: tuple = None
    max_ap: int = 3
    ap: int = 0
    initiative: int = 10
    turn_started: bool = False
    move_delay: float = 0.25
    atk: int = 3
    atk_range: int = 1

    def __post_init__(self):
        if self.color is None:
            self.color = (50, 150, 255) if self.team == 'player' else (200, 80, 80)
        if self.ap == 0:
            self.ap = self.max_ap

    def spend_ap(self, cost: int) -> bool:
        if cost <= 0:
            return True
        if self.ap >= cost:
            self.ap -= cost
            return True
        return False

    def reset_ap(self):
        self.ap = self.max_ap

    def take_damage(self, amount: int):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0
