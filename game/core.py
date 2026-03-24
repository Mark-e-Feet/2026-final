import pygame
from game.state import GameState


class Game:
    def __init__(self, width=12, height=8, tile=80, screen=None, starting_level=1):
        self.width = width
        self.height = height
        self.tile = tile
        
        # Camera/viewport system for scrolling
        self.camera_x = 0
        self.camera_y = 0
        self.viewport_width = 12  # Visible tiles horizontally
        self.viewport_height = 8  # Visible tiles vertically
        self.scroll_speed = 8  # Pixels per frame when holding key (increased for better visibility)
        self.enable_scrolling = False  # Enable after boss victory
        
        # Track which keys are currently pressed
        self.keys_pressed = set()
        
        # Use provided screen or create new one
        if screen:
            self.screen = screen
        else:
            self.screen = pygame.display.set_mode((self.viewport_width * tile, self.viewport_height * tile + 80))
            pygame.display.set_caption("Heroes of Tharen")
        
        self.clock = pygame.time.Clock()
        self.state = GameState(width, height, starting_level)
        self.font = pygame.font.SysFont(None, 24)
        self.running = True
        
        # Load terrain images
        try:
            self.grass_image = pygame.image.load("assets/grass.png")
            self.dirt_image = pygame.image.load("assets/dirtpath.png")
            self.castle_image = pygame.image.load("assets/castle.png")
            self.road_image = pygame.image.load("assets/roed.png")
            self.destroyed_house_image = pygame.image.load("assets/destroyed house.png")
            # Scale images to tile size
            self.grass_image = pygame.transform.scale(self.grass_image, (tile, tile))
            self.dirt_image = pygame.transform.scale(self.dirt_image, (tile, tile))
            self.castle_image = pygame.transform.scale(self.castle_image, (tile, tile))
            self.road_image = pygame.transform.scale(self.road_image, (tile, tile))
            self.destroyed_house_image = pygame.transform.scale(self.destroyed_house_image, (tile, tile))
        except pygame.error as e:
            print(f"Could not load terrain images: {e}")
            # Fallback to solid colors if images fail to load
            self.grass_image = None
            self.dirt_image = None
            self.castle_image = None
            self.road_image = None
            self.destroyed_house_image = None
        
        # Update state dimensions if different from default
        self.state.width = width
        self.state.height = height
        
        # Boss victory story system
        self.boss_victory_story_active = False
        self.boss_victory_story_timer = 0.0
        self.boss_victory_story_duration = 8.0  # Show for 8 seconds
        self.boss_story_scroll_offset = 0.0
        self.boss_story_scroll_speed = 0.1
        
        # Boss 2 victory story system
        self.boss2_victory_story_active = False
        self.boss2_victory_story_timer = 0.0
        self.boss2_victory_story_duration = 8.0  # Show for 8 seconds
        self.boss2_story_scroll_offset = 0.0
        self.boss2_story_scroll_speed = 0.1
        
        # Track if Level transitions have been done
        self.level_6_transition_done = False
        self.level_12_transition_done = False

    def get_level_name(self):
        """Get display name for current level"""
        if self.state.current_level == 5:
            return "BOSS"
        else:
            return f"Level {self.state.current_level}"

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
            pygame.display.flip()

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                # Convert mouse coordinates to world coordinates accounting for camera
                world_x = mx + self.camera_x
                world_y = my + self.camera_y
                tx = world_x // self.tile
                ty = world_y // self.tile
                if ty < self.height:
                    self.state.on_click(tx, ty)
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    if self.state.current_phase == 'player':
                        self.state.end_player_phase()
                # Skip boss story with any key
                if self.boss_victory_story_active:
                    self.boss_victory_story_active = False
                    self.state.next_level()
                # Skip Boss 2 story with any key
                if self.boss2_victory_story_active:
                    self.boss2_victory_story_active = False
                    self.state.next_level()
                # Return to main menu when defeated
                if self.state.game_over and not self.state.victory:
                    self.running = False
                # Handle scrolling when enabled - track key press
                if self.enable_scrolling and ev.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d, pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s]:
                    self.keys_pressed.add(ev.key)
            elif ev.type == pygame.KEYUP:
                # Remove key from pressed set when released
                if ev.key in self.keys_pressed:
                    self.keys_pressed.remove(ev.key)

    def update(self, dt):
        self.state.update(dt)
        
        # Handle continuous scrolling when keys are held down
        if self.enable_scrolling and self.keys_pressed:
            # Calculate max scroll boundaries
            max_x = max(0, (self.width - self.viewport_width) * self.tile)
            max_y = max(0, (self.height - self.viewport_height) * self.tile)
            
            # Handle horizontal scrolling
            if pygame.K_LEFT in self.keys_pressed or pygame.K_a in self.keys_pressed:
                self.camera_x = max(0, self.camera_x - self.scroll_speed)
            if pygame.K_RIGHT in self.keys_pressed or pygame.K_d in self.keys_pressed:
                self.camera_x = min(max_x, self.camera_x + self.scroll_speed)
            
            # Handle vertical scrolling
            if pygame.K_UP in self.keys_pressed or pygame.K_w in self.keys_pressed:
                self.camera_y = max(0, self.camera_y - self.scroll_speed)
            if pygame.K_DOWN in self.keys_pressed or pygame.K_s in self.keys_pressed:
                self.camera_y = min(max_y, self.camera_y + self.scroll_speed)
        
        # Camera tracking for active enemy during enemy phase
        if self.enable_scrolling and hasattr(self.state, 'active_enemy') and self.state.active_enemy:
            # Calculate desired camera position to center on active enemy
            target_x = self.state.active_enemy.x * self.tile - (self.viewport_width * self.tile) // 2
            target_y = self.state.active_enemy.y * self.tile - (self.viewport_height * self.tile) // 2
            
            # Smooth camera movement towards target
            camera_speed = 12  # Faster camera for enemy tracking
            if abs(target_x - self.camera_x) > camera_speed:
                if target_x > self.camera_x:
                    self.camera_x += camera_speed
                else:
                    self.camera_x -= camera_speed
            else:
                self.camera_x = target_x
                
            if abs(target_y - self.camera_y) > camera_speed:
                if target_y > self.camera_y:
                    self.camera_y += camera_speed
                else:
                    self.camera_y -= camera_speed
            else:
                self.camera_y = target_y
            
            # Clamp camera to valid boundaries
            max_x = max(0, (self.width - self.viewport_width) * self.tile)
            max_y = max(0, (self.height - self.viewport_height) * self.tile)
            self.camera_x = max(0, min(max_x, self.camera_x))
            self.camera_y = max(0, min(max_y, self.camera_y))
        
        # Check for boss victory and start story
        if self.state.game_over and self.state.victory and self.state.current_level == 5 and not self.boss_victory_story_active:
            self.boss_victory_story_active = True
            self.boss_victory_story_timer = self.boss_victory_story_duration
            self.boss_story_scroll_offset = 0.0
        
        # Check for Boss 2 victory and start story
        if self.state.game_over and self.state.victory and self.state.current_level == 11 and not self.boss2_victory_story_active:
            self.boss2_victory_story_active = True
            self.boss2_victory_story_timer = self.boss2_victory_story_duration
            self.boss2_story_scroll_offset = 0.0
        
        # Check for Level 12 transition to ultra-expanded battlefield (only once)
        if self.state.current_level == 12 and not self.level_12_transition_done:
            # Expand to ultra battlefield and enable scrolling
            self.width = 12
            self.height = 24
            self.viewport_width = 12  # Keep viewport same size
            self.viewport_height = 8  # Keep viewport same size
            self.enable_scrolling = True  # Enable scrolling for ultra battlefield
            # Update state dimensions
            self.state.width = 12
            self.state.height = 24
            # Reset camera position
            self.camera_x = 0
            self.camera_y = 0
            # Mark transition as done
            self.level_12_transition_done = True
        
        # Check for Level 6 transition to expanded battlefield (only once)
        if self.state.current_level == 6 and not self.level_6_transition_done and not self.enable_scrolling:
            # Enable scrolling and expand battlefield
            self.enable_scrolling = True
            self.width = 24
            self.height = 16
            self.viewport_width = 12  # Keep viewport same size
            self.viewport_height = 8  # Keep viewport same size
            # Update state dimensions
            self.state.width = 24
            self.state.height = 16
            # Reset camera position
            self.camera_x = 0
            self.camera_y = 0
            # Mark transition as done
            self.level_6_transition_done = True
        
        # Update boss victory story
        if self.boss_victory_story_active:
            self.boss_story_scroll_offset += self.boss_story_scroll_speed
            
            # Reset scroll when it goes too far
            if self.boss_story_scroll_offset > 600:
                self.boss_story_scroll_offset = 0.0
                
            # Remove automatic timer ending - story only ends on button press
        
        # Update Boss 2 victory story
        if self.boss2_victory_story_active:
            self.boss2_story_scroll_offset += self.boss2_story_scroll_speed
            
            # Reset scroll when it goes too far
            if self.boss2_story_scroll_offset > 600:
                self.boss2_story_scroll_offset = 0.0
                
            # Remove automatic timer ending - story only ends on button press

    def draw(self):
        s = self.screen
        # Clear entire screen first
        s.fill((0, 0, 0))  # Start with black screen
        
        # Calculate status bar height
        status_height = 60  # Default minimum height
        
        # Fill game area only (not status bar area)
        game_area_rect = pygame.Rect(0, 0, self.viewport_width * self.tile, self.screen.get_height() - status_height)
        s.fill((30, 30, 30), game_area_rect)
        
        # Calculate visible range based on camera position
        start_x = self.camera_x // self.tile
        start_y = self.camera_y // self.tile
        end_x = min(self.width, start_x + self.viewport_width + 1)
        end_y = min(self.height, start_y + self.viewport_height + 1)
        
        # draw grid with terrain (only visible tiles)
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                screen_x = x * self.tile - self.camera_x
                screen_y = y * self.tile - self.camera_y
                rect = pygame.Rect(screen_x, screen_y, self.tile, self.tile)
                
                # Check if we have terrain data for this position
                if (hasattr(self.state, 'terrain') and self.state.terrain and 
                    y < len(self.state.terrain) and x < len(self.state.terrain[y])):
                    terrain_type = self.state.terrain[y][x]
                    
                    # Use terrain images if available, otherwise fallback to colors
                    if terrain_type == 'dirt':
                        if self.dirt_image:
                            s.blit(self.dirt_image, (screen_x, screen_y))
                        else:
                            # Fallback to solid brown
                            color = (101, 67, 33) if (x + y) % 2 == 0 else (92, 51, 23)
                            pygame.draw.rect(s, color, rect)
                    elif terrain_type == 'castle':
                        if self.castle_image:
                            s.blit(self.castle_image, (screen_x, screen_y))
                        else:
                            # Fallback to solid gray
                            color = (128, 128, 128) if (x + y) % 2 == 0 else (105, 105, 105)
                            pygame.draw.rect(s, color, rect)
                    elif terrain_type == 'road':
                        # Use road image
                        if self.road_image:
                            s.blit(self.road_image, (screen_x, screen_y))
                        else:
                            # Fallback to darker brown for road
                            color = (80, 50, 20) if (x + y) % 2 == 0 else (70, 40, 15)
                            pygame.draw.rect(s, color, rect)
                    elif terrain_type == 'destroyed_house':
                        # Use destroyed house image
                        if self.destroyed_house_image:
                            s.blit(self.destroyed_house_image, (screen_x, screen_y))
                        else:
                            # Fallback to dark red/brown for destroyed house
                            color = (139, 69, 19) if (x + y) % 2 == 0 else (101, 50, 14)
                            pygame.draw.rect(s, color, rect)
                    else:  # grass
                        if self.grass_image:
                            s.blit(self.grass_image, (screen_x, screen_y))
                        else:
                            # Fallback to solid gray-green
                            color = (70, 70, 70) if (x + y) % 2 == 0 else (60, 60, 60)
                            pygame.draw.rect(s, color, rect)
                else:
                    # Default terrain if no terrain data
                    if self.grass_image:
                        s.blit(self.grass_image, (screen_x, screen_y))
                    else:
                        color = (70, 70, 70) if (x + y) % 2 == 0 else (60, 60, 60)
                        pygame.draw.rect(s, color, rect)
                
                # Draw grid lines around each tile for better visibility
                pygame.draw.rect(s, (30, 30, 30), rect, 1)  # Dark gray grid lines
        # highlights (only visible ones)
        for (x, y) in self.state.highlight_tiles:
            if start_x <= x < end_x and start_y <= y < end_y:
                screen_x = x * self.tile - self.camera_x
                screen_y = y * self.tile - self.camera_y
                rect = pygame.Rect(screen_x, screen_y, self.tile, self.tile)
                # Create a semi-transparent green highlight overlay instead of solid color
                highlight_surface = pygame.Surface((self.tile, self.tile), pygame.SRCALPHA)
                highlight_surface.fill((50, 200, 50, 100))  # Semi-transparent green
                s.blit(highlight_surface, (screen_x, screen_y))
                # Draw a brighter green border
                pygame.draw.rect(s, (100, 255, 100), rect, 3)
        # attack targets (red tint)
        if getattr(self.state, 'attack_targets', None):
            for t in self.state.attack_targets:
                if start_x <= t.x < end_x and start_y <= t.y < end_y:
                    screen_x = t.x * self.tile - self.camera_x
                    screen_y = t.y * self.tile - self.camera_y
                    at_rect = pygame.Rect(screen_x, screen_y, self.tile, self.tile)
                    tint = pygame.Surface((self.tile, self.tile), pygame.SRCALPHA)
                    tint.fill((200, 50, 50, 80))
                    s.blit(tint, (screen_x, screen_y))
                    pygame.draw.rect(s, (220, 80, 80), at_rect, 3)
        # units (only visible ones)
        for u in self.state.units:
            if u.hp <= 0:
                continue
            if start_x <= u.x < end_x and start_y <= u.y < end_y:
                screen_x = u.x * self.tile - self.camera_x
                screen_y = u.y * self.tile - self.camera_y
                rx = screen_x + 8
                ry = screen_y + 8
                w = self.tile - 16
                h = self.tile - 16
                
                # Draw unit (no special border for leveled units)
                pygame.draw.rect(s, u.color, pygame.Rect(rx, ry, w, h), border_radius=6)
                hp_text = self.font.render(str(u.hp), True, (255, 255, 255))
                s.blit(hp_text, (screen_x + 4, screen_y + 4))
                
                # Draw level indicator for player units (gold color)
                if hasattr(u, 'level') and u.team == 'player' and u.level > 1:
                    level_font = pygame.font.SysFont(None, 16)
                    level_text = level_font.render(str(u.level), True, (255, 215, 0))
                    s.blit(level_text, (screen_x + self.tile - 12, screen_y + 4))
                
                # Draw level indicator for enemy units (red color) - only show level 2+
                if hasattr(u, 'level') and u.team == 'enemy' and u.level > 1:
                    level_font = pygame.font.SysFont(None, 16)
                    level_text = level_font.render(str(u.level), True, (255, 100, 100))
                    s.blit(level_text, (screen_x + self.tile - 12, screen_y + 4))
        # selection cursor (only if visible) - always draw if unit is selected
        if self.state.selected:
            sel = self.state.selected
            # Always draw selection cursor, regardless of camera position
            screen_x = sel.x * self.tile - self.camera_x
            screen_y = sel.y * self.tile - self.camera_y
            # Only draw if within viewport bounds
            if 0 <= screen_x < self.viewport_width * self.tile and 0 <= screen_y < self.viewport_height * self.tile:
                rect = pygame.Rect(screen_x, screen_y, self.tile, self.tile)
                pygame.draw.rect(s, (200, 200, 0), rect, 3)
        # status bar: show active unit and actions
        if not self.state.game_over:
            if self.state.current_phase == 'player':
                # Show player unit info if one is selected
                if self.state.selected:
                    u = self.state.selected
                    if hasattr(u, 'level') and u.team == 'player':
                        status = f"""
                        {self.get_level_name()} | PLAYER PHASE | Selected: {u.__class__.__name__} Lv.{u.level} @{u.x},{u.y}  
                        HP: {u.hp}/{u.max_hp}  Moves: {u.moves_remaining}/{u.move}  Attacks: {u.attacks_remaining}/1  
                        EXP: {u.exp}/{u.exp_to_next_level}  Kills: {u.kills}  ATK: {u.atk}
                        -  Press SPACE to end player phase
                        """
                        if self.enable_scrolling:
                            status += "-  Use Arrow Keys or WASD to scroll battlefield\n"
                    else:
                        status = f"""
                        {self.get_level_name()} | PLAYER PHASE | Selected: {u.__class__.__name__} @{u.x},{u.y}  
                        Moves: {u.moves_remaining}/{u.move}  Attacks: {u.attacks_remaining}/1  
                        -  Press SPACE to end player phase
                        """
                        if self.enable_scrolling:
                            status += "-  Use Arrow Keys or WASD to scroll battlefield\n"
                else:
                    status = f"""
                    {self.get_level_name()} | PLAYER PHASE | Click a unit to select
                    -  Press SPACE to end player phase
                    """
                    if self.enable_scrolling:
                        status += "\n-  Use Arrow Keys or WASD to scroll battlefield"
            else:
                status = f"{self.get_level_name()} | ENEMY PHASE | Enemy turn in progress..."
        elif self.state.game_over:
            if self.state.victory:
                status = f"{self.get_level_name()} VICTORY! Advancing to next level..."
            else:
                status = "TRISTAN DEFEATED! Press any key to return to main menu."
        else:
            status = "No active unit"
        
        # phase announcements overlay - only cover game area, not status bar
        if hasattr(self.state, 'phase_announcement_timer') and self.state.phase_announcement_timer > 0:
            if self.state.current_phase == 'enemy':
                # Show "ENEMY PHASE" announcement
                overlay = pygame.Surface((self.viewport_width * self.tile, self.viewport_height * self.tile), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))
                s.blit(overlay, (0, 0))
                
                big_font = pygame.font.SysFont(None, 96)
                phase_text = big_font.render("ENEMY PHASE", True, (200, 50, 50))
                text_rect = phase_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2))
                s.blit(phase_text, text_rect)
            elif self.state.current_phase == 'player':
                # Show "PLAYER PHASE" announcement
                overlay = pygame.Surface((self.viewport_width * self.tile, self.viewport_height * self.tile), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))
                s.blit(overlay, (0, 0))
                
                big_font = pygame.font.SysFont(None, 96)
                phase_text = big_font.render("PLAYER PHASE", True, (50, 150, 255))
                text_rect = phase_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2))
                s.blit(phase_text, text_rect)
        
        # level up announcements - collect all units that leveled up
        leveled_up_units = [u for u in self.state.units if hasattr(u, 'level_up_announcement') and u.level_up_announcement]
        
        if leveled_up_units:
            # Create level up overlay
            overlay = pygame.Surface((self.viewport_width * self.tile, self.viewport_height * self.tile), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            s.blit(overlay, (0, 0))
            
            # Big "LEVEL UP!" text
            huge_font = pygame.font.SysFont(None, 120)
            level_up_text = huge_font.render("LEVEL UP!", True, (255, 215, 0))
            text_rect = level_up_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 - 60))
            s.blit(level_up_text, text_rect)
            
            # Show all units that leveled up
            big_font = pygame.font.SysFont(None, 36)
            med_font = pygame.font.SysFont(None, 28)
            y_offset = self.viewport_height * self.tile // 2 - 20
            
            for i, unit in enumerate(leveled_up_units):
                # Unit name and new level
                unit_text = big_font.render(f"{unit.__class__.__name__} is now Level {unit.level}!", True, (255, 255, 255))
                unit_rect = unit_text.get_rect(center=(self.viewport_width * self.tile // 2, y_offset))
                s.blit(unit_text, unit_rect)
                y_offset += 40
                
                # Stats gained
                hp_gain = int(unit.base_hp * 0.1)
                atk_gain = int(unit.base_atk * 0.15)
                stats_text = med_font.render(f"HP +{hp_gain}  ATK +{atk_gain}", True, (100, 255, 100))
                stats_rect = stats_text.get_rect(center=(self.viewport_width * self.tile // 2, y_offset))
                s.blit(stats_text, stats_rect)
                y_offset += 30
                
                # Movement bonus (every 3 levels)
                if unit.level % 3 == 0:
                    move_text = med_font.render("MOVE +1", True, (100, 200, 255))
                    move_rect = move_text.get_rect(center=(self.viewport_width * self.tile // 2, y_offset))
                    s.blit(move_text, move_rect)
                    y_offset += 30
                
                # Add spacing between multiple units
                if i < len(leveled_up_units) - 1:
                    y_offset += 20
        
        # Boss victory story overlay
        if self.boss_victory_story_active:
            # Create story overlay
            story_overlay = pygame.Surface((self.viewport_width * self.tile - 80, self.viewport_height * self.tile - 160), pygame.SRCALPHA)
            story_overlay.fill((0, 0, 0, 200))
            story_rect = story_overlay.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2))
            self.screen.blit(story_overlay, story_rect)
            
            # Create clipping region for text
            clip_rect = pygame.Rect(story_rect.left + 40, story_rect.top + 40, 
                                   story_rect.width - 80, story_rect.height - 80)
            self.screen.set_clip(clip_rect)
            
            # Boss victory story content
            story_text = [
                "VICTORY!",
                "",
                "By the time Tristan and his party made it to Soron,",
                "it was already under attack by Gredson's Army!",
                "They found a few surviving knights who were willing",
                "to join Tristan's party.",
                "",
                "One of the knights heard of a great sage in Tyick.",
                "This was just a taste of Gredson's power.",
                "If Tristan wants to defeat Gredson's Army,",
                "he'll need as much help as he can get.",
                "",
                "So Tristan and his party set out to Tyick",
                "in search of the Great Sage.",
                "",
                "Press any key to continue..."
            ]
            
            # Render the story text with scrolling
            lines = story_text
            y_offset = clip_rect.top - self.boss_story_scroll_offset
            max_width = clip_rect.width
            
            for line in lines:
                if line == "VICTORY!":
                    text = pygame.font.SysFont(None, 48).render(line, True, (255, 215, 0))
                elif line == "Press any key to continue...":
                    text = pygame.font.SysFont(None, 24).render(line, True, (255, 255, 200))
                else:
                    text = pygame.font.SysFont(None, 28).render(line, True, (255, 255, 200))
                
                text_rect = text.get_rect(center=(self.viewport_width * self.tile // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 35 if line == "" else 40
            
            # Reset clipping
            self.screen.set_clip(None)
        
        # Boss 2 victory story overlay
        if self.boss2_victory_story_active:
            # Create story overlay
            story_overlay = pygame.Surface((self.viewport_width * self.tile - 80, self.viewport_height * self.tile - 160), pygame.SRCALPHA)
            story_overlay.fill((0, 0, 0, 200))
            story_rect = story_overlay.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2))
            self.screen.blit(story_overlay, story_rect)
            
            # Create clipping region for text
            clip_rect = pygame.Rect(story_rect.left + 40, story_rect.top + 40, 
                                   story_rect.width - 80, story_rect.height - 80)
            self.screen.set_clip(clip_rect)
            
            # Boss 2 victory story content
            story_text = [
                "VICTORY!",
                "",
                "Tristan and his party made it to Tyick.",
                "But on their way to the Great Sage they fought a Mage using a strange dark Magic keeping them away from the Great Sage",
                "Tristan and his party defeated him and made it to the Great Sage.",
                "The Great Sage said that the magic that he was using was dark dragon Magic!",
                "Then he also told them of a stone in each kingdom.",
                "Each one of the stones has a great amount of power and told them that is why Gredson is attacking the kingdoms.",
                "The Great Sage sends them to Reevin to find  the stone of  Reevin.",
                "And Send them off with some new troops. ",
                "So Tristan and his party head back to his homeland of Reevin.",
                "",
                "Press any key to continue..."
            ]
            
            # Render the story text with scrolling
            lines = story_text
            y_offset = clip_rect.top - self.boss2_story_scroll_offset
            max_width = clip_rect.width
            
            for line in lines:
                if line == "VICTORY!":
                    text = pygame.font.SysFont(None, 48).render(line, True, (255, 215, 0))
                elif line == "Press any key to continue...":
                    text = pygame.font.SysFont(None, 24).render(line, True, (255, 255, 200))
                else:
                    text = pygame.font.SysFont(None, 28).render(line, True, (255, 255, 200))
                
                text_rect = text.get_rect(center=(self.viewport_width * self.tile // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 35 if line == "" else 40
            
            # Reset clipping
            self.screen.set_clip(None)
        
        # Always ensure status bar is drawn last, after any clipping operations
        # This prevents any overlays or clipping from affecting it
        
        # victory/defeat overlay (only show if not in boss story) - don't cover status bar
        if self.state.game_over and not self.boss_victory_story_active and not self.boss2_victory_story_active:
            overlay = pygame.Surface((self.viewport_width * self.tile, self.viewport_height * self.tile), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            s.blit(overlay, (0, 0))
            
            # big victory/defeat text
            if self.state.victory:
                big_font = pygame.font.SysFont(None, 72)
                victory_text = big_font.render(f"{self.get_level_name()} VICTORY!", True, (255, 215, 0))
                text_rect = victory_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 - 20))
                s.blit(victory_text, text_rect)
                
                sub_font = pygame.font.SysFont(None, 36)
                sub_text = sub_font.render("Advancing to next level...", True, (255, 255, 255))
                sub_rect = sub_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 + 30))
                s.blit(sub_text, sub_rect)
            else:
                # Check if Tristan was defeated for overlay text
                tristan_defeated = False
                for unit in self.state.units:
                    if unit.__class__.__name__ == 'Tristan' and unit.hp <= 0:
                        tristan_defeated = True
                        # Set game over state when Tristan is defeated
                        self.state.game_over = True
                        self.state.victory = False
                        break
                
                if tristan_defeated:
                    # Draw defeat screen and stop other drawing
                    big_font = pygame.font.SysFont(None, 96)
                    sub_font = pygame.font.SysFont(None, 48)
                    defeat_text = big_font.render("GAME OVER", True, (200, 50, 50))
                    tristan_text = sub_font.render("Tristan is defeated!", True, (255, 100, 100))
                    text_rect = defeat_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 - 40))
                    tristan_rect = tristan_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 + 20))
                    s.blit(defeat_text, text_rect)
                    s.blit(tristan_text, tristan_rect)
                    # Don't draw anything else when defeated
                    return
                else:
                    # Generic defeat for other scenarios
                    big_font = pygame.font.SysFont(None, 72)
                    defeat_text = big_font.render("DEFEAT!", True, (200, 50, 50))
                    sub_font = pygame.font.SysFont(None, 36)
                    sub_text = sub_font.render("All units lost...", True, (255, 255, 255))
                    text_rect = defeat_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 - 20))
                    sub_rect = sub_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 + 30))
                    s.blit(defeat_text, text_rect)
                    s.blit(sub_text, sub_rect)
                    # Don't draw anything else when defeated
                    return
        
        # Always draw status bar last to keep it on top of overlays
        if not self.state.game_over:
            if self.state.current_phase == 'player':
                # Show player unit info if one is selected
                if self.state.selected:
                    u = self.state.selected
                    if hasattr(u, 'level') and u.team == 'player':
                        status = f"{self.get_level_name()} | PLAYER PHASE | Selected: {u.__class__.__name__} Lv.{u.level} @{u.x},{u.y}\nHP: {u.hp}/{u.max_hp}  Moves: {u.moves_remaining}/{u.move}  Attacks: {u.attacks_remaining}/1\nEXP: {u.exp}/{u.exp_to_next_level}  Kills: {u.kills}  ATK: {u.atk}\nPress SPACE to end player phase"
                        if self.enable_scrolling:
                            status += "\nUse Arrow Keys or WASD to scroll battlefield"
                    else:
                        status = f"{self.get_level_name()} | PLAYER PHASE | Selected: {u.__class__.__name__} @{u.x},{u.y}\nMoves: {u.moves_remaining}/{u.move}  Attacks: {u.attacks_remaining}/1\nPress SPACE to end player phase"
                        if self.enable_scrolling:
                            status += "\nUse Arrow Keys or WASD to scroll battlefield"
                else:
                    status = f"{self.get_level_name()} | PLAYER PHASE | Click a unit to select\nPress SPACE to end player phase"
                    if self.enable_scrolling:
                        status += "\nUse Arrow Keys or WASD to scroll battlefield"
            else:
                status = f"{self.get_level_name()} | ENEMY PHASE | Enemy turn in progress..."
        elif self.state.game_over:
            if self.state.victory:
                status = f"{self.get_level_name()} VICTORY! Advancing to next level..."
            else:
                # Check if Tristan was defeated
                tristan_defeated = False
                for unit in self.state.units:
                    if unit.__class__.__name__ == 'Tristan' and unit.hp <= 0:
                        tristan_defeated = True
                        break
                
                if tristan_defeated:
                    status = "DEFEAT! Tristan is defeated!"
                else:
                    status = "DEFEAT! Tristan is defeated!"
        else:
            status = "No active unit"
        
        lines = status.strip().split('\n')
        # Calculate needed height for all lines
        status_height = max(60, len(lines) * 20 + 10)  # Minimum 60px, expand based on content
        
        # Position status bar to touch bottom of screen
        screen_height = self.screen.get_height()
        status_bar_rect = pygame.Rect(0, screen_height - status_height, self.viewport_width * self.tile, status_height)
        
        # Clear and fill status bar area with solid black
        s.fill((0, 0, 0), status_bar_rect)  # Solid black
        
        # Draw a border around status bar
        pygame.draw.rect(s, (100, 100, 100), status_bar_rect, 1)  # Gray border
        
        # Draw all lines of status text
        for i, line in enumerate(lines):
            txt = self.font.render(line.strip(), True, (220, 220, 220))
            s.blit(txt, (8, screen_height - status_height + 8 + i * 20))
