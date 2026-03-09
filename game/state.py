import collections
from classes.unit import Unit
from classes.Prince import Prince
from classes.Archer import Archer
from classes.Bandit import Bandit

class GameState:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.units = []
        self.selected = None
        self.highlight_tiles = []
        self.game_over = False
        self.victory = False
        self.current_level = 1
        self.current_phase = 'player'  # 'player' or 'enemy'
        self.phase_timer = 0.0
        self.setup_level()

    def setup_level(self):
        """Setup units for the current level"""
        self.units = []
        self.game_over = False
        self.victory = False
        self.current_phase = 'player'
        self.phase_timer = 0.0
        
        # Player units (keep same positions and health across levels)
        if self.current_level == 1:
            self.units.append(Prince(2, 2, 'player'))
            self.units.append(Archer(3, 2, 'player'))
        else:
            # Restore player units with full health for new levels
            self.units.append(Prince(2, 2, 'player', hp=10))
            self.units.append(Archer(3, 2, 'player', hp=8))
        
        # Enemy units based on level
        if self.current_level == 1:
            self.units.append(Bandit(8, 6, 'enemy'))
            self.units.append(Bandit(9, 6, 'enemy'))
        elif self.current_level == 2:
            self.units.append(Bandit(7, 5, 'enemy'))
            self.units.append(Bandit(9, 6, 'enemy'))
            self.units.append(Bandit(8, 7, 'enemy'))
        elif self.current_level == 3:
            self.units.append(Bandit(6, 4, 'enemy'))
            self.units.append(Bandit(8, 5, 'enemy'))
            self.units.append(Bandit(9, 6, 'enemy'))
            self.units.append(Bandit(7, 7, 'enemy'))
        else:
            # Endless mode - add more enemies each level
            num_enemies = min(2 + self.current_level, 8)
            for i in range(num_enemies):
                x = 6 + (i % 4)
                y = 4 + (i // 2)
                self.units.append(Bandit(x, y, 'enemy'))

        # Reset all units' actions for player phase
        self.reset_all_unit_actions()

    def reset_all_unit_actions(self):
        """Reset actions for all units of the current phase"""
        for unit in self.units:
            unit.reset_ap()

    def next_level(self):
        """Advance to the next level"""
        self.current_level += 1
        self.setup_level()

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
        # no inactivity timer when auto-end is disabled
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
        max_cost = unit.moves_remaining
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
        # only allow player input during player phase
        if self.current_phase != 'player':
            return

        u = self.unit_at(tx, ty)
        # select a player unit when clicked
        if u and u.team == 'player':
            self.selected = u
            self.highlight_tiles = list(self.walkable(u))
            # populate attack targets (units in range)
            self.attack_targets = [t for t in self.units if t.team != u.team and t.hp > 0 and (abs(t.x - u.x) + abs(t.y - u.y)) <= u.atk_range]
            return

        # move if tile is highlighted and selected is a player unit
        if self.selected and self.selected.team == 'player' and (tx, ty) in self.highlight_tiles:
            cost = abs(tx - self.selected.x) + abs(ty - self.selected.y)
            if self.selected.spend_move(cost):
                self.selected.x = tx
                self.selected.y = ty
                self.selected = None
                self.highlight_tiles = []
                self.attack_targets = []
                return

        # attack if clicking on an enemy within attack range
        if self.selected and self.selected.team == 'player' and u and u.team != self.selected.team:
            dist = abs(u.x - self.selected.x) + abs(u.y - self.selected.y)
            if dist <= self.selected.atk_range:
                if self.selected.spend_attack():
                    u.take_damage(self.selected.atk)
                    # remove dead units, rebuild queues
                    self.cleanup_dead()
                    # clear selection/targets after attack
                    self.selected = None
                    self.highlight_tiles = []
                    self.attack_targets = []
                    return

    def update(self, dt):
        # Handle victory timer for level progression
        if self.game_over and self.victory and hasattr(self, 'victory_timer'):
            self.victory_timer -= dt
            if self.victory_timer <= 0:
                self.next_level()
                return
        
        # Update phase announcement timers
        if hasattr(self, 'phase_announcement_timer') and self.phase_announcement_timer > 0:
            self.phase_announcement_timer -= dt
        
        # Handle phase transitions
        if self.current_phase == 'player':
            # Check if player phase should end (all player units out of actions)
            players = [u for u in self.units if u.team == 'player' and u.hp > 0]
            if players and all(u.moves_remaining <= 0 and u.attacks_remaining <= 0 for u in players):
                self.start_enemy_phase()
        elif self.current_phase == 'enemy':
            # Handle enemy AI during enemy phase
            self.phase_timer -= dt
            if self.phase_timer > 0:
                self.update_enemy_ai(dt)
                # Check if all enemies have finished acting
                enemies = [u for u in self.units if u.team == 'enemy' and u.hp > 0]
                if enemies and all(hasattr(u, 'has_acted_this_phase') and u.has_acted_this_phase for u in enemies):
                    # All enemies done, end phase early
                    self.phase_timer = 0
            else:
                # Enemy phase ended, start player phase
                self.start_player_phase()

    def start_enemy_phase(self):
        """Start the enemy phase"""
        self.current_phase = 'enemy'
        self.phase_timer = 5.0  # Enemy phase lasts 5 seconds
        self.phase_announcement_timer = 0.5  # Show announcement for 0.5 seconds
        self.selected = None
        self.highlight_tiles = []
        self.attack_targets = []
        # Reset all enemy actions
        for unit in self.units:
            if unit.team == 'enemy':
                unit.reset_ap()
                unit.ai_target = self.find_nearest_player(unit)
                unit.enemy_move_cooldown = unit.move_delay
                unit.has_acted_this_phase = False
        # Start with first enemy
        self.current_enemy_index = 0
        self.enemy_turn_timer = 1.0  # Wait 1 second before first enemy acts

    def start_player_phase(self):
        """Start the player phase"""
        self.current_phase = 'player'
        self.phase_announcement_timer = 0.5  # Show announcement for 0.5 seconds
        self.selected = None
        self.highlight_tiles = []
        self.attack_targets = []
        # Reset all player actions
        for unit in self.units:
            if unit.team == 'player':
                unit.reset_ap()

    def update_enemy_ai(self, dt):
        """Update enemy AI - both enemies move during their respective turns"""
        # Wait for enemy turn timer
        if hasattr(self, 'enemy_turn_timer') and self.enemy_turn_timer > 0:
            self.enemy_turn_timer -= dt
            return
        
        # Get list of alive enemies
        enemies = [u for u in self.units if u.team == 'enemy' and u.hp > 0]
        if not enemies:
            return
        
        # Check if current enemy index is valid
        if self.current_enemy_index >= len(enemies):
            # All enemies have acted, end phase
            return
        
        current_enemy = enemies[self.current_enemy_index]
        
        # Skip if this enemy has already acted
        if current_enemy.has_acted_this_phase:
            # Move to next enemy after a delay
            self.current_enemy_index += 1
            self.enemy_turn_timer = 0.5  # 0.5 second delay between enemies
            return
        
        # Handle current enemy's turn - allow all enemies to move
        for enemy in enemies:
            if enemy.moves_remaining > 0 and enemy.ai_target:
                enemy.enemy_move_cooldown -= dt
                if enemy.enemy_move_cooldown <= 0:
                    # All enemies can move towards their targets
                    dx = 0 if enemy.x == enemy.ai_target.x else (1 if enemy.ai_target.x > enemy.x else -1)
                    dy = 0 if enemy.y == enemy.ai_target.y else (1 if enemy.ai_target.y > enemy.y else -1)
                    moved = False
                    
                    if dx != 0:
                        nx, ny = enemy.x + dx, enemy.y
                        if self.unit_at(nx, ny) is None and self.in_bounds(nx, ny):
                            enemy.x, enemy.y = nx, ny
                            enemy.moves_remaining -= 1
                            moved = True
                    if not moved and dy != 0:
                        nx, ny = enemy.x, enemy.y + dy
                        if self.unit_at(nx, ny) is None and self.in_bounds(nx, ny):
                            enemy.x, enemy.y = nx, ny
                            enemy.moves_remaining -= 1
                            moved = True
                    
                    enemy.enemy_move_cooldown = enemy.move_delay
        
        # Only current enemy can attack
        if current_enemy.moves_remaining <= 0 and current_enemy.attacks_remaining <= 0:
            current_enemy.has_acted_this_phase = True
            self.enemy_turn_timer = 0.5  # 0.5 second delay before next enemy
            return
        
        # Check if current enemy can attack
        if current_enemy.ai_target and current_enemy.ai_target.hp > 0:
            if self.can_attack_target(current_enemy, current_enemy.ai_target):
                if current_enemy.spend_attack():
                    current_enemy.ai_target.take_damage(current_enemy.atk)
                    self.cleanup_dead()
                    current_enemy.enemy_move_cooldown = current_enemy.move_delay

    def end_player_phase(self):
        """Manually end the player phase"""
        if self.current_phase == 'player':
            self.start_enemy_phase()

    def can_attack_target(self, attacker, target):
        """Check if attacker can reach target with their attack range"""
        if not target or target.hp <= 0:
            return False
        dist = abs(target.x - attacker.x) + abs(target.y - attacker.y)
        return dist <= attacker.atk_range

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
        # check victory conditions
        self.check_victory()
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

    def check_victory(self):
        if self.game_over:
            return
        
        enemies = [u for u in self.units if u.team == 'enemy' and u.hp > 0]
        players = [u for u in self.units if u.team == 'player' and u.hp > 0]
        
        if not enemies:
            # Victory! Advance to next level after a short delay
            self.game_over = True
            self.victory = True
            self.victory_timer = 2.0  # Show victory for 2 seconds
        elif not players:
            self.game_over = True
            self.victory = False
