import pygame
from game.core import Game


class HomeScreen:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.running = True
        self.selected_option = 0
        self.options = ["Start Game", "Instructions", "Exit"]
        
        # Auto-play story timer
        self.story_timer = 0.0
        self.story_delay = 3.0  # Wait 3 seconds before showing story
        self.showing_story = False
        self.story_started = False
        
        # Story scrolling
        self.story_scroll_offset = 0.0  # Continuous scroll offset
        self.scroll_speed = 0.5  # Pixels per frame for smooth scrolling
        
        # Fonts
        self.title_font = pygame.font.SysFont(None, 72)
        self.option_font = pygame.font.SysFont(None, 48)
        self.instruction_font = pygame.font.SysFont(None, 24)
        self.story_font = pygame.font.SysFont(None, 32)
        
        # Colors
        self.bg_color = (20, 20, 30)
        self.title_color = (255, 215, 0)
        self.option_color = (255, 255, 255)
        self.selected_color = (100, 150, 255)
        self.text_color = (200, 200, 200)
        self.story_color = (255, 255, 200)
        
    def draw(self):
        # Background
        self.screen.fill(self.bg_color)
        
        # Draw decorative border
        border_rect = pygame.Rect(20, 20, self.width - 40, self.height - 40)
        pygame.draw.rect(self.screen, (50, 50, 70), border_rect, 3)
        
        # Show story if timer reached
        if self.showing_story:
            self.draw_story()
        else:
            # Normal menu display
            # Title
            title_text = self.title_font.render("Heroes of Tharen", True, self.title_color)
            title_rect = title_text.get_rect(center=(self.width // 2, 100))
            self.screen.blit(title_text, title_rect)
            
            # Subtitle
            subtitle_text = self.option_font.render("A Tactical RPG Adventure", True, self.text_color)
            subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, 160))
            self.screen.blit(subtitle_text, subtitle_rect)
            
            # Menu options
            start_y = 300
            for i, option in enumerate(self.options):
                color = self.selected_color if i == self.selected_option else self.option_color
                option_text = self.option_font.render(option, True, color)
                option_rect = option_text.get_rect(center=(self.width // 2, start_y + i * 80))
                self.screen.blit(option_text, option_rect)
                
                # Draw selection indicator
                if i == self.selected_option:
                    indicator_rect = pygame.Rect(option_rect.left - 40, option_rect.centery - 15, 30, 30)
                    pygame.draw.rect(self.screen, self.selected_color, indicator_rect, 2)
                    pygame.draw.polygon(self.screen, self.selected_color, [
                        (indicator_rect.left + 8, indicator_rect.centery),
                        (indicator_rect.left + 22, indicator_rect.centery - 8),
                        (indicator_rect.left + 22, indicator_rect.centery + 8)
                    ])
            
            # Instructions preview
            if self.selected_option == 1:
                self.draw_instructions_preview()
            
            # Story timer indicator
            if self.story_timer > 0:
                timer_text = self.instruction_font.render(f"Story begins in {int(self.story_delay - self.story_timer) + 1}...", True, self.text_color)
                timer_rect = timer_text.get_rect(center=(self.width // 2, self.height - 80))
                self.screen.blit(timer_text, timer_rect)
            
            # Footer
            footer_text = self.instruction_font.render("Use Arrow Keys or Mouse to Navigate, Enter or Click to Select", True, self.text_color)
            footer_rect = footer_text.get_rect(center=(self.width // 2, self.height - 40))
            self.screen.blit(footer_text, footer_rect)
    
    def draw_story(self):
        """Draws intro story/cutscene with scrolling"""
        # Darken background for story
        story_overlay = pygame.Surface((self.width - 80, self.height - 160), pygame.SRCALPHA)
        story_overlay.fill((0, 0, 0, 200))
        story_rect = story_overlay.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(story_overlay, story_rect)
        
        # Create clipping surface for text area
        clip_rect = pygame.Rect(story_rect.left + 40, story_rect.top + 40, 
                                story_rect.width - 80, story_rect.height - 80)
        
        # Set clipping region
        self.screen.set_clip(clip_rect)
        
        # Extended story content as continuous text
        story_text = (
            "THE LEGEND OF THAREN\n\n"
            "In the land of Tharen there was a great war against the dragons and people. "
            "The evil sorcerer Malakor, once a trusted advisor to the throne "
            "has been corrupted by forbidden magic and now seeks to enslave all kingdoms. "
            "His armies of shadow creatures march upon peaceful villages, "
            "and the people of Tharen live in fear and despair.\n\n"
            "But hope remains in the hearts of the brave. "
            "In the hidden valley of Eldoria, a group of heroes has gathered, "
            "led by the noble Prince Alaric, heir to the fallen kingdom. "
            "With him stand the finest warriors: Lyra the Archer, whose arrows "
            "never miss their mark; Marcus the Mage, master of arcane arts; "
            "and Borin the Hose, a warrior of unmatched strength.\n\n"
            "These heroes have sworn an oath to restore light to Tharen, "
            "to defeat Malakor and break his dark hold over the realm. "
            "With tactical skill, unwavering courage, and the bonds of friendship, "
            "they embark on an epic quest that will determine the fate of their world.\n\n"
            "Their journey will take them through corrupted forests, "
            "across treacherous mountains, and into the heart of darkness itself. "
            "They will face impossible odds, make unlikely alliances, "
            "and discover that the greatest power lies not in magic, but in hope.\n\n"
            "This is their story...\n\n"
            "This is... HEROES OF THAREN\n\n"
            "Press any key to continue..."
        )
        
        # Render the story text with continuous scrolling and text wrapping
        lines = story_text.split('\n')
        y_offset = clip_rect.top - self.story_scroll_offset
        max_width = clip_rect.width  # Use clip rect width for proper fitting
        
        for line in lines:
            if line == "THE LEGEND OF THAREN":
                text = self.title_font.render(line, True, self.title_color)
                text_rect = text.get_rect(center=(self.width // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 50
            elif line == "This is... HEROES OF THAREN":
                text = self.option_font.render(line, True, self.title_color)
                text_rect = text.get_rect(center=(self.width // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 50
            elif line == "Press any key to continue...":
                text = self.instruction_font.render(line, True, self.story_color)
                text_rect = text.get_rect(center=(self.width // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 40
            elif line == "":
                y_offset += 20  # Smaller gap for empty lines
            else:
                # Wrap long lines to fit within screen
                words = line.split(' ')
                current_line = ""
                
                for word in words:
                    test_line = current_line + word + " " if current_line else word
                    test_surface = self.story_font.render(test_line, True, self.story_color)
                    
                    if test_surface.get_width() <= max_width:
                        current_line = test_line
                    else:
                        if current_line:
                            # Render the current line
                            text = self.story_font.render(current_line.strip(), True, self.story_color)
                            text_rect = text.get_rect(center=(self.width // 2, y_offset))
                            self.screen.blit(text, text_rect)
                            y_offset += 35
                        current_line = word + " "
                
                # Render remaining text
                if current_line:
                    text = self.story_font.render(current_line.strip(), True, self.story_color)
                    text_rect = text.get_rect(center=(self.width // 2, y_offset))
                    self.screen.blit(text, text_rect)
                    y_offset += 35
        
        # Reset clipping region
        self.screen.set_clip(None)
    
    def draw_instructions_preview(self):
        # Semi-transparent overlay for instructions
        overlay = pygame.Surface((self.width - 200, 300), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        overlay_rect = overlay.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(overlay, overlay_rect)
        
        instructions = [
            "HOW TO PLAY:",
            "",
            "• Click units to select them",
            "• Green tiles show movement range",
            "• Red tiles show attack targets", 
            "• Defeat all enemies to advance",
            "• Units gain EXP and level up!",
            "• Press SPACE to end player turn",
            "",
            "Press ESC to return to menu"
        ]
        
        y_offset = overlay_rect.top + 20
        for line in instructions:
            if line == "HOW TO PLAY:":
                text = self.option_font.render(line, True, self.title_color)
            else:
                text = self.instruction_font.render(line, True, self.text_color)
            text_rect = text.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25 if line.startswith("•") else 35
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if self.showing_story:
                    # Story controls
                    if event.key == pygame.K_UP:
                        self.story_scroll_offset = max(0, self.story_scroll_offset - 20)
                    elif event.key == pygame.K_DOWN:
                        self.story_scroll_offset = min(1000, self.story_scroll_offset + 20)
                    elif event.key == pygame.K_PAGEUP:
                        self.story_scroll_offset = max(0, self.story_scroll_offset - 100)
                    elif event.key == pygame.K_PAGEDOWN:
                        self.story_scroll_offset = min(1000, self.story_scroll_offset + 100)
                    else:
                        # Any other key returns to menu
                        self.showing_story = False
                        self.story_timer = 0.0
                        self.story_started = True
                else:
                    # Reset story timer on any interaction
                    self.story_timer = 0.0
                    
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:  # Start Game
                            return "play"
                        elif self.selected_option == 1:  # Instructions
                            return "instructions"
                        elif self.selected_option == 2:  # Exit
                            return "exit"
                    elif event.key == pygame.K_ESCAPE:
                        return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.showing_story:
                    # Click during story returns to menu
                    self.showing_story = False
                    self.story_timer = 0.0
                    self.story_started = True
                else:
                    # Reset story timer on mouse interaction
                    self.story_timer = 0.0
                    
                    # Check mouse click on menu options
                    mouse_x, mouse_y = event.pos
                    start_y = 300
                    
                    for i, option in enumerate(self.options):
                        option_rect = pygame.Rect(self.width // 2 - 100, start_y + i * 80 - 24, 200, 48)
                        if option_rect.collidepoint(mouse_x, mouse_y):
                            if i == 0:  # Start Game
                                return "play"
                            elif i == 1:  # Instructions
                                return "instructions"
                            elif i == 2:  # Exit
                                return "exit"
                            break
            elif event.type == pygame.MOUSEMOTION:
                if not self.showing_story:
                    # Update selected option based on mouse position
                    mouse_x, mouse_y = event.pos
                    start_y = 300
                    
                    for i, option in enumerate(self.options):
                        option_rect = pygame.Rect(self.width // 2 - 100, start_y + i * 80 - 24, 200, 48)
                        if option_rect.collidepoint(mouse_x, mouse_y):
                            self.selected_option = i
                            break
            elif event.type == pygame.MOUSEWHEEL:
                if self.showing_story:
                    # Mouse wheel scrolling
                    if event.y > 0:  # Scroll up
                        self.story_scroll_offset = max(0, self.story_scroll_offset - 30)
                    elif event.y < 0:  # Scroll down
                        self.story_scroll_offset = min(1000, self.story_scroll_offset + 30)
        return None
    
    def show_instructions(self):
        showing = True
        while showing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        showing = False
            
            # Draw instructions screen
            self.screen.fill(self.bg_color)
            
            # Title
            title_text = self.title_font.render("Instructions", True, self.title_color)
            title_rect = title_text.get_rect(center=(self.width // 2, 80))
            self.screen.blit(title_text, title_rect)
            
            instructions = [
                "HEROES OF THAREN - HOW TO PLAY",
                "",
                "BASIC CONTROLS:",
                "• Use mouse to click and select units",
                "• Click green tiles to move selected unit",
                "• Click red tiles to attack enemies",
                "• Press SPACE to end your turn",
                "",
                "GAMEPLAY:",
                "• Your units (blue) fight enemies (red)",
                "• Each unit has movement and attack points",
                "• Defeat all enemies to advance to next level",
                "",
                "LEVELING SYSTEM:",
                "• Units gain EXP by defeating enemies",
                "• Level up increases HP and ATK",
                "• Every 3 levels, units gain +1 movement",
                "• Unit progression carries over between levels",
                "",
                "UNITS:",
                "• Prince: Balanced fighter",
                "• Archer: Long-range attacks (3 tiles)",
                "• Mage: Magical damage dealer",
                "• Hose: Heavy warrior",
                "",
                "Press ESC to return to main menu"
            ]
            
            y_offset = 140
            for line in instructions:
                if line in ["HEROES OF THAREN - HOW TO PLAY", "BASIC CONTROLS:", "GAMEPLAY:", "LEVELING SYSTEM:", "UNITS:"]:
                    text = self.option_font.render(line, True, self.title_color)
                else:
                    text = self.instruction_font.render(line, True, self.text_color)
                text_rect = text.get_rect(center=(self.width // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 30 if line.startswith("•") else 40
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
        
        return None
    
    def run(self):
        while self.running:
            # Update story timer if not started and not showing story
            if not self.story_started and not self.showing_story:
                self.story_timer += 1/60  # Assuming 60 FPS
                if self.story_timer >= self.story_delay:
                    self.showing_story = True
                    self.story_timer = 0.0
            
            # Update continuous scrolling when showing story
            if self.showing_story:
                self.story_scroll_offset += self.scroll_speed
                # Reset when scrolled too far
                if self.story_scroll_offset > 800:
                    self.story_scroll_offset = 0
            
            action = self.handle_events()
            if action == "exit":
                return False
            elif action == "play":
                return True
            elif action == "instructions":
                result = self.show_instructions()
                if result == "exit":
                    return False
            
            self.draw()
            pygame.display.flip()
            pygame.time.Clock().tick(60)
        
        return False
