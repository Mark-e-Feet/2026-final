import pygame
from game.state import GameState


class Game:
    def __init__(self, width=12, height=8, tile=80, screen=None):
        self.width = width
        self.height = height
        self.tile = tile
        
        # Use provided screen or create new one
        if screen:
            self.screen = screen
        else:
            self.screen = pygame.display.set_mode((width * tile, height * tile + 80))
            pygame.display.set_caption("Heroes of Tharen")
        
        self.clock = pygame.time.Clock()
        self.state = GameState(width, height)
        self.font = pygame.font.SysFont(None, 24)
        self.running = True
        
        # Boss victory story system
        self.boss_victory_story_active = False
        self.boss_victory_story_timer = 0.0
        self.boss_victory_story_duration = 8.0  # Show for 8 seconds
        self.boss_story_scroll_offset = 0.0
        self.boss_story_scroll_speed = 0.3

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
                tx = mx // self.tile
                ty = my // self.tile
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

    def update(self, dt):
        self.state.update(dt)
        
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
        s.fill((30, 30, 30))
        # draw grid
        for x in range(self.width):
            for y in range(self.height):
                rect = pygame.Rect(x * self.tile, y * self.tile, self.tile, self.tile)
                color = (70, 70, 70) if (x + y) % 2 == 0 else (60, 60, 60)
                pygame.draw.rect(s, color, rect)
                pygame.draw.rect(s, (40, 40, 40), rect, 1)
        # highlights
        for (x, y) in self.state.highlight_tiles:
            rect = pygame.Rect(x * self.tile, y * self.tile, self.tile, self.tile)
            pygame.draw.rect(s, (50, 150, 50), rect, 0)
            pygame.draw.rect(s, (50, 200, 50), rect, 3)
        # attack targets (red tint)
        if getattr(self.state, 'attack_targets', None):
            for t in self.state.attack_targets:
                at_rect = pygame.Rect(t.x * self.tile, t.y * self.tile, self.tile, self.tile)
                tint = pygame.Surface((self.tile, self.tile), pygame.SRCALPHA)
                tint.fill((200, 50, 50, 80))
                s.blit(tint, (t.x * self.tile, t.y * self.tile))
                pygame.draw.rect(s, (220, 80, 80), at_rect, 3)
        # units
        for u in self.state.units:
            if u.hp <= 0:
                continue
            rx = u.x * self.tile + 8
            ry = u.y * self.tile + 8
            w = self.tile - 16
            h = self.tile - 16
            
            # Draw unit (no special border for leveled units)
            pygame.draw.rect(s, u.color, pygame.Rect(rx, ry, w, h), border_radius=6)
            hp_text = self.font.render(str(u.hp), True, (255, 255, 255))
            s.blit(hp_text, (u.x * self.tile + 4, u.y * self.tile + 4))
            
            # Draw level indicator for player units (keep the level number)
            if hasattr(u, 'level') and u.team == 'player' and u.level > 1:
                level_font = pygame.font.SysFont(None, 16)
                level_text = level_font.render(str(u.level), True, (255, 215, 0))
                s.blit(level_text, (u.x * self.tile + self.tile - 12, u.y * self.tile + 4))
        # selection cursor
        if self.state.selected:
            sel = self.state.selected
            rect = pygame.Rect(sel.x * self.tile, sel.y * self.tile, self.tile, self.tile)
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
                    else:
                        status = f"""
                        {self.get_level_name()} | PLAYER PHASE | Selected: {u.__class__.__name__} @{u.x},{u.y}  
                        Moves: {u.moves_remaining}/{u.move}  Attacks: {u.attacks_remaining}/1  
                        -  Press SPACE to end player phase
                        """
                else:
                    status = f"""
                    {self.get_level_name()} | PLAYER PHASE | Click a unit to select
                    -  Press SPACE to end player phase
                    """
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
        #txt = self.font.render(status, True, (220, 220, 220))
        s.fill((40, 40, 40), (0, self.height * self.tile, self.width * self.tile, 40))
        for i, line in enumerate(lines):
            txt = self.font.render(line.strip(), True, (220, 220, 220))
            s.blit(txt, (8, self.height * self.tile + 8 + i * 20))
        
        # phase announcements overlay
        if hasattr(self.state, 'phase_announcement_timer') and self.state.phase_announcement_timer > 0:
            if self.state.current_phase == 'enemy':
                # Show "ENEMY PHASE" announcement
                overlay = pygame.Surface((self.width * self.tile, self.height * self.tile), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))
                s.blit(overlay, (0, 0))
                
                big_font = pygame.font.SysFont(None, 96)
                phase_text = big_font.render("ENEMY PHASE", True, (200, 50, 50))
                text_rect = phase_text.get_rect(center=(self.width * self.tile // 2, self.height * self.tile // 2))
                s.blit(phase_text, text_rect)
            elif self.state.current_phase == 'player':
                # Show "PLAYER PHASE" announcement
                overlay = pygame.Surface((self.width * self.tile, self.height * self.tile), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))
                s.blit(overlay, (0, 0))
                
                big_font = pygame.font.SysFont(None, 96)
                phase_text = big_font.render("PLAYER PHASE", True, (50, 150, 255))
                text_rect = phase_text.get_rect(center=(self.width * self.tile // 2, self.height * self.tile // 2))
                s.blit(phase_text, text_rect)
        
        # level up announcements - collect all units that leveled up
        leveled_up_units = [u for u in self.state.units if hasattr(u, 'level_up_announcement') and u.level_up_announcement]
        
        if leveled_up_units:
            # Create level up overlay
            overlay = pygame.Surface((self.width * self.tile, self.height * self.tile), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            s.blit(overlay, (0, 0))
            
            # Big "LEVEL UP!" text
            huge_font = pygame.font.SysFont(None, 120)
            level_up_text = huge_font.render("LEVEL UP!", True, (255, 215, 0))
            text_rect = level_up_text.get_rect(center=(self.width * self.tile // 2, self.height * self.tile // 2 - 60))
            s.blit(level_up_text, text_rect)
            
            # Show all units that leveled up
            big_font = pygame.font.SysFont(None, 36)
            med_font = pygame.font.SysFont(None, 28)
            y_offset = self.height * self.tile // 2 - 20
            
            for i, unit in enumerate(leveled_up_units):
                # Unit name and new level
                unit_text = big_font.render(f"{unit.__class__.__name__} is now Level {unit.level}!", True, (255, 255, 255))
                unit_rect = unit_text.get_rect(center=(self.width * self.tile // 2, y_offset))
                s.blit(unit_text, unit_rect)
                y_offset += 40
                
                # Stats gained
                hp_gain = int(unit.base_hp * 0.1)
                atk_gain = int(unit.base_atk * 0.15)
                stats_text = med_font.render(f"HP +{hp_gain}  ATK +{atk_gain}", True, (100, 255, 100))
                stats_rect = stats_text.get_rect(center=(self.width * self.tile // 2, y_offset))
                s.blit(stats_text, stats_rect)
                y_offset += 30
                
                # Movement bonus (every 3 levels)
                if unit.level % 3 == 0:
                    move_text = med_font.render("MOVE +1", True, (100, 200, 255))
                    move_rect = move_text.get_rect(center=(self.width * self.tile // 2, y_offset))
                    s.blit(move_text, move_rect)
                    y_offset += 30
                
                # Add spacing between multiple units
                if i < len(leveled_up_units) - 1:
                    y_offset += 20
        
        # Boss victory story overlay
        if self.boss_victory_story_active:
            # Create story overlay
            story_overlay = pygame.Surface((self.width * self.tile - 80, self.height * self.tile - 160), pygame.SRCALPHA)
            story_overlay.fill((0, 0, 0, 200))
            story_rect = story_overlay.get_rect(center=(self.width * self.tile // 2, self.height * self.tile // 2))
            self.screen.blit(story_overlay, story_rect)
            
            # Create clipping region for text
            clip_rect = pygame.Rect(story_rect.left + 40, story_rect.top + 40, 
                                   story_rect.width - 80, story_rect.height - 80)
            self.screen.set_clip(clip_rect)
            
            # Boss victory story content
            story_text = (
                "VICTORY OVER MALAKOR!\n\n"
                "With a final, decisive strike, the heroes have defeated the evil sorcerer Malakor. "
                "His dark influence over Tharen begins to fade, and the shadow creatures that once "
                "terrorized the land now dissolve into nothingness.\n\n"
                "Prince Alaric stands victorious, his sword still gleaming from the battle. "
                "Lyra the Archer lowers her bow, a look of relief on her face. "
                "Marcus the Mage sheathes his staff, the arcane energies now calm. "
                "And Borin the Hose gives a mighty cheer, his strength having turned the tide.\n\n"
                "The people of Tharen emerge from their homes, tentative at first, then celebrating "
                "in the streets. The darkness that had gripped their realm for so long is finally broken. "
                "Hope returns to the hearts of the brave, and the realm begins to heal.\n\n"
                "Though Malakor is defeated, the heroes know their journey is not over. "
                "Other threats may lurk in the shadows, and new challenges await. "
                "But for now, they have won a great victory for the realm of Tharen.\n\n"
                "This day will be remembered as the day the heroes brought light back to Tharen... "
                "the day MALAKOR FELL!\n\n"
                "The heroes have saved Tharen... for now.\n\n"
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
                
                text_rect = text.get_rect(center=(self.width * self.tile // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 35 if line == "" else 40
            
            # Reset clipping
            self.screen.set_clip(None)
        
        # victory/defeat overlay (only show if not in boss story)
        if self.state.game_over and not self.boss_victory_story_active:
            overlay = pygame.Surface((self.width * self.tile, self.height * self.tile), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            s.blit(overlay, (0, 0))
            
            # big victory/defeat text
            if self.state.victory:
                big_font = pygame.font.SysFont(None, 72)
                victory_text = big_font.render(f"{self.get_level_name()} VICTORY!", True, (255, 215, 0))
                text_rect = victory_text.get_rect(center=(self.width * self.tile // 2, self.height * self.tile // 2 - 20))
                s.blit(victory_text, text_rect)
                
                sub_font = pygame.font.SysFont(None, 36)
                sub_text = sub_font.render("Advancing to next level...", True, (255, 255, 255))
                sub_rect = sub_text.get_rect(center=(self.width * self.tile // 2, self.height * self.tile // 2 + 30))
                s.blit(sub_text, sub_rect)
            else:
                big_font = pygame.font.SysFont(None, 72)
                defeat_text = big_font.render("DEFEAT!", True, (200, 50, 50))
                text_rect = defeat_text.get_rect(center=(self.width * self.tile // 2, self.height * self.tile // 2 - 20))
                s.blit(defeat_text, text_rect)
                
                sub_font = pygame.font.SysFont(None, 36)
                sub_text = sub_font.render("All units lost!", True, (255, 255, 255))
                sub_rect = sub_text.get_rect(center=(self.width * self.tile // 2, self.height * self.tile // 2 + 30))
                s.blit(sub_text, sub_rect)
