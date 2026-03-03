import collections
from classes.unit import Unit


class GameState:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.units = []
        self.selected = None
        self.highlight_tiles = []
        # sample units (with simple initiative values)
        self.units.append(Unit(1, 1, 'player', move=3, max_ap=4, initiative=12))
        self.units.append(Unit(2, 1, 'player', move=3, max_ap=4, initiative=8))
        self.units.append(Unit(5, 4, 'enemy', move=3, max_ap=3, initiative=10))
        self.units.append(Unit(6, 4, 'enemy', move=3, max_ap=3, initiative=9))

        self.turn_queue = []
        self.current_index = 0
        self.active_unit = None
        self.setup_turn_order()

    def setup_turn_order(self):
        self.turn_queue = [u for u in self.units if u.hp > 0]
        # highest initiative goes first
        self.turn_queue.sort(key=lambda u: u.initiative, reverse=True)
        self.current_index = 0
        if self.turn_queue:
            self.start_unit_turn(self.turn_queue[self.current_index])

    def rebuild_queue(self):
        prev = self.active_unit
        self.turn_queue = [u for u in self.units if u.hp > 0]
        self.turn_queue.sort(key=lambda u: u.initiative, reverse=True)
        if not self.turn_queue:
            self.active_unit = None
            return
        if prev in self.turn_queue:
            self.current_index = self.turn_queue.index(prev)
        else:
            self.current_index = 0

    def start_unit_turn(self, unit: Unit):
        self.active_unit = unit
        unit.reset_ap()
        unit.turn_started = True
        self.selected = None
        self.highlight_tiles = []
        self.attack_targets = []
        # prepare enemy AI pacing
        if unit.team == 'enemy':
            self.ai_target = self.find_nearest_player(unit)
            # initial cooldown before first step uses unit's move_delay
            self.enemy_move_cooldown = unit.move_delay
        else:
            self.ai_target = None
            self.enemy_move_cooldown = 0.0

    def end_unit_turn(self):
        if not self.turn_queue:
            return
        prev = self.active_unit
        if prev:
            prev.turn_started = False
        # rebuild queue to skip dead units
        self.rebuild_queue()
        if not self.turn_queue:
            return
        if prev in self.turn_queue:
            idx = self.turn_queue.index(prev)
            next_idx = (idx + 1) % len(self.turn_queue)
        else:
            next_idx = 0
        self.current_index = next_idx
        self.start_unit_turn(self.turn_queue[self.current_index])

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def unit_at(self, x, y):
        for u in self.units:
            if u.x == x and u.y == y and u.hp > 0:
                return u
        return None

    def neighbors(self, x, y):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                yield nx, ny

    def walkable(self, unit: Unit):
        max_cost = min(unit.move, unit.ap)
        q = collections.deque()
        q.append((unit.x, unit.y, 0))
        seen = {(unit.x, unit.y)}
        res = set()
        while q:
            x, y, d = q.popleft()
            if d > max_cost:
                continue
            res.add((x, y))
            for nx, ny in self.neighbors(x, y):
                if (nx, ny) in seen:
                    continue
                if self.unit_at(nx, ny) is None or (nx, ny) == (unit.x, unit.y):
                    seen.add((nx, ny))
                    q.append((nx, ny, d + 1))
        res.discard((unit.x, unit.y))
        return res

    def on_click(self, tx, ty):
        # only allow player input for the active player unit
        if not self.active_unit or self.active_unit.hp <= 0:
            return
        if self.active_unit.team != 'player':
            return

        u = self.unit_at(tx, ty)
        # select the active unit when clicked
        if u is self.active_unit:
            self.selected = u
            self.highlight_tiles = list(self.walkable(u))
            # populate attack targets (units in range)
            self.attack_targets = [t for t in self.units if t.team != u.team and t.hp > 0 and (abs(t.x - u.x) + abs(t.y - u.y)) <= u.atk_range]
            return

        # move if tile is highlighted and selected is the active unit
        if self.selected is self.active_unit and (tx, ty) in self.highlight_tiles:
            cost = abs(tx - self.active_unit.x) + abs(ty - self.active_unit.y)
            if self.active_unit.spend_ap(cost):
                self.active_unit.x = tx
                self.active_unit.y = ty
                self.selected = None
                self.highlight_tiles = []
                self.attack_targets = []
                # if no AP left, end this unit's turn
                if self.active_unit.ap <= 0:
                    self.end_unit_turn()
                return

        # attack if clicking on an enemy within attack range
        if self.selected is self.active_unit and u and u.team != self.active_unit.team:
            dist = abs(u.x - self.active_unit.x) + abs(u.y - self.active_unit.y)
            if dist <= self.active_unit.atk_range:
                if self.active_unit.spend_ap(1):
                    u.take_damage(self.active_unit.atk)
                    # remove dead units, rebuild queues
                    self.cleanup_dead()
                    # clear selection/targets after attack
                    self.selected = None
                    self.highlight_tiles = []
                    self.attack_targets = []
                    # end unit turn if no AP left
                    if self.active_unit.ap <= 0:
                        self.end_unit_turn()

    def update(self, dt):
        # handle enemy AI pacing: move one AP per cooldown tick
        if self.active_unit and self.active_unit.team == 'enemy' and self.active_unit.hp > 0:
            self.enemy_move_cooldown -= dt
            if self.enemy_move_cooldown <= 0:
                e = self.active_unit
                if e.ap <= 0:
                    # ensure a small final pause before ending so last move is visible
                    self.enemy_move_cooldown = e.move_delay
                    # will end on next update after cooldown
                    return
                # recompute target if needed
                if not self.ai_target or self.ai_target.hp <= 0:
                    self.ai_target = self.find_nearest_player(e)
                if not self.ai_target:
                    self.end_unit_turn()
                    return
                # move one tile towards target
                dx = 0 if e.x == self.ai_target.x else (1 if self.ai_target.x > e.x else -1)
                dy = 0 if e.y == self.ai_target.y else (1 if self.ai_target.y > e.y else -1)
                moved = False
                # attempt horizontal move first
                if dx != 0:
                    nx, ny = e.x + dx, e.y
                    if self.unit_at(nx, ny) is None and self.in_bounds(nx, ny):
                        e.x, e.y = nx, ny
                        e.ap -= 1
                        moved = True
                if not moved and dy != 0:
                    nx, ny = e.x, e.y + dy
                    if self.unit_at(nx, ny) is None and self.in_bounds(nx, ny):
                        e.x, e.y = nx, ny
                        e.ap -= 1
                        moved = True
                # set cooldown for next step using unit's move_delay
                self.enemy_move_cooldown = e.move_delay
                # if couldn't move or no AP left, end turn after cooldown expires
                if not moved or e.ap <= 0:
                    # next update will see ap<=0 and end the turn after cooldown
                    pass

    def find_nearest_player(self, unit: Unit):
        players = [u for u in self.units if u.team == 'player' and u.hp > 0]
        if not players:
            return None
        return min(players, key=lambda p: abs(p.x - unit.x) + abs(p.y - unit.y))

    def cleanup_dead(self):
        # Remove units with hp <= 0 and rebuild turn queue
        dead = [u for u in self.units if u.hp <= 0]
        if not dead:
            return
        # remove dead units
        self.units = [u for u in self.units if u.hp > 0]
        # if active unit died, end its turn and advance
        if self.active_unit and self.active_unit.hp <= 0:
            self.end_unit_turn()
            return
        # otherwise rebuild queue to ensure consistency
        self.rebuild_queue()
        # if active unit was removed from queue, pick a valid one
        if self.active_unit and self.active_unit not in self.turn_queue:
            if self.turn_queue:
                self.current_index = 0
                self.start_unit_turn(self.turn_queue[self.current_index])
            else:
                self.active_unit = None
