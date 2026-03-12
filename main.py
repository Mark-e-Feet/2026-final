import pygame
from game.core import Game
from game.menu import HomeScreen


def main():
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((960, 720))  # 12x8 grid with 80px tiles + status bar
    pygame.display.set_caption("Heroes of Tharen")
    
    # Create and run home screen
    home_screen = HomeScreen(screen)
    
    while True:
        # Show home screen
        should_play = home_screen.run()
        if not should_play:
            break
        
        # Start the game
        game = Game(screen=screen)
        game.run()
    
    pygame.quit()


if __name__ == "__main__":
    main()