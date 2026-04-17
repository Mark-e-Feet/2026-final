import pygame
import sys
from game.menu import HomeScreen
from game.core import Game
import classes.unit as unit_module


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
        
        # Check for secret codes
        if game_mode == "K.K.23":
            # Enable knight transformation mode - all enemies become knights, except bosses (knights become soldiers)
            unit_module.KNIGHTFALL_MODE = True
            print("================================")
            print("     KNIGHT MODE ACTIVATED!   ")
            print(" All enemies become KNIGHTS!      ")
            print(" (Knights become SOLDIERS!)       ")
            print("================================")
            import time
            time.sleep(1)  # Brief pause to let user see message
            continue  # Return to home screen
        elif game_mode == "K.K.23_enabled":
            # K.K.23 was activated - set the flag
            unit_module.KNIGHTFALL_MODE = True
            print("================================")
            print("     KNIGHT MODE ACTIVATED!   ")
            print(" All enemies become KNIGHTS!      ")
            print(" (Knights become SOLDIERS!)       ")
            print("================================")
            import time
            time.sleep(1)  # Brief pause to let user see message
            continue  # Return to home screen
        elif game_mode == "NORMAL":
            # Disable knight transformation mode
            unit_module.KNIGHTFALL_MODE = False
            print("K.K.23 mode disabled! Game returns to normal enemy types.")
            continue  # Return to home screen
        
        # Start game with appropriate mode
        if game_mode == "Part 1":
            game = Game(screen=screen, width=12, height=8)
            game.enable_scrolling = False
            game.run()
        elif game_mode == "Part 2":
            # Start directly at level 6 with expanded battlefield
            game = Game(screen=screen, width=24, height=16, starting_level=6)
            game.enable_scrolling = True
            game.run()
        elif game_mode == "Part 3":
            # Start directly at level 12 with ultra-expanded battlefield
            game = Game(screen=screen, width=12, height=24, starting_level=12)
            game.enable_scrolling = True
            game.run()
        elif game_mode == "Part 4":
            # Start directly at level 18 with 30x8 battlefield
            game = Game(screen=screen, width=30, height=8, starting_level=18)
            game.enable_scrolling = True
            game.run()
        elif game_mode == "double_xp_enabled":
            # Enable double XP mode globally
            unit_module.DOUBLE_XP_ENABLED = True
            print("Double XP mode enabled! You will now receive 2x experience from defeating enemies.")
            continue  # Return to home screen
        elif game_mode and game_mode.startswith("level_"):
            # Extract level number from "level_X" format
            try:
                level_num = int(game_mode.split("_")[1])
                if 1 <= level_num <= 23:
                    # Determine battlefield size based on level
                    if level_num <= 5:
                        game = Game(screen=screen, width=12, height=8, starting_level=level_num)
                        game.enable_scrolling = False
                    elif level_num <= 11:
                        game = Game(screen=screen, width=24, height=16, starting_level=level_num)
                        game.enable_scrolling = True
                    elif level_num <= 17:
                        game = Game(screen=screen, width=12, height=24, starting_level=level_num)
                        game.enable_scrolling = True
                    elif level_num <= 22:
                        game = Game(screen=screen, width=30, height=8, starting_level=level_num)
                        game.enable_scrolling = True
                    elif level_num == 23:
                        game = Game(screen=screen, width=15, height=35, starting_level=level_num)
                        game.enable_scrolling = True
                    else:
                        game = Game(screen=screen, width=32, height=32, starting_level=level_num)
                        game.enable_scrolling = True
                    
                    # Run the game
                    game.run()
                else:
                    print("Invalid level number. Please choose a level between 1 and 23.")
            except (ValueError, IndexError):
                print("Invalid level format. Please select a level from the menu.")
        else:
            print(f"Unknown game mode: {game_mode}")
    
    pygame.quit()


if __name__ == "__main__":
    main()
