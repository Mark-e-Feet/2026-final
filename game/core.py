import pygame
from game.state import GameState


class Game:
    def __init__(self, width=12, height=8, tile=80):
        self.width = width
        self.height = height
        self.tile = tile
        self.screen = pygame.display.set_mode((width * tile, height * tile + 80))
        pygame.display.set_caption("Tactics Prototype")
        self.clock = pygame.time.Clock()
        self.state = GameState(width, height)
        self.font = pygame.font.SysFont(None, 24)
        self.running = True

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

    def update(self, dt):
        self.state.update(dt)

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
            pygame.draw.rect(s, u.color, pygame.Rect(rx, ry, w, h), border_radius=6)
            hp_text = self.font.render(str(u.hp), True, (255, 255, 255))
            s.blit(hp_text, (u.x * self.tile + 4, u.y * self.tile + 4))
        # selection cursor
        if self.state.selected:
            sel = self.state.selected
            rect = pygame.Rect(sel.x * self.tile, sel.y * self.tile, self.tile, self.tile)
            pygame.draw.rect(s, (200, 200, 0), rect, 3)
        # active enemy indicator during enemy phase
        if hasattr(self.state, 'active_enemy') and self.state.active_enemy:
            active = self.state.active_enemy
            rect = pygame.Rect(active.x * self.tile, active.y * self.tile, self.tile, self.tile)
            pygame.draw.rect(s, (255, 100, 100), rect, 4)  # Red border for active enemy
        # status bar: show active unit and actions
        if not self.state.game_over:
            if self.state.current_phase == 'player':
                # Show player unit info if one is selected
                if self.state.selected:
                    u = self.state.selected
                    status = f"""
                    Level {self.state.current_level} | PLAYER PHASE | Selected: {u.__class__.__name__} @{u.x},{u.y}  
                    Moves: {u.moves_remaining}/{u.move}  Attacks: {u.attacks_remaining}/1  
                    -  Press SPACE to end player phase
                    """
                else:
                    status = f"""
                    Level {self.state.current_level} | PLAYER PHASE | Click a unit to select
                    -  Press SPACE to end player phase
                    """
            else:
                status = f"Level {self.state.current_level} | ENEMY PHASE | Enemy turn in progress..."
                if hasattr(self.state, 'active_enemy') and self.state.active_enemy:
                    status += f" | Active: {self.state.active_enemy.__class__.__name__}"
        elif self.state.game_over:
            if self.state.victory:
                status = f"Level {self.state.current_level} VICTORY! Advancing to next level..."
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
        
        # victory/defeat overlay
        if self.state.game_over:
            overlay = pygame.Surface((self.width * self.tile, self.height * self.tile), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            s.blit(overlay, (0, 0))
            
            # big victory/defeat text
            if self.state.victory:
                big_font = pygame.font.SysFont(None, 72)
                victory_text = big_font.render(f"LEVEL {self.state.current_level} VICTORY!", True, (255, 215, 0))
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
