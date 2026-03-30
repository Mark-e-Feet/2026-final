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
        self.scroll_speed = 600  # Pixels per second (7.5 tiles per second with 80px tiles)
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
        
        # Load character images
        self.character_images = {}
        try:
            # Load level artwork
            self.level_artwork = {}
            try:
                # Load level-specific artwork images (using placeholder names for now)
                self.level_artwork['Level 9'] = pygame.image.load("assets/arrow.mp3")  # Using arrow as placeholder
                self.level_artwork['Level 10'] = pygame.image.load("assets/fire_magic.mp3")  # Using fire_magic as placeholder  
                self.level_artwork['Level 11'] = pygame.image.load("assets/finle_boss.mp3")  # Using finle_boss as placeholder
                print("Level artwork loaded")
            except FileNotFoundError:
                print("Level artwork files not found - using default")
            except Exception as e:
                print(f"Could not load level artwork: {e}")
            
            # Load player character images
            self.character_images['Tristan_P'] = pygame.image.load("assets/tristan P.png")
            self.character_images['Archer_P'] = pygame.image.load("assets/archer P.png")  # Using new archer P image
            self.character_images['Mage_P'] = pygame.image.load("assets/mage P.png")
            self.character_images['Horse_P'] = pygame.image.load("assets/horse P.png")
            self.character_images['Srodman_P'] = pygame.image.load("assets/sorodman P.png")
            self.character_images['Knight_P'] = pygame.image.load("assets/knigt P.png")
            self.character_images['King_P'] = pygame.image.load("assets/king P.png")  
            self.character_images['Knig_P'] = pygame.image.load("assets/king P.png")  # Knig class uses king P image
            self.character_images['Soldier_P'] = pygame.image.load("assets/soldier P.png")  # Using soldier P image
            self.character_images['Healer_P'] = pygame.image.load("assets/healer P.png")  # Using new healer P image
            self.character_images['Horsearcher_P'] = pygame.image.load("assets/horsearcher P.png")  # Using new horsearcher P image
            self.character_images['Ballistician_P'] = pygame.image.load("assets/ballistician P.png")  # Using new ballistician P image
            
            # Load enemy character images
            self.character_images['Bandit_E'] = pygame.image.load("assets/bandit E.png")
            self.character_images['Archer_E'] = pygame.image.load("assets/archer E.png")
            self.character_images['Knight_E'] = pygame.image.load("assets/knigt E.png")
            self.character_images['Mage_E'] = pygame.image.load("assets/mage E.png")
            self.character_images['Horse_E'] = pygame.image.load("assets/horse E.png")
            self.character_images['Srodman_E'] = pygame.image.load("assets/srodman E.png")
            self.character_images['Soldier_E'] = pygame.image.load("assets/soldier E.png")
            self.character_images['Boss1_E'] = pygame.image.load("assets/boss 1 E.png")  # Using new boss 1 E image
            self.character_images['Boss2_E'] = pygame.image.load("assets/boss 2 E.png")  # Using new boss 2 E image
            self.character_images['Boss3_E'] = pygame.image.load("assets/boss 3 E.png")  # Using new boss 3 E image
            self.character_images['Healer_E'] = pygame.image.load("assets/healer E.png")  # Using new healer E image
            self.character_images['Horsearcher_E'] = pygame.image.load("assets/horsearcher E.png")  # Using new horsearcher E image
            self.character_images['Ballistician_E'] = pygame.image.load("assets/ballistician E.png")  # Using new ballistician E image
            self.character_images['Darkmage_E'] = pygame.image.load("assets/darkmage E.png")
            
            # Scale all character images to be much larger (120x120 instead of 80x80)
            for key in self.character_images:
                self.character_images[key] = pygame.transform.scale(self.character_images[key], (120, 120))
                
        except pygame.error as e:
            print(f"Could not load character images: {e}")
            self.character_images = {}
        
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
        
        # Level 17 victory story system
        self.level17_victory_story_active = False
        self.level17_victory_story_timer = 0.0
        self.level17_victory_story_duration = 8.0  # Show for 8 seconds
        self.level17_story_scroll_offset = 0.0
        self.level17_story_scroll_speed = 0.1
        
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
            
            # Update Game class (handles scrolling)
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
                # Skip Level 17 story with any key
                if self.level17_victory_story_active:
                    self.level17_victory_story_active = False
                    self.state.next_level()
                # Return to main menu when defeated
                if self.state.game_over and not self.state.victory:
                    self.running = False
                # Handle scrolling when enabled - track key press
                if self.state.enable_scrolling and hasattr(self.state, 'enable_scrolling') and ev.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d, pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s]:
                    self.keys_pressed.add(ev.key)
            elif ev.type == pygame.KEYUP:
                # Remove key from pressed set when released
                if ev.key in self.keys_pressed:
                    self.keys_pressed.remove(ev.key)

    def update(self, dt):
        self.state.update(dt)
        
        # Sync scrolling flag and dimensions with GameState
        self.enable_scrolling = self.state.enable_scrolling
        self.width = self.state.width
        self.height = self.state.height
        
        # Handle continuous scrolling when keys are held down
        if (hasattr(self.state, 'enable_scrolling') and self.state.enable_scrolling and 
            hasattr(self, 'width') and hasattr(self, 'height') and 
            hasattr(self, 'viewport_width') and hasattr(self, 'viewport_height') and 
            self.keys_pressed):
            try:
                # Calculate max scroll boundaries using synced dimensions
                max_x = max(0, (self.width - self.viewport_width) * self.tile)
                max_y = max(0, (self.height - self.viewport_height) * self.tile)
                
                # Handle horizontal scrolling - smooth gradual movement
                if pygame.K_LEFT in self.keys_pressed or pygame.K_a in self.keys_pressed:
                    self.camera_x = max(0, self.camera_x - self.scroll_speed * dt)
                if pygame.K_RIGHT in self.keys_pressed or pygame.K_d in self.keys_pressed:
                    self.camera_x = min(max_x, self.camera_x + self.scroll_speed * dt)
                
                # Handle vertical scrolling - smooth gradual movement
                if pygame.K_UP in self.keys_pressed or pygame.K_w in self.keys_pressed:
                    self.camera_y = max(0, self.camera_y - self.scroll_speed * dt)
                if pygame.K_DOWN in self.keys_pressed or pygame.K_s in self.keys_pressed:
                    self.camera_y = min(max_y, self.camera_y + self.scroll_speed * dt)
            except Exception as e:
                # If scrolling fails, disable it to prevent crashes
                print(f"Scrolling error: {e}")
                self.state.enable_scrolling = False
                self.enable_scrolling = False
                # Clear pressed keys to prevent continuous error processing
                self.keys_pressed.clear()
        
        # Camera tracking for active enemy during enemy phase
        if self.state.enable_scrolling and hasattr(self.state, 'active_enemy') and self.state.active_enemy:
            try:
                # Calculate desired camera position to center on active enemy
                target_x = self.state.active_enemy.x * self.tile - (self.viewport_width * self.tile) // 2
                target_y = self.state.active_enemy.y * self.tile - (self.viewport_height * self.tile) // 2
                
                # Calculate max scroll boundaries
                max_x = max(0, (self.width - self.viewport_width) * self.tile)
                max_y = max(0, (self.height - self.viewport_height) * self.tile)
                
                # Clamp target to boundaries
                target_x = max(0, min(target_x, max_x))
                target_y = max(0, min(target_y, max_y))
                
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
            except Exception as e:
                print(f"Camera tracking error: {e}")
                # Disable camera tracking if it fails
                pass
            
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
        
        # Check for Level 17 victory and start story
        if self.state.game_over and self.state.victory and self.state.current_level == 17 and not self.level17_victory_story_active:
            self.level17_victory_story_active = True
            self.level17_victory_story_timer = self.level17_victory_story_duration
            self.level17_story_scroll_offset = 0.0
        
        # Play boss music during boss battles
        if hasattr(self, 'boss_music') and self.boss_music:
            if (self.state.current_level == 5 or self.state.current_level == 11 or self.state.current_level == 17) and not self.state.game_over:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    self.boss_music.play(-1)  # Loop boss music
                    print("Playing boss battle music")
            else:
                if self.state.game_over and self.state.victory:
                    # Stop boss music after boss victory
                    if hasattr(self, 'boss_music') and self.boss_music:
                        self.boss_music.stop()
                        print("Boss music stopped after victory")
                if hasattr(self, 'boss_music') and self.boss_music.get_num_channels() > 0:
                    self.boss_music.stop()
        
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
        
        # Check for Level 18 transition to Part 4 battlefield (only once)
        if self.state.current_level == 18 and not hasattr(self, 'level_18_transition_done'):
            # Transition to Part 4 - 30x8 battlefield
            self.width = 30
            self.height = 8
            self.viewport_width = 12  # Keep viewport same size
            self.viewport_height = 8  # Keep viewport same size
            self.enable_scrolling = True  # Enable scrolling for Part 4 battlefield
            # Update state dimensions
            self.state.width = 30
            self.state.height = 8
            self.state.enable_scrolling = True
            # Reset camera position
            self.camera_x = 0
            self.camera_y = 0
            
            # Add three new player units for Part 4
            from classes.Soldier import Soldier
            from classes.Knig import Knig
            
            # Find available positions for new units
            new_unit_positions = [(1, 1), (2, 1), (3, 1)]  # Starting positions
            new_unit_classes = [Soldier, Soldier, Knig]
            
            for i, (pos_x, pos_y) in enumerate(new_unit_positions):
                unit_class = new_unit_classes[i]
                # Check if position is empty
                position_occupied = False
                for unit in self.state.units:
                    if unit.x == pos_x and unit.y == pos_y and unit.team == 'player':
                        position_occupied = True
                        break
                
                if not position_occupied:
                    # Add new unit with appropriate level for Part 4
                    new_unit = unit_class(pos_x, pos_y, 'player')
                    new_unit.set_level(3)  # Set level to match Part 3 difficulty
                    self.state.units.append(new_unit)
                    print(f"Added new {unit_class.__name__} at position ({pos_x}, {pos_y})")
            
            # Mark transition as done
            self.level_18_transition_done = True
            print("Transitioned to Part 4 - 30x8 battlefield with new units")
        
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

        # Update Level 17 victory story
        if self.level17_victory_story_active:
            self.level17_story_scroll_offset += self.level17_story_scroll_speed
            
            # Reset scroll when it goes too far
            if self.level17_story_scroll_offset > 600:
                self.level17_story_scroll_offset = 0.0
                
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
        start_x = int(self.camera_x // self.tile)
        start_y = int(self.camera_y // self.tile)
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
                
                # Draw unit using character image or fallback to colored rectangle
                team_suffix = "P" if u.team == "player" else "E"
                unit_key = f"{u.__class__.__name__}_{team_suffix}"
                if unit_key in self.character_images:
                    # Draw character image centered with black outline (120px image on 80px tile, so -20px offset)
                    img_x = screen_x - 20
                    img_y = screen_y - 20
                    
                    # Create a black silhouette for outline
                    black_img = self.character_images[unit_key].copy()
                    black_img.fill((0, 0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                    
                    # Draw black outline by drawing the black silhouette at 4 offset positions
                    s.blit(black_img, (img_x - 2, img_y))  # Left
                    s.blit(black_img, (img_x + 2, img_y))  # Right
                    s.blit(black_img, (img_x, img_y - 2))  # Top
                    s.blit(black_img, (img_x, img_y + 2))  # Bottom
                    
                    # Draw the main character image on top
                    s.blit(self.character_images[unit_key], (img_x, img_y))
                else:
                    # Fallback to colored rectangle if no image available
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
        
        # Victory overlay for regular battles (non-boss levels)
        if self.state.game_over and self.state.victory and self.state.current_level not in [5, 11, 17]:
            # Create victory overlay
            overlay = pygame.Surface((self.viewport_width * self.tile, self.viewport_height * self.tile), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            s.blit(overlay, (0, 0))
            
            # Big "VICTORY! Battle Won!" text
            huge_font = pygame.font.SysFont(None, 120)
            victory_text = huge_font.render("VICTORY!", True, (255, 215, 0))
            victory_rect = victory_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 - 60))
            s.blit(victory_text, victory_rect)
            
            # "Battle Won!" text
            big_font = pygame.font.SysFont(None, 72)
            battle_text = big_font.render("Battle Won!", True, (100, 255, 100))
            battle_rect = battle_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2))
            s.blit(battle_text, battle_rect)
            
            # Level completed text
            medium_font = pygame.font.SysFont(None, 48)
            level_text = medium_font.render(f"Level {self.state.current_level} Complete!", True, (200, 200, 255))
            level_rect = level_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 + 60))
            s.blit(level_text, level_rect)
        
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
                "But on their way to the Great Sage they fought a Mage using",
                "a strange dark Magic keeping them away from the Great Sage.",
                "Tristan and his party defeated him and made it to the Great Sage.",
                "The Great Sage said that the magic that he was using was dark dragon Magic!",
                "Then he also told them of a stone in each kingdom.",
                "Each one of the stones has a great amount of power and",
                "told them that is why Gredson is attacking the kingdoms.",
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
        
        # Level 17 victory story overlay
        if self.level17_victory_story_active:
            # Create story overlay
            story_overlay = pygame.Surface((self.viewport_width * self.tile - 80, self.viewport_height * self.tile - 160), pygame.SRCALPHA)
            story_overlay.fill((0, 0, 0, 200))
            story_rect = story_overlay.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2))
            self.screen.blit(story_overlay, story_rect)
            
            # Create clipping region for text
            clip_rect = pygame.Rect(story_rect.left + 40, story_rect.top + 40, 
                                   story_rect.width - 80, story_rect.height - 80)
            self.screen.set_clip(clip_rect)
            
            # Level 17 victory story content
            story_text = [
                "VICTORY!",
                "",
                "With the defeat of the final enemy forces, Tristan and his allies stand victorious.",
                "The long and difficult campaign has come to an end.",
                "",
                "Their courage and strength have saved the kingdoms from destruction.",
                "Gredson's Army has been vanquished, and peace can finally return to the land.",
                "",
                "The people of Tharen celebrate their heroes.",
                "Songs will be sung of their bravery for generations to come.",
                "",
                "Tristan looks toward the future, ready to rebuild and restore",
                "the kingdoms to their former glory.",
                "",
                "Press any key to continue..."
            ]
            
            # Render the story text with scrolling
            lines = story_text
            y_offset = clip_rect.top - self.level17_story_scroll_offset
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
        pygame.draw.rect(self.screen, (0, 0, 0), status_bar_rect)
        
        # Draw status text lines
        y_offset = status_bar_rect.top + 5
        for line in lines:
            text = self.font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(centerx=status_bar_rect.centerx, y=y_offset)
            self.screen.blit(text, text_rect)
            y_offset += 20

    
