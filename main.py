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
        game_mode = home_screen.run()
        if not game_mode:
            break
        
        # Start the game with appropriate mode
        if game_mode == "Part 1":
            game = Game(screen=screen, width=12, height=8)
            game.enable_scrolling = False
        elif game_mode == "Part 2":
            # Start directly at level 6 with expanded battlefield
            game = Game(screen=screen, width=24, height=16, starting_level=6)
            game.enable_scrolling = True
        else:
            # Default to original for safety
            game = Game(screen=screen, width=12, height=8)
            game.enable_scrolling = False
        
        game.run()
    
    pygame.quit()


if __name__ == "__main__":
    main()