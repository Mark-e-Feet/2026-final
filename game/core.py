import pygame
from game.state import GameState


class Game:
    def __init__(self, width=8, height=6, tile=64):
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
                    self.state.end_unit_turn()

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
        # status bar: show active unit and AP
        active = self.state.active_unit
        if active:
            status = f"""
            Active: {active.team} @{active.x},{active.y}  
            AP: {active.ap}/{active.max_ap}  Init: {active.initiative}  
            -  Press SPACE to end unit turn
            """
        else:
            status = "No active unit"
        lines = status.strip().split('\n')
        #txt = self.font.render(status, True, (220, 220, 220))
        s.fill((40, 40, 40), (0, self.height * self.tile, self.width * self.tile, 40))
        for i, line in enumerate(lines):
            txt = self.font.render(line.strip(), True, (220, 220, 220))
            s.blit(txt, (8, self.height * self.tile + 8 + i * 20))
