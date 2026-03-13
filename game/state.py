import collections
from classes.unit import Unit
from classes.Tristan import Tristan
from classes.Archer import Archer
from classes.Bandit import Bandit
from classes.Horse import Horse
from classes.Knight import Knight
from classes.Mage import Mage
from classes.Srodman import Srodman
from classes.Boss1 import Boss1
from classes.Soldier import Soldier
from classes.Boss2 import Boss2

class GameState:
    def __init__(self, width, height, starting_level=1):
        self.width = width
        self.height = height
        self.units = []
        self.selected = None
        self.highlight_tiles = []
        self.game_over = False
        self.victory = False
        self.current_level = starting_level
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
        
        # Player units (preserve progression across levels)
        if self.current_level == 1:
            self.units.append(Tristan(2, 2, 'player'))
            self.units.append(Archer(3, 2, 'player'))
            self.units.append(Mage(4, 2, 'player'))
        else:
            # For levels > 1, create units with default progression
            # They will be restored from saved progress in next_level()
            tristan = Tristan(2, 2, 'player')
            archer = Archer(3, 2, 'player')
            mage = Mage(4, 2, 'player')
            horse = Horse(5, 2, 'player')    
            
            # Add units based on level
            if self.current_level >= 6:  # Level 6+ - get all units
                srodman = Srodman(6, 2, 'player')
                knight = Knight(7, 2, 'player')
                self.units.extend([tristan, archer, mage, horse, srodman, knight])
            else:
                self.units.extend([tristan, archer, mage, horse])
            

        
        # Enemy units based on level
        if self.current_level == 1:
            self.units.append(Bandit(8, 6, 'enemy'))
            self.units.append(Bandit(9, 6, 'enemy'))
        elif self.current_level == 2:
            self.units.append(Bandit(7, 5, 'enemy'))
            self.units.append(Bandit(9, 6, 'enemy'))
            self.units.append(Knight(8, 7, 'enemy'))
        elif self.current_level == 3:
            self.units.append(Bandit(6, 4, 'enemy'))
            self.units.append(Bandit(8, 5, 'enemy'))
            self.units.append(Knight(9, 6, 'enemy'))
            self.units.append(Horse(7, 7, 'enemy'))
        elif self.current_level == 4:
            self.units.append(Knight(11, 0, 'enemy'))
            self.units.append(Knight(11, 1, 'enemy'))
            self.units.append(Knight(11, 2, 'enemy'))
            self.units.append(Knight(11, 3, 'enemy'))
            self.units.append(Knight(11, 4, 'enemy'))
        elif self.current_level == 5:
            self.units.append(Boss1(11, 7, 'enemy'))
            self.units.append(Horse(10, 7, 'enemy'))
            self.units.append(Horse(11, 6, 'enemy'))
        elif self.current_level == 6:
            # Part 2 - 
            self.units.append(Srodman(15, 10, 'enemy'))
            self.units.append(Srodman(18, 12, 'enemy'))
            self.units.append(Knight(20, 8, 'enemy'))
            self.units.append(Knight(22, 14, 'enemy'))
            self.units.append(Horse(16, 13, 'enemy'))
        elif self.current_level == 7:
            self.units.append(Horse(23, 1, 'enemy'))
            self.units.append(Horse(23, 0, 'enemy'))
            self.units.append(Horse(22, 1, 'enemy'))
            self.units.append(Horse(22, 0, 'enemy'))
            self.units.append(Horse(22, 14, 'enemy'))
            self.units.append(Horse(23, 14, 'enemy'))
            self.units.append(Horse(22, 15, 'enemy'))
            self.units.append(Horse(23, 15, 'enemy'))
        elif self.current_level == 8:
            self.units.append(Soldier(15, 10, 'enemy'))
            self.units.append(Archer(18, 12, 'enemy'))
            self.units.append(Soldier(20, 8, 'enemy'))
            self.units.append(Knight(22, 14, 'enemy'))
            self.units.append(Soldier(16, 13, 'enemy'))
            self.units.append(Horse(16, 3, 'enemy'))
            self.units.append(Soldier(16, 1, 'enemy'))
            self.units.append(Srodman(16, 3, 'enemy'))
        elif self.current_level == 9:
            self.units.append(Mage(0, 15, 'enemy'))
            self.units.append(Knight(12, 8, 'enemy'))
            self.units.append(Mage(23, 0, 'enemy'))
            self.units.append(Knight(13, 8, 'enemy'))
            self.units.append(Mage(23, 15, 'enemy'))
        elif self.current_level == 10:
            self.units.append(Soldier(23, 0, 'enemy'))
            self.units.append(Soldier(23, 1, 'enemy'))
            self.units.append(Soldier(23, 2, 'enemy'))
            self.units.append(Soldier(23, 3, 'enemy'))
            self.units.append(Soldier(23, 4, 'enemy'))
            self.units.append(Soldier(23, 11, 'enemy'))
            self.units.append(Soldier(23, 12, 'enemy'))
            self.units.append(Soldier(23, 14, 'enemy'))    
            self.units.append(Soldier(23, 13, 'enemy'))
            self.units.append(Soldier(23, 15, 'enemy'))
        elif self.current_level == 11:
            self.units.append(Boss2(12, 8, 'enemy'))
            self.units.append(Mage(10, 6, 'enemy'))
            self.units.append(Mage(14, 6, 'enemy'))
            self.units.append(Mage(10, 10, 'enemy'))
            self.units.append(Mage(14, 10, 'enemy'))




            
        
        # Reset all units' actions for player phase
        self.reset_all_unit_actions()

    def restore_unit_progression(self, unit, saved_progress):
        """Restore a unit's leveled stats and progression"""
        unit.level = saved_progress['level']
        unit.exp = saved_progress['exp']
        unit.exp_to_next_level = saved_progress['exp_to_next_level']
        unit.kills = saved_progress['kills']
        unit.base_hp = saved_progress['base_hp']
        unit.base_atk = saved_progress['base_atk']
        unit.base_move = saved_progress['base_move']
        
        # Apply the leveled stats
        unit.max_hp = unit.base_hp
        unit.hp = unit.max_hp  # Full heal between levels
        unit.atk = unit.base_atk
        unit.move = unit.base_move
        unit.moves_remaining = unit.move

    def reset_all_unit_actions(self):
        """Reset actions for all units of the current phase"""
        for unit in self.units:
            unit.reset_ap()

    def next_level(self):
        """Advance to the next level"""
        # Store existing player units to preserve their progress
        existing_player_units = {}
        if hasattr(self, 'units'):
            for unit in self.units:
                if unit.team == 'player' and unit.hp > 0:
                    # Store unit class and progress
                    existing_player_units[unit.__class__.__name__] = {
                        'level': getattr(unit, 'level', 1),
                        'exp': getattr(unit, 'exp', 0),
                        'exp_to_next_level': getattr(unit, 'exp_to_next_level', 10),
                        'kills': getattr(unit, 'kills', 0),
                        'base_hp': getattr(unit, 'base_hp', unit.hp),
                        'base_atk': getattr(unit, 'base_atk', unit.atk),
                        'base_move': getattr(unit, 'base_move', unit.move)
                    }
        
        # Advance to next level
        self.current_level += 1
        self.setup_level()
        
        # Restore progression for levels > 1
        if self.current_level > 1:
            for unit in self.units:
                if unit.team == 'player' and unit.__class__.__name__ in existing_player_units:
                    self.restore_unit_progression(unit, existing_player_units[unit.__class__.__name__])

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
                # Allow movement through empty spaces or same-team units
                occupying_unit = self.unit_at(nx, ny)
                if occupying_unit is None or occupying_unit.team == unit.team:
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
            # Allow moving through same-team units (including stopping on same tile)
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
                    # Store enemy's exp reward before defeating
                    exp_reward = u.get_exp_reward()
                    u.take_damage(self.selected.atk)
                    # Award experience if enemy was defeated
                    if not u.is_alive():
                        self.selected.gain_exp(exp_reward)
                        self.selected.kills += 1
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
        
        # Handle level up announcements for player units
        for unit in self.units:
            if hasattr(unit, 'level_up_announcement') and unit.level_up_announcement:
                unit.level_up_timer -= dt
                if unit.level_up_timer <= 0:
                    unit.level_up_announcement = False
                    unit.level_up_timer = 0.0
        
        # Handle phase transitions
        if self.current_phase == 'player':
            # Check if player phase should end (all player units out of actions)
            players = [u for u in self.units if u.team == 'player' and u.hp > 0]
            if players and all(u.moves_remaining <= 0 and u.attacks_remaining <= 0 for u in players):
                self.start_enemy_phase()
        elif self.current_phase == 'enemy':
            # Handle enemy AI during enemy phase
            self.update_enemy_ai(dt)
            # Check if all enemies have finished acting
            enemies = [u for u in self.units if u.team == 'enemy' and u.hp > 0]
            if enemies and all(hasattr(u, 'has_acted_this_phase') and u.has_acted_this_phase for u in enemies):
                # All enemies done, start player phase
                self.start_player_phase()

    def start_enemy_phase(self):
        """Start the enemy phase"""
        self.current_phase = 'enemy'
        self.phase_timer = 0.0  # No time limit - enemies complete all turns
        self.phase_announcement_timer = 0.5  # Show announcement for 0.5 seconds
        self.selected = None
        self.highlight_tiles = []
        self.attack_targets = []
        self.active_enemy = None  # Track which enemy is currently acting
        self.enemy_movement_timer = 0.0  # Timer to delay enemy movements
        
        # Reset all enemy actions
        for unit in self.units:
            if unit.team == 'enemy':
                unit.reset_ap()
                unit.ai_target = self.find_nearest_player(unit)
                unit.enemy_move_cooldown = unit.move_delay
                unit.has_acted_this_phase = False
        
        # Start with first enemy
        self.current_enemy_index = 0
        # Initialize first enemy's cooldown
        enemies = [u for u in self.units if u.team == 'enemy' and u.hp > 0]
        if enemies:
            enemies[0].enemy_move_cooldown = 0.5  # Short delay before first enemy acts

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
        """Update enemy AI - all enemies can end turn by attacking or choice"""
        # Get list of alive enemies
        enemies = [u for u in self.units if u.team == 'enemy' and u.hp > 0]
        if not enemies:
            # No enemies left, start player phase
            self.start_player_phase()
            return
        
        # Check if current enemy index is valid
        if self.current_enemy_index >= len(enemies):
            # All enemies have acted, end phase
            self.start_player_phase()
            return
        
        current_enemy = enemies[self.current_enemy_index]
        self.active_enemy = current_enemy  # Set as currently acting enemy
        
        # Skip if this enemy has already acted
        if hasattr(current_enemy, 'has_acted_this_phase') and current_enemy.has_acted_this_phase:
            # Move to next enemy immediately
            self.current_enemy_index += 1
            if self.current_enemy_index < len(enemies):
                self.active_enemy = enemies[self.current_enemy_index]
                # Reset the next enemy's cooldown to ensure proper behavior 
                if hasattr(self.active_enemy, 'enemy_move_cooldown'):
                    self.active_enemy.enemy_move_cooldown = self.active_enemy.move_delay
            else:
                self.active_enemy = None
            return
        
        # Handle enemy cooldown
        if hasattr(current_enemy, 'enemy_move_cooldown'):
            current_enemy.enemy_move_cooldown -= dt
            if current_enemy.enemy_move_cooldown <= 0:
                # Check if can attack first
                if hasattr(current_enemy, 'ai_target') and current_enemy.ai_target and current_enemy.ai_target.hp > 0:
                    if self.can_attack_target(current_enemy, current_enemy.ai_target):
                        if hasattr(current_enemy, 'spend_attack') and current_enemy.spend_attack():
                            current_enemy.ai_target.take_damage(current_enemy.atk)
                            self.cleanup_dead()
                            if hasattr(current_enemy, 'has_acted_this_phase'):
                                current_enemy.has_acted_this_phase = True
                            # Move to next enemy immediately
                            self.current_enemy_index += 1
                            if self.current_enemy_index < len(enemies):
                                self.active_enemy = enemies[self.current_enemy_index]
                                self.active_enemy.enemy_move_cooldown = 0.5
                            else:
                                self.active_enemy = None
                            return
                
                # Try to move towards target
                if hasattr(current_enemy, 'moves_remaining') and current_enemy.moves_remaining > 0 and hasattr(current_enemy, 'ai_target') and current_enemy.ai_target:
                    dx = 0 if current_enemy.x == current_enemy.ai_target.x else (1 if current_enemy.ai_target.x > current_enemy.x else -1)
                    dy = 0 if current_enemy.y == current_enemy.ai_target.y else (1 if current_enemy.ai_target.y > current_enemy.y else -1)
                    moved = False
                    
                    # Try horizontal movement first
                    if dx != 0:
                        nx, ny = current_enemy.x + dx, current_enemy.y
                        occupying_unit = self.unit_at(nx, ny)
                        # Allow moving through same-team units but prevent landing on same spot
                        if (occupying_unit is None or occupying_unit == current_enemy) and self.in_bounds(nx, ny):
                            current_enemy.x, current_enemy.y = nx, ny
                            current_enemy.moves_remaining -= 1
                            moved = True
                    
                    # Try vertical movement if horizontal didn't work
                    if not moved and dy != 0:
                        nx, ny = current_enemy.x, current_enemy.y + dy
                        occupying_unit = self.unit_at(nx, ny)
                        # Allow moving through same-team units but prevent landing on same spot
                        if (occupying_unit is None or occupying_unit == current_enemy) and self.in_bounds(nx, ny):
                            current_enemy.x, current_enemy.y = nx, ny
                            current_enemy.moves_remaining -= 1
                            moved = True
                    
                    if moved:
                        # Check if can attack after moving
                        if self.can_attack_target(current_enemy, current_enemy.ai_target):
                            if hasattr(current_enemy, 'spend_attack') and current_enemy.spend_attack():
                                current_enemy.ai_target.take_damage(current_enemy.atk)
                                self.cleanup_dead()
                                if hasattr(current_enemy, 'has_acted_this_phase'):
                                    current_enemy.has_acted_this_phase = True
                                # Move to next enemy immediately
                                self.current_enemy_index += 1
                                if self.current_enemy_index < len(enemies):
                                    self.active_enemy = enemies[self.current_enemy_index]
                                    self.active_enemy.enemy_move_cooldown = 0.5
                                else:
                                    self.active_enemy = None
                                return
                        
                        # Reset cooldown for next action
                        current_enemy.enemy_move_cooldown = 0.3
                    else:
                        # Can't move (blocked), end turn
                        if hasattr(current_enemy, 'has_acted_this_phase'):
                            current_enemy.has_acted_this_phase = True
                        self.current_enemy_index += 1
                        if self.current_enemy_index < len(enemies):
                            self.active_enemy = enemies[self.current_enemy_index]
                            self.active_enemy.enemy_move_cooldown = 0.5
                        else:
                            self.active_enemy = None
                        return
                else:
                    # No movement left or no target, end turn
                    if hasattr(current_enemy, 'has_acted_this_phase'):
                        current_enemy.has_acted_this_phase = True
                    self.current_enemy_index += 1
                    if self.current_enemy_index < len(enemies):
                        self.active_enemy = enemies[self.current_enemy_index]
                        self.active_enemy.enemy_move_cooldown = 0.5
                    else:
                        self.active_enemy = None
                    return
        
        # Check if all enemies have finished their turns
        all_acted = all(hasattr(enemy, 'has_acted_this_phase') and enemy.has_acted_this_phase for enemy in enemies)
        if all_acted:
            # All enemies done, start player phase
            self.start_player_phase()
        
        # Safety check: if current enemy has no movement and no attacks, end its turn
        if current_enemy and current_enemy.moves_remaining <= 0 and current_enemy.attacks_remaining <= 0:
            if not current_enemy.has_acted_this_phase:
                current_enemy.has_acted_this_phase = True
            self.current_enemy_index += 1
            if self.current_enemy_index < len(enemies):
                self.active_enemy = enemies[self.current_enemy_index]
                self.active_enemy.enemy_move_cooldown = 0.5
            else:
                self.active_enemy = None

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
        # Remove units with hp <= 0
        dead = [u for u in self.units if u.hp <= 0]
        if not dead:
            return
        # remove dead units
        self.units = [u for u in self.units if u.hp > 0]
        # check victory conditions
        self.check_victory()
        # if active enemy died, advance to next enemy
        if hasattr(self, 'active_enemy') and self.active_enemy and self.active_enemy.hp <= 0:
            self.active_enemy.has_acted_this_phase = True
            self.enemy_turn_timer = 3.0  # 3 second delay before next enemy
            self.active_enemy = None

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
