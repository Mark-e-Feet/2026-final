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
        self.scroll_speed = 4  # Pixels per frame when holding key
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
        
        # Update state dimensions if different from default
        self.state.width = width
        self.state.height = height
        
        # Boss victory story system
        self.boss_victory_story_active = False
        self.boss_victory_story_timer = 0.0
        self.boss_victory_story_duration = 8.0  # Show for 8 seconds
        self.boss_story_scroll_offset = 0.0
        self.boss_story_scroll_speed = 0.1

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
                # Handle scrolling when enabled - track key press
                elif self.enable_scrolling:
                    if ev.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d, pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s]:
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
        
        # Check for boss victory and start story
        if self.state.game_over and self.state.victory and self.state.current_level == 5 and not self.boss_victory_story_active:
            self.boss_victory_story_active = True
            self.boss_victory_story_timer = self.boss_victory_story_duration
            self.boss_story_scroll_offset = 0.0
        
        # Update boss victory story
        if self.boss_victory_story_active:
            self.boss_victory_story_timer -= dt
            self.boss_story_scroll_offset += self.boss_story_scroll_speed
            
            # Reset scroll when it goes too far
            if self.boss_story_scroll_offset > 600:
                self.boss_story_scroll_offset = 0.0
                
            # End story after duration
            if self.boss_victory_story_timer <= 0:
                self.boss_victory_story_active = False
                # Continue with normal level progression
                self.state.next_level()

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
        
        # draw grid (only visible tiles)
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                screen_x = x * self.tile - self.camera_x
                screen_y = y * self.tile - self.camera_y
                rect = pygame.Rect(screen_x, screen_y, self.tile, self.tile)
                color = (70, 70, 70) if (x + y) % 2 == 0 else (60, 60, 60)
                pygame.draw.rect(s, color, rect)
                pygame.draw.rect(s, (40, 40, 40), rect, 1)
        # highlights (only visible ones)
        for (x, y) in self.state.highlight_tiles:
            if start_x <= x < end_x and start_y <= y < end_y:
                screen_x = x * self.tile - self.camera_x
                screen_y = y * self.tile - self.camera_y
                rect = pygame.Rect(screen_x, screen_y, self.tile, self.tile)
                pygame.draw.rect(s, (50, 150, 50), rect, 0)
                pygame.draw.rect(s, (50, 200, 50), rect, 3)
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
                
                # Draw level indicator for player units (keep the level number)
                if hasattr(u, 'level') and u.team == 'player' and u.level > 1:
                    level_font = pygame.font.SysFont(None, 16)
                    level_text = level_font.render(str(u.level), True, (255, 215, 0))
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
                status = "DEFEAT! All units lost."
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
            story_text = (
                "VICTORY!\n\n"
                "By the time Tristan and his party made it to Soron, it was already attacked by Gredson’s Army! "
                "They found a few surviving knights who are willing to join Tristan's party"
                "One of the knights heard of a great sage in Tyick."
                "This was just a taste of Gredson’s power.If Tristan will want to defeat Gredson’s Army he'll need as much help as he can get."
                " So Tristan and his party set out to Tyick  in search of the Great Sage.\n\n"
                "Press any key to continue..."
            )
            
            # Render the story text with scrolling
            lines = story_text.split('\n')
            y_offset = clip_rect.top - self.boss_story_scroll_offset
            max_width = clip_rect.width
            
            for line in lines:
                if line == "VICTORY OVER MALAKOR!":
                    text = pygame.font.SysFont(None, 48).render(line, True, (255, 215, 0))
                elif line == "The heroes have saved Tharen... for now.":
                    text = pygame.font.SysFont(None, 36).render(line, True, (200, 200, 255))
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
        if self.state.game_over and not self.boss_victory_story_active:
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
                big_font = pygame.font.SysFont(None, 72)
                defeat_text = big_font.render("DEFEAT!", True, (200, 50, 50))
                text_rect = defeat_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 - 20))
                s.blit(defeat_text, text_rect)
                
                sub_font = pygame.font.SysFont(None, 36)
                sub_text = sub_font.render("All units lost!", True, (255, 255, 255))
                sub_rect = sub_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 + 30))
                s.blit(sub_text, sub_rect)
        
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
                status = "DEFEAT! All units lost."
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
