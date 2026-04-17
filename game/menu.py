import pygame
from game.core import Game


class HomeScreen:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.running = True
        self.selected_option = None
        self.options = ["Part 1", "Part 2", "Part 3", "Part 4", "PI 3.14", "Codes", "Instructions", "Exit"]
        
        # Auto-play story timer
        self.story_timer = 0.0
        self.story_delay = 5.0  # Wait 5 seconds before showing story
        self.showing_story = False
        self.story_started = False
        
        # Story scrolling
        self.story_scroll_offset = 0.0  # Continuous scroll offset
        self.scroll_speed = 0.1  # Pixels per frame for smooth scrolling
        
        # Code input system
        self.entering_code = False
        self.code_input = ""
        self.code_font = pygame.font.SysFont(None, 36)
        
        # Track active codes
        self.active_codes = set()
        self.update_active_codes()
    
    def update_active_codes(self):
        """Update active codes based on current global flags"""
        import classes.unit as unit_module
        self.active_codes.clear()
        
        if unit_module.DOUBLE_XP_ENABLED:
            self.active_codes.add("WWW.RRR.EEE")
        if unit_module.KNIGHTFALL_MODE:
            self.active_codes.add("K.K.23")
        if unit_module.PIKACHU_MODE:
            self.active_codes.add("PI 3.14")
        
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
        self.hover_color = (50, 100, 200)  # Blue color for hover
        self.text_color = (200, 200, 200)
        self.story_color = (255, 255, 200)
        
        # Track hover state
        self.hovered_option = None
        
    def draw(self):
        # Background
        self.screen.fill(self.bg_color)
        
        # Draw decorative border
        border_rect = pygame.Rect(20, 20, self.width - 40, self.height - 40)
        pygame.draw.rect(self.screen, (50, 50, 70), border_rect, 3)
        
        # Show story if timer reached
        if self.showing_story:
            self.draw_story()
        elif self.entering_code:
            # Code input screen
            self.draw_code_input()
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
            
            # Menu options in 3x2 grid
            # Part 1 (top-left)
            option_text = self.option_font.render("Part 1", True, 
                self.selected_color if (self.selected_option is not None and self.selected_option == 0) or self.hovered_option == 0 else self.option_color)
            option_rect = option_text.get_rect(center=(self.width // 2 - 200, 280))
            self.screen.blit(option_text, option_rect)
            
            # Part 2 (top-center)
            option_text = self.option_font.render("Part 2", True,
                self.selected_color if (self.selected_option is not None and self.selected_option == 1) or self.hovered_option == 1 else self.option_color)
            option_rect = option_text.get_rect(center=(self.width // 2, 280))
            self.screen.blit(option_text, option_rect)
            
            # Part 3 (top-right)
            option_text = self.option_font.render("Part 3", True,
                self.selected_color if (self.selected_option is not None and self.selected_option == 2) or self.hovered_option == 2 else self.option_color)
            option_rect = option_text.get_rect(center=(self.width // 2 + 200, 280))
            self.screen.blit(option_text, option_rect)
            
            # Part 4 (middle-left)
            option_text = self.option_font.render("Part 4", True,
                self.selected_color if (self.selected_option is not None and self.selected_option == 3) or self.hovered_option == 3 else self.option_color)
            option_rect = option_text.get_rect(center=(self.width // 2 - 200, 360))
            self.screen.blit(option_text, option_rect)
            
            # Codes (middle-center)
            option_text = self.option_font.render("Codes", True,
                self.selected_color if (self.selected_option is not None and self.selected_option == 4) or self.hovered_option == 4 else self.option_color)
            option_rect = option_text.get_rect(center=(self.width // 2, 360))
            self.screen.blit(option_text, option_rect)
            
            # Instructions (middle-right)
            option_text = self.option_font.render("Instructions", True,
                self.selected_color if (self.selected_option is not None and self.selected_option == 5) or self.hovered_option == 5 else self.option_color)
            option_rect = option_text.get_rect(center=(self.width // 2 + 200, 360))
            self.screen.blit(option_text, option_rect)
            
            # Exit (bottom center)
            option_text = self.option_font.render("Exit", True,
                self.selected_color if (self.selected_option is not None and self.selected_option == 6) or self.hovered_option == 6 else self.option_color)
            option_rect = option_text.get_rect(center=(self.width // 2, 440))
            self.screen.blit(option_text, option_rect)
                
                # Draw selection indicators for each option
            positions = [
                (self.width // 2 - 200, 280),  # Part 1
                (self.width // 2, 280),        # Part 2
                (self.width // 2 + 200, 280),  # Part 3
                (self.width // 2 - 200, 360),  # Part 4
                (self.width // 2, 360),        # Codes
                (self.width // 2 + 200, 360),  # Instructions
                (self.width // 2, 440)          # Exit
            ]
            
            for i, pos in enumerate(positions):
                if (self.selected_option is not None and i == self.selected_option) or i == self.hovered_option:
                    indicator_rect = pygame.Rect(pos[0] - 100, pos[1] - 24, 200, 48)
                    pygame.draw.rect(self.screen, self.selected_color, indicator_rect, 2)
                    pygame.draw.polygon(self.screen, self.selected_color, [
                        (pos[0] - 92, pos[1]),
                        (pos[0] - 78, pos[1] - 8),
                        (pos[0] - 78, pos[1] + 8)
                    ])
            
            # Story timer indicator
            if self.story_timer > 0:
                timer_text = self.instruction_font.render(f"Story begins in {int(self.story_delay - self.story_timer)}...", True, self.text_color)
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
            "HEROES OF THAREN\n\n"
            "Ages ago in the land of Tharen there was a great war against the dragons and people."
            "It was a hard time to live for the people of Tharen.Then five great leaders defeated the dragons and sealed them away."
            "The people of Tharen made the 5 Leaders into  five kingdoms, "
            "Gredson,Tyick,Reevin,Soron,and Lackol.It's been many years with no violence then one day Gredson attacked Lackol!"
            "The other kingdoms live Ready for War at any time.\n\n"
            "But the young prince of Reevin Tristan Sets out toSoron for help to stop this terrible War and Find the secrets of Gredson."
            "Tristan  in his party gets attacked by Bandits working for the Gredson Army.\n\n"
            "This is... HEROES OF THAREN\n\n"
            "Press any key to continue..."
        )
        
        # Render the story text with continuous scrolling and text wrapping
        lines = story_text.split('\n')
        y_offset = clip_rect.top - self.story_scroll_offset
        max_width = clip_rect.width  # Use clip rect width for proper fitting
        
        for line in lines:
            if line == "HEROES OF THAREN":
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

    def draw_expanded_preview(self):
        # Semi-transparent overlay for expanded battlefield info
        overlay = pygame.Surface((self.width - 200, 280), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        overlay_rect = overlay.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(overlay, overlay_rect)
        
        info = [
            "EXPANDED BATTLEFIELD",
            "",
            "• Large 24x16 grid battlefield",
            "• Scroll with WASD or Arrow keys",
            "• More strategic space for battles",
            "• Post-boss content available",
            "• Challenging enemy placements",
            "",
            "For experienced players"
        ]
        
        y_offset = overlay_rect.top + 20
        for line in info:
            if line == "EXPANDED BATTLEFIELD":
                text = self.option_font.render(line, True, self.title_color)
            else:
                text = self.instruction_font.render(line, True, self.text_color)
            text_rect = text.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25 if line.startswith("•") else 35

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
                elif self.entering_code:
                    # Handle code input
                    if event.key == pygame.K_ESCAPE:
                        self.entering_code = False
                        self.code_input = ""
                    elif event.key == pygame.K_RETURN:
                            code_input_upper = self.code_input.upper()
                            if code_input_upper == "LEVELS HT":
                                return "level_select"
                            elif code_input_upper == "WWW.RRR.EEE":
                                import classes.unit as unit_module
                                unit_module.DOUBLE_XP_ENABLED = True
                                self.show_code_confirmation("Double XP Enabled!")
                                self.code_input = ""
                                # Stay in code screen to allow more codes
                            elif code_input_upper == "K.K.23":
                                import classes.unit as unit_module
                                unit_module.KNIGHTFALL_MODE = True
                                self.show_code_confirmation("Knight Mode Activated!")
                                self.code_input = ""
                                # Stay in code screen to allow more codes
                            elif code_input_upper == "PI 3.14":
                                import classes.unit as unit_module
                                unit_module.PIKACHU_MODE = True
                                self.show_code_confirmation("Pikachu has been added to your party!")
                                self.code_input = ""
                                # Stay in code screen to allow more codes
                            else:
                                # Wrong code - show error and clear input
                                self.show_code_confirmation("Invalid Code!")
                                self.code_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.code_input = self.code_input[:-1]
                    else:
                        # Add character to input
                        char = event.unicode
                        if len(self.code_input) < 15:  # Limit code length
                            self.code_input += char.upper()
                else:
                    # Reset story timer on any interaction
                    self.story_timer = 0.0
                    
                    if event.key == pygame.K_UP:
                        if self.selected_option is None:
                            self.selected_option = 0
                        else:
                            self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        if self.selected_option is None:
                            self.selected_option = 0
                        else:
                            self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option is not None:
                            if self.selected_option == 0:  # Part 1
                                return "Part 1"
                            elif self.selected_option == 1:  # Part 2
                                return "Part 2"
                            elif self.selected_option == 2:  # Part 3
                                return "Part 3"
                            elif self.selected_option == 3:  # Part 4
                                return "Part 4"
                            elif self.selected_option == 4:  # Codes
                                self.entering_code = True
                                self.code_input = ""
                            elif self.selected_option == 5:  # Instructions
                                return "instructions"
                            elif self.selected_option == 6:  # Exit
                                return "exit"
                    elif event.key == pygame.K_ESCAPE:
                        if self.entering_code:
                            self.entering_code = False
                            self.code_input = ""
                        else:
                            return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.showing_story:
                    # Click during story returns to menu
                    self.showing_story = False
                    self.story_timer = 0.0
                    self.story_started = True
                elif self.entering_code:
                    # Ignore clicks during code input
                    pass
                else:
                    # Reset story timer on mouse interaction
                    self.story_timer = 0.0
                    
                    # Check mouse click on menu options and update selection
                    mouse_x, mouse_y = event.pos
                    
                    # Define option areas for new layout
                    option_areas = [
                        pygame.Rect(self.width // 2 - 300, 256, 200, 48),  # Part 1
                        pygame.Rect(self.width // 2 - 100, 256, 200, 48),  # Part 2
                        pygame.Rect(self.width // 2 + 100, 256, 200, 48),  # Part 3
                        pygame.Rect(self.width // 2 - 300, 336, 200, 48),  # Part 4
                        pygame.Rect(self.width // 2 - 100, 336, 200, 48), # Codes
                        pygame.Rect(self.width // 2 + 100, 336, 200, 48), # Instructions
                        pygame.Rect(self.width // 2 + 300, 336, 200, 48)  # Exit
                    ]
                    
                    for i, option_rect in enumerate(option_areas):
                        if option_rect.collidepoint(mouse_x, mouse_y):
                            self.selected_option = i  # Update selection on click
                            if i == 0:  # Part 1
                                return "Part 1"
                            elif i == 1:  # Part 2
                                return "Part 2"
                            elif i == 2:  # Part 3
                                return "Part 3"
                            elif i == 3:  # Part 4
                                return "Part 4"
                            elif i == 4:  # Codes
                                self.entering_code = True
                                self.code_input = ""
                            elif i == 5:  # Instructions
                                return "instructions"
                            elif i == 6:  # Exit
                                return "exit"
                            break
            elif event.type == pygame.MOUSEMOTION:
                if not self.showing_story:
                    # Update hover state based on mouse position
                    mouse_x, mouse_y = event.pos
                    
                    # Define option areas for new layout (same as click detection)
                    option_areas = [
                        pygame.Rect(self.width // 2 - 300, 256, 200, 48),  # Part 1
                        pygame.Rect(self.width // 2 - 100, 256, 200, 48),  # Part 2
                        pygame.Rect(self.width // 2 + 100, 256, 200, 48),  # Part 3
                        pygame.Rect(self.width // 2 - 300, 336, 200, 48),  # Part 4
                        pygame.Rect(self.width // 2 - 100, 336, 200, 48), # Codes
                        pygame.Rect(self.width // 2 + 100, 336, 200, 48), # Instructions
                        pygame.Rect(self.width // 2 + 300, 336, 200, 48)  # Exit
                    ]
                    
                    self.hovered_option = None  # Reset hover
                    for i, option_rect in enumerate(option_areas):
                        if option_rect.collidepoint(mouse_x, mouse_y):
                            self.hovered_option = i
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
            ]
            
            y_offset = 140
            for line in instructions:
                if line in ["HEROES OF THAREN - HOW TO PLAY", "BASIC CONTROLS:", "BATTLEFIELD MODES:", "GAMEPLAY:", "LEVELING SYSTEM:", "UNITS:"]:
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
            # Update story timer if not started and not showing story and not entering code
            if not self.story_started and not self.showing_story and not self.entering_code:
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
            elif action == "Part 1":
                return "Part 1"
            elif action == "Part 2":
                return "Part 2"
            elif action == "Part 3":
                return "Part 3"
            elif action == "Part 4":
                return "Part 4"
            elif action == "instructions":
                result = self.show_instructions()
                if result == "exit":
                    return False
            elif action == "level_select":
                result = self.show_level_select()
                if result:
                    return result
            
            self.draw()
            pygame.display.flip()
            pygame.time.Clock().tick(60)
        
        return False
    
    def show_code_confirmation(self, message):
        """Show temporary confirmation message"""
        confirmation_timer = 2.0  # Show for 2 seconds
        
        while confirmation_timer > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
            
            # Calculate delta time
            dt = 0.016  # Assuming 60 FPS
            confirmation_timer -= dt
            
            # Draw normal menu
            self.draw()
            
            # Draw confirmation overlay
            overlay = pygame.Surface((400, 100), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            overlay_rect = overlay.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(overlay, overlay_rect)
            
            # Draw confirmation text
            confirm_text = self.title_font.render(message, True, (0, 255, 0))
            confirm_rect = confirm_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(confirm_text, confirm_rect)
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
    def draw_code_input(self):
        """Draw code input screen"""
        # Update active codes display
        self.update_active_codes()
        
        # Title
        title_text = self.title_font.render("Enter Code", True, self.title_color)
        title_rect = title_text.get_rect(center=(self.width // 2, 120))
        self.screen.blit(title_text, title_rect)
        
        # Code input field
        input_rect = pygame.Rect(self.width // 2 - 200, 200, 400, 60)
        pygame.draw.rect(self.screen, (40, 40, 50), input_rect)
        pygame.draw.rect(self.screen, self.option_color, input_rect, 2)
        
        # Display entered code
        code_text = self.code_font.render(self.code_input, True, self.option_color)
        code_rect = code_text.get_rect(center=input_rect.center)
        self.screen.blit(code_text, code_rect)
        
        # Show active codes
        if self.active_codes:
            active_title = self.instruction_font.render("Active Codes:", True, (100, 255, 100))
            active_rect = active_title.get_rect(center=(self.width // 2, 300))
            self.screen.blit(active_title, active_rect)
            
            y_offset = 330
            for code in sorted(self.active_codes):
                code_display = self.instruction_font.render(f"  {code}", True, (150, 255, 150))
                code_display_rect = code_display.get_rect(center=(self.width // 2, y_offset))
                self.screen.blit(code_display, code_display_rect)
                y_offset += 30
        else:
            no_codes = self.instruction_font.render("No active codes", True, (200, 200, 200))
            no_codes_rect = no_codes.get_rect(center=(self.width // 2, 330))
            self.screen.blit(no_codes, no_codes_rect)
        
        # Instructions
        inst_text = self.instruction_font.render("Enter code to unlock features", True, self.text_color)
        inst_rect = inst_text.get_rect(center=(self.width // 2, 450))
        self.screen.blit(inst_text, inst_rect)
        
        back_text = self.instruction_font.render("Press ESC to go back", True, self.text_color)
        back_rect = back_text.get_rect(center=(self.width // 2, 500))
        self.screen.blit(back_text, back_rect)
    
    def show_level_select(self):
        """Show level selection screen"""
        selecting = True
        selected_level = 1
        
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key == pygame.K_RETURN:
                        return f"level_{selected_level}"
                    elif event.key == pygame.K_UP:
                        selected_level = min(23, selected_level + 1)
                    elif event.key == pygame.K_DOWN:
                        selected_level = max(1, selected_level - 1)
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        # Direct number input
                        level_num = event.key - pygame.K_0
                        if 1 <= level_num <= 23:
                            selected_level = level_num
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Check level number clicks (1-23)
                    for level in range(1, 24):
                        level_x = 100 + ((level - 1) % 6) * 100
                        level_y = 200 + ((level - 1) // 6) * 60
                        level_rect = pygame.Rect(level_x, level_y, 80, 40)
                        if level_rect.collidepoint(mouse_x, mouse_y):
                            selected_level = level
                            break
            
            # Draw level selection screen
            self.screen.fill(self.bg_color)
            
            title_text = self.title_font.render("Select Level", True, self.title_color)
            title_rect = title_text.get_rect(center=(self.width // 2, 100))
            self.screen.blit(title_text, title_rect)
            
            # Draw level grid (4x6 = 24 levels, but we only have 1-23)
            for level in range(1, 24):
                level_x = 100 + ((level - 1) % 6) * 100
                level_y = 200 + ((level - 1) // 6) * 60
                
                # Highlight selected level
                if level == selected_level:
                    pygame.draw.rect(self.screen, self.selected_color, 
                                 pygame.Rect(level_x - 5, level_y - 5, 90, 50), 3)
                
                # Draw level box
                pygame.draw.rect(self.screen, self.option_color, 
                                 pygame.Rect(level_x, level_y, 80, 40), 2)
                
                # Draw level number
                level_text = self.option_font.render(str(level), True, self.text_color)
                level_rect = level_text.get_rect(center=(level_x + 40, level_y + 20))
                self.screen.blit(level_text, level_rect)
            
            # Instructions
            inst_text = self.instruction_font.render("Use Arrow Keys or Mouse to Select, Enter to Start, ESC to Back", True, self.text_color)
            inst_rect = inst_text.get_rect(center=(self.width // 2, 500))
            self.screen.blit(inst_text, inst_rect)
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
