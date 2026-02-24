import pygame
import random
import sys

WIDTH, HEIGHT = 1540, 800
PLAYER_SIZE = 48
COLLECT_SIZE = 18
BG_COLOR = (30, 30, 40)
PLAYER_COLOR = (80, 200, 120)
COLLECT_COLOR = (240, 200, 60)
FPS = 60

def clamp_rect(pos, size):
    x = max(0, min(pos.x, WIDTH - size))
    y = max(0, min(pos.y, HEIGHT - size))
    return pygame.Vector2(x, y)

class Player:
    def __init__(self):
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        self.size = PLAYER_SIZE
        self.speed = 320.0

    def rect(self):
        return pygame.Rect(int(self.pos.x), int(self.pos.y), self.size, self.size)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move.x += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move.y += 1
        if move.length_squared() > 0:
            move = move.normalize()
            self.pos += move * self.speed * dt
        self.pos = clamp_rect(self.pos, self.size)

    def draw(self, surf):
        pygame.draw.rect(surf, PLAYER_COLOR, self.rect(), border_radius=6)

class Collectible:
    def __init__(self):
        self.size = COLLECT_SIZE
        self.respawn()

    def respawn(self):
        margin = 10
        x = random.randint(margin, WIDTH - self.size - margin)
        y = random.randint(margin, HEIGHT - self.size - margin)
        self.pos = pygame.Vector2(x, y)

    def rect(self):
        return pygame.Rect(int(self.pos.x), int(self.pos.y), self.size, self.size)

    def draw(self, surf):
        pygame.draw.ellipse(surf, COLLECT_COLOR, self.rect())

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Pygame: Collect and Move")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    player = Player()
    collect = Collectible()
    score = 0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        player.update(dt)

        # Check collision with collectible
        if player.rect().colliderect(collect.rect()):
            score += 1
            collect.respawn()

        # Render
        screen.fill(BG_COLOR)
        player.draw(screen)
        collect.draw(screen)

        score_surf = font.render(f"Score: {score}", True, (235, 235, 235))
        instr_surf = font.render("Move: WASD / Arrows — Esc to quit", True, (180, 180, 180))
        screen.blit(score_surf, (8, 8))
        screen.blit(instr_surf, (8, HEIGHT - 36))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
