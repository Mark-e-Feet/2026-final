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
        self.scroll_speed = 600  # Pixels per second (7.5 tiles per second with 80px tiles)
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
        self.state = GameState(width, height, starting_level, self)
        self.font = pygame.font.SysFont(None, 24)
        self.running = True
        
        # Track phase for music
        self.current_music_phase = None
        self.music_channel = pygame.mixer.Channel(0)  # Use channel 0 for music
        
        # Boss victory music timing
        self.waiting_for_boss_victory_music = False
        self.boss_victory_music_start_time = 0
        
        # Victory timing system
        self.victory_sign_start_time = 0
        self.victory_sign_duration = 4000  # 4 seconds for regular battles (4000ms)
        self.boss_victory_sign_duration = 10000  # 10 seconds for boss battles (10000ms)
        
        # Victory music flags to prevent multiple plays
        self.victory_music_played = False
        self.boss_victory_music_played = False
        
        # Load terrain images
        try:
            self.grass_image = pygame.image.load("assets/grass.png")
            self.dirt_image = pygame.image.load("assets/dirtpath.png")
            self.castle_image = pygame.image.load("assets/castle.png")
            self.road_image = pygame.image.load("assets/roed.png")
            self.destroyed_house_image = pygame.image.load("assets/destroyed house.png")
            # Load new terrain images
            self.sord_image = pygame.image.load("assets/sord.png")
            self.pillar_image = pygame.image.load("assets/pillar.png")
            self.mat_image = pygame.image.load("assets/mat.png")
            self.throne_image = pygame.image.load("assets/throne.png")
            self.cave_image = pygame.image.load("assets/cave.png")
            # Scale images to tile size
            self.grass_image = pygame.transform.scale(self.grass_image, (tile, tile))
            self.dirt_image = pygame.transform.scale(self.dirt_image, (tile, tile))
            self.castle_image = pygame.transform.scale(self.castle_image, (tile, tile))
            self.road_image = pygame.transform.scale(self.road_image, (tile, tile))
            self.destroyed_house_image = pygame.transform.scale(self.destroyed_house_image, (tile, tile))
            self.sord_image = pygame.transform.scale(self.sord_image, (tile, tile))
            self.pillar_image = pygame.transform.scale(self.pillar_image, (tile, tile))
            self.mat_image = pygame.transform.scale(self.mat_image, (tile, tile))
            self.throne_image = pygame.transform.scale(self.throne_image, (tile, tile))
            self.cave_image = pygame.transform.scale(self.cave_image, (tile, tile))
        except pygame.error as e:
            print(f"Could not load terrain images: {e}")
            # Fallback to solid colors if images fail to load
            self.grass_image = None
            self.dirt_image = None
            self.castle_image = None
            self.road_image = None
            self.destroyed_house_image = None
            self.sord_image = None
            self.pillar_image = None
            self.mat_image = None
            self.throne_image = None
            self.cave_image = None
        
        # Load character images
        self.character_images = {}
        try:
            # Load terrain tiles for battlefield artwork
            self.terrain_tiles = {}
            try:
                # Load and scale terrain tiles
                grass_img = pygame.image.load("assets/grass.png")
                dirt_img = pygame.image.load("assets/dirtpath.png")
                road_img = pygame.image.load("assets/roed.png")  # Use roed.png for road
                castle_img = pygame.image.load("assets/castle.png")
                destroyed_img = pygame.image.load("assets/destroyed house.png")
                magic_img = pygame.image.load("assets/magic.png")
                
                # Scale all images to tile size
                self.terrain_tiles['G'] = pygame.transform.scale(grass_img, (self.tile, self.tile))
                self.terrain_tiles['D'] = pygame.transform.scale(dirt_img, (self.tile, self.tile))
                self.terrain_tiles['R'] = pygame.transform.scale(road_img, (self.tile, self.tile))  # Road uses roed.png
                self.terrain_tiles['C'] = pygame.transform.scale(castle_img, (self.tile, self.tile))
                self.terrain_tiles['H'] = pygame.transform.scale(destroyed_img, (self.tile, self.tile))
                self.terrain_tiles['M'] = pygame.transform.scale(magic_img, (self.tile, self.tile))  # Scale magic properly
                print("Terrain tiles loaded")
            except FileNotFoundError as e:
                print(f"Terrain tile files not found: {e}")
                # Create fallback colored surfaces
                self.terrain_tiles['G'] = pygame.Surface((self.tile, self.tile))
                self.terrain_tiles['G'].fill((34, 139, 34))  # Green for grass
                self.terrain_tiles['D'] = pygame.Surface((self.tile, self.tile))
                self.terrain_tiles['D'].fill((139, 69, 19))  # Brown for dirt
                self.terrain_tiles['R'] = pygame.Surface((self.tile, self.tile))
                self.terrain_tiles['R'].fill((105, 105, 105))  # Gray for road
                self.terrain_tiles['C'] = pygame.Surface((self.tile, self.tile))
                self.terrain_tiles['C'].fill((128, 128, 128))  # Gray for castle
                self.terrain_tiles['H'] = pygame.Surface((self.tile, self.tile))
                self.terrain_tiles['H'].fill((64, 64, 64))  # Dark gray for destroyed house
                self.terrain_tiles['M'] = pygame.Surface((self.tile, self.tile))
                self.terrain_tiles['M'].fill((148, 0, 211))  # Purple for magic
                print("Using fallback terrain tiles")
            
            # Load level layouts from text files
            self.level_layouts = {}
            for level_num in range(7, 14):  # Levels 7-13
                try:
                    with open(f"Levels/level_{level_num}.txt", 'r') as f:
                        layout = [line.strip() for line in f.readlines()]
                        self.level_layouts[level_num] = layout
                        print(f"Loaded level {level_num} layout")
                except FileNotFoundError:
                    print(f"Level {level_num} layout file not found")
                    self.level_layouts[level_num] = None
            
            # Load player character images
            self.character_images['Tristan_P'] = pygame.image.load("assets/tristan P.png")
            self.character_images['Archer_P'] = pygame.image.load("assets/archer P.png")  # Using new archer P image
            self.character_images['Mage_P'] = pygame.image.load("assets/mage P.png")
            self.character_images['Horse_P'] = pygame.image.load("assets/horse P.png")
            self.character_images['Srodman_P'] = pygame.image.load("assets/sorodman P.png")
            self.character_images['Knight_P'] = pygame.image.load("assets/knigt P.png")
            self.character_images['Knig_P'] = pygame.image.load("assets/king P.png")  # Knig class uses king P image
            self.character_images['Soldier_P'] = pygame.image.load("assets/soldier P.png")  # Using soldier P image
            self.character_images['Healer_P'] = pygame.image.load("assets/healer P.png")  # Using new healer P image
            self.character_images['Horsearcher_P'] = pygame.image.load("assets/horsearcher P.png")  # Using new horsearcher P image
            self.character_images['Ballistician_P'] = pygame.image.load("assets/ballistician P.png")  # Using new ballistician P image
            self.character_images['Great_sage_P'] = pygame.image.load("assets/great_sage P.png")
            self.character_images['Pikachu_P'] = pygame.image.load("assets/pikachu.png")  # Load Pikachu image

            # Load enemy character images
            self.character_images['Bandit_E'] = pygame.image.load("assets/bandit E.png")
            self.character_images['Archer_E'] = pygame.image.load("assets/archer E.png")
            self.character_images['Knight_E'] = pygame.image.load("assets/knigt E.png")
            self.character_images['Mage_E'] = pygame.image.load("assets/mage E.png")
            self.character_images['Horse_E'] = pygame.image.load("assets/horse E.png")
            self.character_images['Srodman_E'] = pygame.image.load("assets/srodman E.png")
            self.character_images['Soldier_E'] = pygame.image.load("assets/soldier E.png")
            self.character_images['Boss1_E'] = pygame.image.load("assets/boss 1 E.png")  # Using new boss 1 E image
            self.character_images['Boss2_E'] = pygame.image.load("assets/boss 2 E.png")  # Using new boss 2 E image
            self.character_images['Boss3_E'] = pygame.image.load("assets/boss 3 E.png")  # Using new boss 3 E image
            self.character_images['Healer_E'] = pygame.image.load("assets/healer E.png")  # Using new healer E image
            self.character_images['Horsearcher_E'] = pygame.image.load("assets/horsearcher E.png")  # Using new horsearcher E image
            self.character_images['Ballistician_E'] = pygame.image.load("assets/ballistician E.png")  # Using new ballistician E image
            self.character_images['Darkmage_E'] = pygame.image.load("assets/darkmage E.png")
            self.character_images['Final_Boss_E'] = pygame.image.load("assets/final_boss E.png")
            
            # Scale all character images to be much larger (120x120 instead of 80x80)
            for key in self.character_images:
                self.character_images[key] = pygame.transform.scale(self.character_images[key], (120, 120))
                
        except pygame.error as e:
            print(f"Could not load character images: {e}")
            self.character_images = {}
        
        # Update state dimensions if different from default
        self.state.width = width
        self.state.height = height
        
        # Boss victory story system
        self.boss_victory_story_active = False
        self.boss_victory_story_timer = 0.0
        self.boss_victory_story_duration = 8.0  # Show for 8 seconds
        self.boss_story_scroll_offset = 0.0
        self.boss_story_scroll_speed = 0.1
        
        # Boss 2 victory story system
        self.boss2_victory_story_active = False
        self.boss2_victory_story_timer = 0.0
        self.boss2_victory_story_duration = 8.0  # Show for 8 seconds
        self.boss2_story_scroll_offset = 0.0
        self.boss2_story_scroll_speed = 0.1
        
        # Level 17 victory story system
        self.level17_victory_story_active = False
        self.level17_victory_story_timer = 0.0
        self.level17_victory_story_duration = 8.0  # Show for 8 seconds
        self.level17_story_scroll_offset = 0.0
        self.level17_story_scroll_speed = 0.1
        
        # Level 22 victory story system
        self.level22_victory_story_active = False
        self.level22_victory_story_timer = 0.0
        self.level22_victory_story_duration = 8.0  # Show for 8 seconds
        self.level22_story_scroll_offset = 0.0
        self.level22_story_scroll_speed = 0.1
        
        # Level 23 victory story system
        self.level23_victory_story_active = False
        self.level23_victory_story_timer = 0.0
        self.level23_victory_story_duration = 8.0  # Show for 8 seconds
        self.level23_story_scroll_offset = 0.0
        self.level23_story_scroll_speed = 0.1
        
        # Character-specific epilogue system
        self.character_epilogue_active = False
        self.character_epilogue_timer = 0.0
        self.character_epilogue_duration = 10.0  # Show for 10 seconds per character
        self.current_character_index = 0
        self.surviving_characters = []
        self.surviving_character_objects = []  # Store actual unit objects for names
        
        # Credits system
        self.credits_active = False
        self.credits_timer = 0.0
        self.credits_duration = 30.0  # Show credits for 30 seconds
        self.credits_scroll_offset = 0.0
        self.credits_scroll_speed = 1.0  # Scroll speed for credits
        
        # Character epilogue stories
        self.character_epilogues = {
            'Tristan': [
                "Tristan The Brave Prince",
                "",
                "After Tristan defeated Rather Tristan returned to his",
                "kingdom of Reevin and worked hard and studied because",
                "he knew that the day when the Great War happens again",
                "he'll need to be ready.",
                "",
                "A few years later he became king.",
                "His rule as king was very good  was to be set one of",
                "the best Kings who has ever ruled Reevin."
            ],
            'Archer': [
                "Lusia The Eagle's Eye",
                "",
                "After the final battle she remained a soldier of Reevin.",
                "Her skill with a bow was famed  all throughout Tharen.",
                "",
                "She became the leader of the archers of Reevin.",
                "No one can pass her skill except one."
            ],
            'Mage': [
                "Wen The Young Sage",
                "",
                "After the defeat of Rather Wen went back to",
                "his homeland of Reevin to study Magic.",
                "He traveled many different lands other than",
                "Tharen To study Magic and to help others.",
                "",
                "He was famed and loved by people",
                "throughout the places he traveled.",
                "He would be known as one of the best mages in",
                "Tharen even more than the Great Sage himself."
            ],
            'Horse': [
                "Marcus The Cavalry Master",
                "",
                "After the war he was interested in the kingdom of",
                "Reevin to protect whoever was the ruler of the throne.",
                "Once Tristan was King he served as hard as he ever",
                "could each land in need and still having time to help the king.",
                "",
                "He wasn't known much further than Reevin",
                "but in Reevin he was known very well."
            ],
            'Srodman': [
                "Jake The Old Fighter",
                "",
                "He went back to Soron to serve and help rebuild.",
                "Even as he got old he still helped serve his",
                "Homeland of Soron as much as he could.",
                "",
                "When he got too old to serve Retired but",
                "still helped train some new soldiers",
                "Then he got the nickname of the “Old Fighter”."
            ],
            'Knight': [
                "Sir Galahad The Royal Protector",
                "",
                "After the war he was in charge of all the nights and",
                "was at the right hand of the rulers of Soron.",
                "He was known as one of the greatest Knights of Theron.",
                "",
                "People were feared by his strength and never wanted to attack Soron except a few.",
                "except a few.",
                "He protected the Royal air of Soron with his life."
            ],
            'Soldier1': [
                "Luther The Broken Soldier",
                "",
                "After the war he served as a soldier for Reevin.",
                "A few years later he had an injury and was no",
                "longer able to be a soldier.",
                "",
                "Instead of being a soldier he opened an",
                "Armory for the knights of Reevin.",
            ],
            'Soldier2': [
                "Leo The Loyal Soldier",
                "",
                "After the final battle Leo Luther's brother",
                "continued to serve as a soldier for Reevin.",
                "He was known as one of the greatest soldiers for Reevin.",
                "",
                "He wasn't always known as one of the greatest",
                "soldiers until the Great War happened.",
                "He is also an armorer."
            ],
            'Healer': [
                "Elena The Peaceful Healer",
                "",
                "Instead of going where she lived she went to Reevin",
                "and became a Healer and in much later times she became a teacher.",
                "",
                "She lived a peaceful life until the next",
                "Great War then she worked as hard as she",
                "could to stop it alongside Tristan."
            ],
            'Horsearcher': [
                "Gunnar The Mysterious Archer",
                "",
                "After the war, instead of returning to Reevin he",
                "went to Lackol to help build and restore the kingdom.",
                "He served as a knight for Lackol for a few",
                "years but then one day he vanished never to be seen.",
                "",
                "There's been rumors that he's either been ordered out",
                "by the king or he has been searching for",
                "something or has been kidnapped by Bandits.",
                "But no one really knows the true story."
            ],
            'Ballistician': [
                "Greta The Ballistician Teacher",
                "",
                "After the defeat of Rather he returned to Reevin",
                "soon after he retired and he trained new soldiers.",
                "He was known as one of the greatest trainers.",
                "",
                "At the time the Great War started back he",
                "also started back as a soldier."
            ],
            'Great_sage': [
                "Great Sage Athelstan",
                "",
                "After the war instead of being Secret he now",
                "teaches people all throughout Theron.",
                "His Legend is known very far even further than Tharen.",
                "",
                "He now has a school for people to learn magic.",
                ".When the time of the Great War happened he was",
                "one of the persons that did the most to try to stop it."
            ],
            'Knig': [
                "KING Vens",
                "",
                "After the war he still served as king for a",
                "while longer until he made his son Tristan King.",
                "",
                "Before Tristan was King the war started and King Vens",
                "worked as hard as he could to stop the war."
            ]
        }
        
        # Track if Level transitions have been done
        self.level_6_transition_done = False
        self.level_12_transition_done = False
        
        # Initialize music system
        try:
            pygame.mixer.init()
            
            # Load phase-specific music (handle missing files gracefully)
            try:
                self.player_phase_music = pygame.mixer.Sound("assets/player phase.mp3")
                print("Player phase music loaded")
            except (pygame.error, FileNotFoundError):
                self.player_phase_music = None
                print("Player phase music not found")
                
            try:
                self.enemy_phase_music = pygame.mixer.Sound("assets/enemy phase.mp3")
                print("Enemy phase music loaded")
            except (pygame.error, FileNotFoundError):
                self.enemy_phase_music = None
                print("Enemy phase music not found")
                
            try:
                self.boss_music = pygame.mixer.Sound("assets/boss_song.mp3")
                print("Boss music loaded")
            except (pygame.error, FileNotFoundError):
                self.boss_music = None
                print("Boss music not found")
                
            try:
                self.victory_music = pygame.mixer.Sound("assets/victory.mp3")
                print("Victory music loaded")
            except (pygame.error, FileNotFoundError):
                self.victory_music = None
                print("Victory music not found")
                
            try:
                self.boss_victory_music = pygame.mixer.Sound("assets/boss victory.mp3")
                print("Boss victory music loaded")
            except (pygame.error, FileNotFoundError):
                self.boss_victory_music = None
                print("Boss victory music not found")
            
            try:
                self.endgame_music = pygame.mixer.Sound("assets/endgame.mp3")
                print("Endgame music loaded")
            except (pygame.error, FileNotFoundError):
                self.endgame_music = None
                print("Endgame music not found")
            
            try:
                self.final_boss_music = pygame.mixer.Sound("assets/final_boss.mp3")
                print("Final boss music loaded")
            except (pygame.error, FileNotFoundError):
                self.final_boss_music = None
                print("Final boss music not found")
            
            print("Music system initialized")
        except pygame.error as e:
            print(f"Could not initialize music system: {e}")
            self.player_phase_music = None
            self.enemy_phase_music = None
            self.boss_music = None
            self.final_boss_music = None
            self.endgame_music = None
        
        # Initialize slash sound
        try:
            self.slash_sound = pygame.mixer.Sound("assets/slash.mp3")
            self.slash_sound.set_volume(1.0)  # Maximum volume
            print("Slash sound loaded successfully")
        except pygame.error as e:
            print(f"Could not load slash sound: {e}")
            self.slash_sound = None
        
        # Initialize arrow sound
        try:
            self.arrow_sound = pygame.mixer.Sound("assets/arrow.mp3")
            self.arrow_sound.set_volume(1.0)  # Maximum volume
            print("Arrow sound loaded successfully")
        except pygame.error as e:
            print(f"Could not load arrow sound: {e}")
            self.arrow_sound = None
        
        # Initialize fire magic sound
        try:
            self.fire_magic_sound = pygame.mixer.Sound("assets/fire_magic.mp3")
            self.fire_magic_sound.set_volume(1.0)  # Maximum volume
            print("Fire magic sound loaded successfully")
        except pygame.error as e:
            print(f"Could not load fire magic sound: {e}")
            self.fire_magic_sound = None
        
        # Initialize thunder sound for Pikachu
        try:
            self.thunder_sound = pygame.mixer.Sound("assets/thunder.mp3")
            self.thunder_sound.set_volume(1.0)  # Maximum volume
            print("Thunder sound loaded successfully")
        except pygame.error as e:
            print(f"Could not load thunder sound: {e}")
            self.thunder_sound = None
    
    def play_phase_music(self):
        """Play appropriate music based on current phase and level"""
        if not hasattr(self.state, 'current_phase'):
            return
        
        # Don't change music during character epilogues
        if self.character_epilogue_active:
            return
            
        # Check if phase changed
        if self.current_music_phase != self.state.current_phase:
            self.current_music_phase = self.state.current_phase
            
            # Stop current music
            self.music_channel.stop()
            
            # Determine which music to play
            if self.state.current_level == 23:
                # Level 23 special music behavior
                if self.state.current_phase == 'player':
                    # Level 23 player phase plays final_boss.mp3 specifically
                    music_to_play = self.final_boss_music
                    print("Switching to Final Boss music for Player Phase")
                elif self.state.current_phase == 'enemy':
                    # Level 23 enemy phase plays enemy_phase.mp3
                    music_to_play = self.enemy_phase_music
                    print("Switching to Enemy Phase music")
                else:
                    return  # No music for other phases
            elif self.state.current_phase == 'player':
                # Check if this is a boss level - play boss music during player phase
                if self.state.current_level in [5, 11, 17]:
                    music_to_play = self.boss_music
                    print("Switching to Boss music for Player Phase")
                else:
                    music_to_play = self.player_phase_music
                    print("Switching to Player Phase music")
            elif self.state.current_phase == 'enemy':
                # Enemy phase music stays the same for both boss and regular battles
                music_to_play = self.enemy_phase_music
                print("Switching to Enemy Phase music")
            else:
                return  # No music for other phases
            
            # Play the selected music
            if music_to_play:
                try:
                    self.music_channel.play(music_to_play, -1)  # Loop indefinitely
                    # Set volume based on music type
                    if self.state.current_level == 23 and self.state.current_phase == 'player':
                        self.music_channel.set_volume(0.4)  # Lower volume for final boss music to 40%
                    else:
                        self.music_channel.set_volume(0.4)  # Lower music volume to 40% for all other music
                    phase_name = "Boss" if (self.state.current_phase == 'player' and self.state.current_level in [5, 11, 17]) else self.state.current_phase.title()
                    print(f"Now playing: {phase_name} Phase music")
                except pygame.error as e:
                    print(f"Could not play music: {e}")
            else:
                print(f"No music file available for {self.state.current_phase} phase")

    def play_victory_music(self):
        """Play appropriate victory music based on level type"""
        # Stop all current music
        self.music_channel.stop()
        
        # Determine which victory music to play
        if self.state.current_level == 23:
            # Level 23 plays endgame music - only play once
            if not self.victory_music_played:
                music_to_play = self.endgame_music
                print("Playing Endgame music")
                self.victory_music_played = True
            else:
                music_to_play = None
        elif self.state.current_level in [5, 11, 17]:
            # Boss victory music - only play once
            if not self.boss_victory_music_played:
                music_to_play = self.boss_victory_music
                print("Playing Boss Victory music")
                # Set flag to wait for music before showing story
                self.waiting_for_boss_victory_music = True
                self.boss_victory_music_start_time = pygame.time.get_ticks()
                self.boss_victory_music_played = True
            else:
                music_to_play = None
        else:
            # Regular victory music - only play once
            if not self.victory_music_played:
                music_to_play = self.victory_music
                print("Playing Victory music")
                self.victory_music_played = True
            else:
                music_to_play = None
        
        # Play victory music once (not looping)
        if music_to_play:
            try:
                self.music_channel.play(music_to_play, 0)  # Play once
                self.music_channel.set_volume(0.4)  # Lower victory music volume to 40%
                self.victory_sign_start_time = pygame.time.get_ticks()  # Start victory sign timer
                print("Victory music started")
            except pygame.error as e:
                print(f"Could not play victory music: {e}")
        else:
            print("No victory music file available")

    def restart_music_after_battle(self):
        """Restart appropriate phase music after battle ends"""
        # Check if we should restart music (not during story sequences)
        if not (self.boss_victory_story_active or self.boss2_victory_story_active or 
                  self.level17_victory_story_active or self.level22_victory_story_active or 
                  self.level23_victory_story_active or self.character_epilogue_active):
            self.current_music_phase = None  # Reset to force music restart
            self.play_phase_music()  # Restart appropriate phase music
        else:
            # During character epilogues, ensure endgame music continues playing
            if self.character_epilogue_active and self.endgame_music:
                try:
                    if not self.music_channel.get_busy():
                        self.music_channel.play(self.endgame_music, -1)  # Loop endgame music
                        self.music_channel.set_volume(0.4)
                        print("Continuing endgame music during character epilogues")
                except pygame.error as e:
                    print(f"Could not continue endgame music: {e}")

    def restart_music_for_new_battle(self):
        """Restart music when starting a new battle"""
        self.current_music_phase = None  # Reset to force music restart
        self.play_phase_music()  # Start appropriate phase music for new battle
        
        # Reset victory music flags for new battle
        self.victory_music_played = False
        self.boss_victory_music_played = False

    def play_attack_sound(self, attacker_class_name):
        """Play appropriate attack sound based on unit type"""
        # Don't play sound effects during character epilogues
        if self.character_epilogue_active:
            return
            
        # Units that should play slash sound when attacking
        slash_units = ['Bandit', 'Boss1', 'Final_Boss', 'Horse', 'King', 'Knight', 'Soldier', 'Srodman', 'Tristan']
        
        # Units that should play arrow sound when attacking
        arrow_units = ['Archer', 'Ballistician', 'Horsearcher', 'Boss3']
        
        # Units that should play fire magic sound when attacking
        magic_units = ['Mage', 'Darkmage', 'Boss2', 'Great_sage']
        
        # Units that should play thunder sound when attacking
        thunder_units = ['Pikachu']
        
        # Play slash sound for melee units
        if hasattr(self, 'slash_sound') and self.slash_sound and attacker_class_name in slash_units:
            self.slash_sound.play()
            print(f"Playing slash sound for {attacker_class_name}")
        
        # Play arrow sound for ranged units
        elif hasattr(self, 'arrow_sound') and self.arrow_sound and attacker_class_name in arrow_units:
            self.arrow_sound.play()
            print(f"Playing arrow sound for {attacker_class_name}")
        
        # Play fire magic sound for magic units
        elif hasattr(self, 'fire_magic_sound') and self.fire_magic_sound and attacker_class_name in magic_units:
            self.fire_magic_sound.play()
            print(f"Playing fire magic sound for {attacker_class_name}")
        
        # Play thunder sound for Pikachu
        elif hasattr(self, 'thunder_sound') and self.thunder_sound and attacker_class_name in thunder_units:
            self.thunder_sound.play()
            print(f"Playing thunder sound for {attacker_class_name}")

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
            
            # Update Game class (handles scrolling)
            self.update(dt)
            
            self.draw()
            pygame.display.flip()

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                # Check for character epilogue click first
                if self.character_epilogue_active:
                    self.advance_character_epilogue()
                elif self.level23_victory_story_active:
                    # Click to exit level 23 story and start character epilogues
                    self.level23_victory_story_active = False
                    self.start_character_epilogues()
                    self.restart_music_after_battle()  # Restart music after story
                else:
                    mx, my = ev.pos
                    # Convert mouse coordinates to world coordinates accounting for camera
                    world_x = mx + self.camera_x
                    world_y = my + self.camera_y
                    tx = world_x // self.tile
                    ty = world_y // self.tile
                    if ty < self.height:
                        self.state.on_click(tx, ty)
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 3:  # Right click for healing
                mx, my = ev.pos
                # Convert mouse coordinates to world coordinates accounting for camera
                world_x = mx + self.camera_x
                world_y = my + self.camera_y
                tx = world_x // self.tile
                ty = world_y // self.tile
                if ty < self.height:
                    self.state.on_right_click(tx, ty)
            elif ev.type == pygame.KEYDOWN:
                # Handle Shift+V cheat to beat level 23 immediately
                if ev.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                    if self.state.current_level == 23 and not self.state.game_over:
                        print("Shift+V pressed - Immediate victory for level 23!")
                        # Trigger victory
                        self.state.game_over = True
                        self.state.victory = True
                        self.play_victory_music()  # Play endgame music
                        continue  # Skip other key handling
                
                # Handle Shift+T to move Tristan in front of final boss
                if ev.key == pygame.K_t and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                    if self.state.current_level == 23 and not self.state.game_over:
                        print("Shift+T pressed - Moving Tristan in front of final boss!")
                        # Find Tristan and Final Boss
                        tristan_unit = None
                        final_boss_unit = None
                        
                        for unit in self.state.units:
                            if unit.__class__.__name__ == 'Tristan':
                                tristan_unit = unit
                            elif unit.__class__.__name__ == 'Final_Boss':
                                final_boss_unit = unit
                        
                        # Move Tristan right in front of Final Boss
                        if tristan_unit and final_boss_unit:
                            # Position Tristan directly in front of Final Boss
                            tristan_unit.x = final_boss_unit.x + 1
                            tristan_unit.y = final_boss_unit.y
                            # Center camera on Tristan
                            self.camera_x = tristan_unit.x * self.tile - self.viewport_width * self.tile // 2
                            self.camera_y = tristan_unit.y * self.tile - self.viewport_height * self.tile // 2
                            # Force immediate redraw to show the change
                            self.draw()
                            pygame.display.flip()
                        continue  # Skip other key handling
                
                if ev.key == pygame.K_SPACE:
                    if self.state.current_phase == 'player':
                        self.state.end_player_phase()
                # Skip boss story with any key
                if self.boss_victory_story_active:
                    self.boss_victory_story_active = False
                    self.state.next_level()
                    self.restart_music_after_battle()  # Restart music after story
                # Skip Boss 2 story with any key
                if self.boss2_victory_story_active:
                    self.boss2_victory_story_active = False
                    self.state.next_level()
                    self.restart_music_after_battle()  # Restart music after story
                # Skip Level 17 story with any key
                if self.level17_victory_story_active:
                    self.level17_victory_story_active = False
                    self.state.next_level()
                    self.restart_music_after_battle()  # Restart music after story
                # Skip Level 22 story with any key
                if self.level22_victory_story_active:
                    self.level22_victory_story_active = False
                    self.state.next_level()
                    self.restart_music_after_battle()  # Restart music after story
                # Skip Level 23 story with any key - trigger character epilogues
                if self.level23_victory_story_active:
                    self.level23_victory_story_active = False
                    # Start character epilogue system
                    self.start_character_epilogues()
                # Skip character epilogue with any key
                if self.character_epilogue_active:
                    self.advance_character_epilogue()
                # Skip credits with any key
                if self.credits_active:
                    self.credits_active = False
                    self.running = False
                    print("Credits skipped. Returning to title screen.")
                # Return to main menu when defeated
                if self.state.game_over and not self.state.victory:
                    self.running = False
                # Handle scrolling when enabled - track key press
                if self.state.enable_scrolling and hasattr(self.state, 'enable_scrolling') and ev.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d, pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s]:
                    self.keys_pressed.add(ev.key)
            elif ev.type == pygame.KEYUP:
                # Remove key from pressed set when released
                if ev.key in self.keys_pressed:
                    self.keys_pressed.remove(ev.key)

    def update(self, dt):
        self.state.update(dt)
        
        # Play appropriate music for current phase
        self.play_phase_music()
        
        # Sync scrolling flag and dimensions with GameState
        self.enable_scrolling = self.state.enable_scrolling
        self.width = self.state.width
        self.height = self.state.height
        
        # Handle continuous scrolling when keys are held down
        if (hasattr(self.state, 'enable_scrolling') and self.state.enable_scrolling and 
            hasattr(self, 'width') and hasattr(self, 'height') and 
            hasattr(self, 'viewport_width') and hasattr(self, 'viewport_height') and 
            self.keys_pressed):
            try:
                # Calculate max scroll boundaries using synced dimensions
                max_x = max(0, (self.width - self.viewport_width) * self.tile)
                max_y = max(0, (self.height - self.viewport_height) * self.tile)
                
                # Handle horizontal scrolling - smooth gradual movement
                if pygame.K_LEFT in self.keys_pressed or pygame.K_a in self.keys_pressed:
                    self.camera_x = max(0, self.camera_x - self.scroll_speed * dt)
                if pygame.K_RIGHT in self.keys_pressed or pygame.K_d in self.keys_pressed:
                    self.camera_x = min(max_x, self.camera_x + self.scroll_speed * dt)
                
                # Handle vertical scrolling - smooth gradual movement
                if pygame.K_UP in self.keys_pressed or pygame.K_w in self.keys_pressed:
                    self.camera_y = max(0, self.camera_y - self.scroll_speed * dt)
                if pygame.K_DOWN in self.keys_pressed or pygame.K_s in self.keys_pressed:
                    self.camera_y = min(max_y, self.camera_y + self.scroll_speed * dt)
            except Exception as e:
                # If scrolling fails, disable it to prevent crashes
                print(f"Scrolling error: {e}")
                self.state.enable_scrolling = False
                self.enable_scrolling = False
                # Clear pressed keys to prevent continuous error processing
                self.keys_pressed.clear()
        
        # Camera tracking for active enemy during enemy phase
        if self.state.enable_scrolling and hasattr(self.state, 'active_enemy') and self.state.active_enemy:
            # Reset tristan_centered flag when enemy phase starts
            self.tristan_centered = False
            try:
                # Calculate desired camera position to center on active enemy
                target_x = self.state.active_enemy.x * self.tile - (self.viewport_width * self.tile) // 2
                target_y = self.state.active_enemy.y * self.tile - (self.viewport_height * self.tile) // 2
                
                # Calculate max scroll boundaries
                max_x = max(0, (self.width - self.viewport_width) * self.tile)
                max_y = max(0, (self.height - self.viewport_height) * self.tile)
                
                # Clamp target to boundaries
                target_x = max(0, min(target_x, max_x))
                target_y = max(0, min(target_y, max_y))
                
                # Smooth camera movement towards target
                camera_speed = 12  # Faster camera for enemy tracking
                if abs(target_x - self.camera_x) > camera_speed:
                    if target_x > self.camera_x:
                        self.camera_x += camera_speed
                    else:
                        self.camera_x -= camera_speed
                else:
                    self.camera_x = target_x
                
                if abs(target_y - self.camera_y) > camera_speed:
                    if target_y > self.camera_y:
                        self.camera_y += camera_speed
                    else:
                        self.camera_y -= camera_speed
                else:
                    self.camera_y = target_y
            except Exception as e:
                print(f"Camera tracking error: {e}")
                # Disable camera tracking if it fails
                pass
        else:
            # Check for player phase start and smoothly center on Tristan (only once)
            if self.state.enable_scrolling and hasattr(self.state, 'current_phase') and self.state.current_phase == 'player':
                # Check if we need to center on Tristan (only at phase start)
                if not hasattr(self, 'tristan_centered') or not self.tristan_centered:
                    # Find Tristan
                    tristan_units = [u for u in self.state.units if u.__class__.__name__ == 'Tristan' and u.team == 'player' and u.hp > 0]
                    if tristan_units:
                        tristan = tristan_units[0]
                        # Center camera on Tristan's position
                        target_x = tristan.x * self.tile - (self.viewport_width * self.tile) // 2
                        target_y = tristan.y * self.tile - (self.viewport_height * self.tile) // 2
                        
                        # Calculate max boundaries
                        max_x = max(0, (self.width - self.viewport_width) * self.tile)
                        max_y = max(0, (self.height - self.viewport_height) * self.tile)
                        
                        # Clamp target to boundaries
                        target_x = max(0, min(target_x, max_x))
                        target_y = max(0, min(target_y, max_y))
                        
                        # Smooth camera movement towards Tristan
                        camera_speed = 8  # Smooth movement speed
                        if abs(target_x - self.camera_x) > camera_speed:
                            if target_x > self.camera_x:
                                self.camera_x += camera_speed
                            else:
                                self.camera_x -= camera_speed
                        else:
                            self.camera_x = target_x
                        
                        if abs(target_y - self.camera_y) > camera_speed:
                            if target_y > self.camera_y:
                                self.camera_y += camera_speed
                            else:
                                self.camera_y -= camera_speed
                        else:
                            self.camera_y = target_y
                            
                        # Check if reached target
                        if abs(target_x - self.camera_x) <= camera_speed and abs(target_y - self.camera_y) <= camera_speed:
                            self.tristan_centered = True  # Mark as centered, don't do it again
            
            # Clamp camera to valid boundaries
            max_x = max(0, (self.width - self.viewport_width) * self.tile)
            max_y = max(0, (self.height - self.viewport_height) * self.tile)
            self.camera_x = max(0, min(max_x, self.camera_x))
            self.camera_y = max(0, min(max_y, self.camera_y))
        
        # Check for boss victory and start story
        if self.state.game_over and self.state.victory and self.state.current_level == 5 and not self.boss_victory_story_active:
            if not self.waiting_for_boss_victory_music:
                self.play_victory_music()  # Play boss victory music
            # Check if boss victory music has finished (wait 10 seconds for victory sign)
            if self.waiting_for_boss_victory_music:
                current_time = pygame.time.get_ticks()
                if current_time - self.victory_sign_start_time > self.boss_victory_sign_duration:  # 10 seconds
                    self.boss_victory_story_active = True
                    self.boss_victory_story_timer = self.boss_victory_story_duration
                    self.boss_story_scroll_offset = 0.0
                    self.waiting_for_boss_victory_music = False
                    print("Starting boss victory story after 10 seconds")
        
        # Check for Boss 2 victory and start story
        if self.state.game_over and self.state.victory and self.state.current_level == 11 and not self.boss2_victory_story_active:
            if not self.waiting_for_boss_victory_music:
                self.play_victory_music()  # Play boss victory music
            # Check if boss victory music has finished (wait 10 seconds for victory sign)
            if self.waiting_for_boss_victory_music:
                current_time = pygame.time.get_ticks()
                if current_time - self.victory_sign_start_time > self.boss_victory_sign_duration:  # 10 seconds
                    self.boss2_victory_story_active = True
                    self.boss2_victory_story_timer = self.boss2_victory_story_duration
                    self.boss2_story_scroll_offset = 0.0
                    self.waiting_for_boss_victory_music = False
                    print("Starting boss 2 victory story after 10 seconds")
        
        # Check for Level 17 victory and start story
        if self.state.game_over and self.state.victory and self.state.current_level == 17 and not self.level17_victory_story_active:
            if not self.waiting_for_boss_victory_music:
                self.play_victory_music()  # Play boss victory music
            # Check if boss victory music has finished (wait 10 seconds for victory sign)
            if self.waiting_for_boss_victory_music:
                current_time = pygame.time.get_ticks()
                if current_time - self.victory_sign_start_time > self.boss_victory_sign_duration:  # 10 seconds
                    self.level17_victory_story_active = True
                    self.level17_victory_story_timer = self.level17_victory_story_duration
                    self.level17_story_scroll_offset = 0.0
                    self.waiting_for_boss_victory_music = False
                    print("Starting level 17 victory story after 10 seconds")
        
        # Check for Level 22 victory and start story
        if self.state.game_over and self.state.victory and self.state.current_level == 22 and not self.level22_victory_story_active:
            self.level22_victory_story_active = True
            self.level22_victory_story_timer = self.level22_victory_story_duration
            self.level22_story_scroll_offset = 0.0
        
        # Check for Level 23 victory and start story
        if self.state.game_over and self.state.victory and self.state.current_level == 23 and not self.level23_victory_story_active and not self.character_epilogue_active:
            self.level23_victory_story_active = True
            self.level23_victory_story_timer = self.level23_victory_story_duration
            self.level23_story_scroll_offset = 0.0
            # Play endgame music for level 23 story
            self.music_channel.stop()
            if self.endgame_music:
                try:
                    self.music_channel.play(self.endgame_music, -1)  # Loop endgame music during story
                    self.music_channel.set_volume(0.4)  # Set volume to 40%
                    print("Playing Endgame music during Level 23 story")
                except pygame.error as e:
                    print(f"Could not play endgame music: {e}")
        
        # Boss music disabled - no music during boss battles (levels 5, 11, 17)
        # Sound effects will still play normally
        
        # Check for Level 12 transition to ultra-expanded battlefield (only once)
        if self.state.current_level == 12 and not self.level_12_transition_done:
            # Expand to ultra battlefield and enable scrolling
            self.width = 12
            self.height = 24
            self.viewport_width = 12  # Keep viewport same size
            self.viewport_height = 8  # Keep viewport same size
            self.enable_scrolling = True  # Enable scrolling for ultra battlefield
            # Update state dimensions
            self.state.width = 12
            self.state.height = 24
            # Reset camera position
            self.camera_x = 0
            self.camera_y = 0
            # Mark transition as done
            self.level_12_transition_done = True
        
        # Check for Level 6 transition to expanded battlefield (only once)
        if self.state.current_level == 6 and not self.level_6_transition_done:
            # Enable scrolling and expand battlefield
            self.enable_scrolling = True
            self.state.enable_scrolling = True  # Ensure state scrolling is also enabled
            self.width = 24
            self.height = 16
            self.viewport_width = 12  # Keep viewport same size
            self.viewport_height = 8  # Keep viewport same size
            # Update state dimensions
            self.state.width = 24
            self.state.height = 16
            # Reset camera position
            self.camera_x = 0
            self.camera_y = 0
            # Mark transition as done
            self.level_6_transition_done = True
            print("Level 6 transition: Scrolling enabled and battlefield expanded")
        
        # Check for Level 18 transition to Part 4 battlefield (only once)
        if self.state.current_level == 18 and not hasattr(self, 'level_18_transition_done'):
            # Transition to Part 4 - 30x8 battlefield
            self.width = 30
            self.height = 8
            self.viewport_width = 12  # Keep viewport same size
            self.viewport_height = 8  # Keep viewport same size
            self.enable_scrolling = True  # Enable scrolling for Part 4 battlefield
            # Update state dimensions
            self.state.width = 30
            self.state.height = 8
            self.state.enable_scrolling = True
            # Reset camera position
            self.camera_x = 0
            self.camera_y = 0
            
            # Units are now added in setup_level() - no need for duplicate creation here
            
            # Mark transition as done
            self.level_18_transition_done = True
            print("Transitioned to Part 4 - 30x8 battlefield with new units")
        
        # Update boss victory story
        if self.boss_victory_story_active:
            self.boss_story_scroll_offset += self.boss_story_scroll_speed
            
            # Reset scroll when it goes too far
            if self.boss_story_scroll_offset > 600:
                self.boss_story_scroll_offset = 0.0
                
            # Remove automatic timer ending - story only ends on button press
        
        # Update Level 22 victory story
        if self.level22_victory_story_active:
            self.level22_story_scroll_offset += self.level22_story_scroll_speed
            
            # Reset scroll when it goes too far
            if self.level22_story_scroll_offset > 600:
                self.level22_story_scroll_offset = 0.0
                
            # Remove automatic timer ending - story only ends on button press
        
        # Update Level 23 victory story
        if self.level23_victory_story_active:
            self.level23_story_scroll_offset += self.level23_story_scroll_speed
            
            # Reset scroll when it goes too far
            if self.level23_story_scroll_offset > 600:
                self.level23_story_scroll_offset = 0.0
                
            # Remove automatic timer ending - story only ends on button press
        
        # Character epilogue system - no scrolling (static display)
        
        # Update credits timer and scrolling
        if self.credits_active:
            self.credits_timer += dt
            self.credits_scroll_offset += self.credits_scroll_speed
            
            # Check if credits have finished scrolling (based on scroll offset)
            if self.credits_timer >= self.credits_duration or self.credits_scroll_offset > 2000:
                # Credits finished, return to title screen
                self.credits_active = False
                self.running = False
                print("Credits completed. Returning to title screen.")
        
        # Update Boss 2 victory story
        if self.boss2_victory_story_active:
            self.boss2_story_scroll_offset += self.boss2_story_scroll_speed
            
            # Reset scroll when it goes too far
            if self.boss2_story_scroll_offset > 600:
                self.boss2_story_scroll_offset = 0.0
                
            # Remove automatic timer ending - story only ends on button press

        # Update Level 17 victory story
        if self.level17_victory_story_active:
            self.level17_story_scroll_offset += self.level17_story_scroll_speed
            
            # Reset scroll when it goes too far
            if self.level17_story_scroll_offset > 600:
                self.level17_story_scroll_offset = 0.0
                
            # Remove automatic timer ending - story only ends on button press

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
        start_x = int(self.camera_x // self.tile)
        start_y = int(self.camera_y // self.tile)
        end_x = min(self.width, start_x + self.viewport_width + 1)
        end_y = min(self.height, start_y + self.viewport_height + 1)
        
        # draw grid with terrain (only visible tiles)
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                screen_x = x * self.tile - self.camera_x
                screen_y = y * self.tile - self.camera_y
                rect = pygame.Rect(screen_x, screen_y, self.tile, self.tile)
                
                # Check if current level has text file terrain layout (levels 7-13)
                current_level = getattr(self.state, 'current_level', 1)
                terrain_tile = None
                use_text_layout = False
                
                if (current_level in self.level_layouts and 
                    self.level_layouts[current_level] and
                    y < len(self.level_layouts[current_level]) and 
                    x < len(self.level_layouts[current_level][y])):
                    terrain_char = self.level_layouts[current_level][y][x]
                    if terrain_char in self.terrain_tiles:
                        terrain_tile = self.terrain_tiles[terrain_char]
                        use_text_layout = True
                
                if use_text_layout and terrain_tile:
                    # Use terrain from text file
                    s.blit(terrain_tile, (screen_x, screen_y))
                else:
                    # Use original terrain system for other levels
                    # Check if we have terrain data for this position
                    if (hasattr(self.state, 'terrain') and self.state.terrain and 
                        y < len(self.state.terrain) and x < len(self.state.terrain[y])):
                        terrain_type = self.state.terrain[y][x]
                        
                        # Use terrain images if available, otherwise fallback to colors
                        if terrain_type == 'dirt':
                            if self.dirt_image:
                                s.blit(self.dirt_image, (screen_x, screen_y))
                            else:
                                # Fallback to solid brown
                                color = (101, 67, 33) if (x + y) % 2 == 0 else (92, 51, 23)
                                pygame.draw.rect(s, color, rect)
                        elif terrain_type == 'castle':
                            if self.castle_image:
                                s.blit(self.castle_image, (screen_x, screen_y))
                            else:
                                # Fallback to solid gray
                                color = (128, 128, 128) if (x + y) % 2 == 0 else (105, 105, 105)
                                pygame.draw.rect(s, color, rect)
                        elif terrain_type == 'road':
                            if self.road_image:
                                s.blit(self.road_image, (screen_x, screen_y))
                            else:
                                # Fallback to solid gray
                                color = (105, 105, 105) if (x + y) % 2 == 0 else (84, 84, 84)
                                pygame.draw.rect(s, color, rect)
                        elif terrain_type == 'destroyed_house':
                            if self.destroyed_house_image:
                                s.blit(self.destroyed_house_image, (screen_x, screen_y))
                            else:
                                # Fallback to dark red/brown for destroyed house
                                color = (139, 69, 19) if (x + y) % 2 == 0 else (101, 50, 14)
                                pygame.draw.rect(s, color, rect)
                        elif terrain_type == 'sord':
                            if self.sord_image:
                                s.blit(self.sord_image, (screen_x, screen_y))
                            else:
                                # Fallback to dark gray for sord
                                color = (64, 64, 64) if (x + y) % 2 == 0 else (48, 48, 48)
                                pygame.draw.rect(s, color, rect)
                        elif terrain_type == 'pillar':
                            if self.pillar_image:
                                s.blit(self.pillar_image, (screen_x, screen_y))
                            else:
                                # Fallback to light gray for pillar
                                color = (192, 192, 192) if (x + y) % 2 == 0 else (160, 160, 160)
                                pygame.draw.rect(s, color, rect)
                        elif terrain_type == 'mat':
                            if self.mat_image:
                                s.blit(self.mat_image, (screen_x, screen_y))
                            else:
                                # Fallback to brown for mat
                                color = (139, 90, 43) if (x + y) % 2 == 0 else (121, 85, 61)
                                pygame.draw.rect(s, color, rect)
                        elif terrain_type == 'throne':
                            if self.throne_image:
                                s.blit(self.throne_image, (screen_x, screen_y))
                            else:
                                # Fallback to gold for throne
                                color = (255, 215, 0) if (x + y) % 2 == 0 else (218, 165, 32)
                                pygame.draw.rect(s, color, rect)
                        elif terrain_type == 'cave':
                            if self.cave_image:
                                s.blit(self.cave_image, (screen_x, screen_y))
                            else:
                                # Fallback to dark brown for cave
                                color = (101, 67, 33) if (x + y) % 2 == 0 else (80, 50, 20)
                                pygame.draw.rect(s, color, rect)
                        else:  # grass
                            if self.grass_image:
                                s.blit(self.grass_image, (screen_x, screen_y))
                            else:
                                # Fallback to solid gray-green
                                color = (70, 70, 70) if (x + y) % 2 == 0 else (60, 60, 60)
                                pygame.draw.rect(s, color, rect)
                    else:
                        # Default terrain if no terrain data
                        if self.grass_image:
                            s.blit(self.grass_image, (screen_x, screen_y))
                        else:
                            color = (70, 70, 70) if (x + y) % 2 == 0 else (60, 60, 60)
                            pygame.draw.rect(s, color, rect)
                
                # Draw grid lines around each tile for better visibility
                pygame.draw.rect(s, (30, 30, 30), rect, 1)  # Dark gray grid lines
        # highlights (only visible ones)
        for (x, y) in self.state.highlight_tiles:
            if start_x <= x < end_x and start_y <= y < end_y:
                screen_x = x * self.tile - self.camera_x
                screen_y = y * self.tile - self.camera_y
                rect = pygame.Rect(screen_x, screen_y, self.tile, self.tile)
                # Create a semi-transparent green highlight overlay instead of solid color
                highlight_surface = pygame.Surface((self.tile, self.tile), pygame.SRCALPHA)
                highlight_surface.fill((50, 200, 50, 100))  # Semi-transparent green
                s.blit(highlight_surface, (screen_x, screen_y))
                # Draw a brighter green border
                pygame.draw.rect(s, (100, 255, 100), rect, 3)
        # attack targets (red tint for enemies, blue tint for healable allies)
        if getattr(self.state, 'attack_targets', None):
            for t in self.state.attack_targets:
                if start_x <= t.x < end_x and start_y <= t.y < end_y:
                    screen_x = t.x * self.tile - self.camera_x
                    screen_y = t.y * self.tile - self.camera_y
                    at_rect = pygame.Rect(screen_x, screen_y, self.tile, self.tile)
                    tint = pygame.Surface((self.tile, self.tile), pygame.SRCALPHA)
                    
                    # Check if selected unit is a healer and target is an ally
                    if (getattr(self.state, 'selected', None) and 
                        self.state.selected.__class__.__name__ == 'Healer' and 
                        t.team == self.state.selected.team):
                        # Blue tint for healable allies
                        tint.fill((50, 50, 200, 80))
                        pygame.draw.rect(s, (80, 80, 220), at_rect, 3)
                    else:
                        # Red tint for attackable enemies
                        tint.fill((200, 50, 50, 80))
                        pygame.draw.rect(s, (220, 80, 80), at_rect, 3)
                    
                    s.blit(tint, (screen_x, screen_y))
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
                
                # Draw unit using character image or fallback to colored rectangle
                team_suffix = "P" if u.team == "player" else "E"
                unit_key = f"{u.__class__.__name__}_{team_suffix}"
                if unit_key in self.character_images:
                    # Draw character image centered with black outline (120px image on 80px tile, so -20px offset)
                    img_x = screen_x - 20
                    img_y = screen_y - 20
                    
                    # Create a black silhouette for outline
                    black_img = self.character_images[unit_key].copy()
                    black_img.fill((0, 0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                    
                    # Draw black outline by drawing the black silhouette at 4 offset positions
                    s.blit(black_img, (img_x - 2, img_y))  # Left
                    s.blit(black_img, (img_x + 2, img_y))  # Right
                    s.blit(black_img, (img_x, img_y - 2))  # Top
                    s.blit(black_img, (img_x, img_y + 2))  # Bottom
                    
                    # Draw the main character image on top
                    s.blit(self.character_images[unit_key], (img_x, img_y))
                else:
                    # Fallback to colored rectangle if no image available
                    pygame.draw.rect(s, u.color, pygame.Rect(rx, ry, w, h), border_radius=6)
                
                hp_text = self.font.render(str(u.hp), True, (255, 255, 255))
                s.blit(hp_text, (screen_x + 4, screen_y + 4))
                
                # Draw level indicator for player units (gold color)
                if hasattr(u, 'level') and u.team == 'player' and u.level > 1:
                    level_font = pygame.font.SysFont(None, 16)
                    level_text = level_font.render(str(u.level), True, (255, 215, 0))
                    s.blit(level_text, (screen_x + self.tile - 12, screen_y + 4))
                
                # Draw level indicator for enemy units (red color) - only show level 2+
                if hasattr(u, 'level') and u.team == 'enemy' and u.level > 1:
                    level_font = pygame.font.SysFont(None, 16)
                    level_text = level_font.render(str(u.level), True, (255, 100, 100))
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
                        # Use custom name if available, otherwise use class name
                        unit_name = u.name if u.name else u.__class__.__name__
                        status = f"""
                        {self.get_level_name()} | PLAYER PHASE | Selected: {unit_name} Lv.{u.level} @{u.x},{u.y}  
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
                if self.state.current_level == 23:
                    status = f"{self.get_level_name()} VICTORY! Game Complete!"
                else:
                    status = f"{self.get_level_name()} VICTORY! Advancing to next level..."
            else:
                status = "TRISTAN DEFEATED! Press any key to return to main menu."
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
        
        # Victory overlay for regular battles (non-boss levels, exclude level 23)
        if self.state.game_over and self.state.victory and self.state.current_level not in [5, 11, 17, 23]:
            # Play regular victory music
            self.play_victory_music()
            
            # Create victory overlay for 4 seconds
            current_time = pygame.time.get_ticks()
            if current_time - self.victory_sign_start_time < self.victory_sign_duration:
                overlay = pygame.Surface((self.viewport_width * self.tile, self.viewport_height * self.tile), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                s.blit(overlay, (0, 0))
            
            # Big "VICTORY! Battle Won!" text
            huge_font = pygame.font.SysFont(None, 120)
            victory_text = huge_font.render("VICTORY!", True, (255, 215, 0))
            victory_rect = victory_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 - 60))
            s.blit(victory_text, victory_rect)
            
            # "Battle Won!" text
            big_font = pygame.font.SysFont(None, 72)
            battle_text = big_font.render("Battle Won!", True, (100, 255, 100))
            battle_rect = battle_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2))
            s.blit(battle_text, battle_rect)
            
            # Level completed text
            medium_font = pygame.font.SysFont(None, 48)
            level_text = medium_font.render(f"Level {self.state.current_level} Complete!", True, (200, 200, 255))
            level_rect = level_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 + 60))
            s.blit(level_text, level_rect)
        
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
            story_text = [
                "VICTORY!",
                "",
                "By the time Tristan and his party made it to Soron,",
                "it was already under attack by Gredson's Army!",
                "They found a few surviving knights who were willing",
                "to join Tristan's party.",
                "",
                "One of the knights heard of a great sage in Tyick.",
                "This was just a taste of Gredson's power.",
                "If Tristan wants to defeat Gredson's Army,",
                "he'll need as much help as he can get.",
                "",
                "So Tristan and his party set out to Tyick",
                "in search of the Great Sage.",
                "",
                "Press any key to continue..."
            ]
            
            # Render the story text with scrolling
            lines = story_text
            y_offset = clip_rect.top - self.boss_story_scroll_offset
            max_width = clip_rect.width
            
            for line in lines:
                if line == "VICTORY!":
                    text = pygame.font.SysFont(None, 48).render(line, True, (255, 215, 0))
                elif line == "Press any key to continue...":
                    text = pygame.font.SysFont(None, 24).render(line, True, (255, 255, 200))
                else:
                    text = pygame.font.SysFont(None, 28).render(line, True, (255, 255, 200))
                
                text_rect = text.get_rect(center=(self.viewport_width * self.tile // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 35 if line == "" else 40
            
            # Reset clipping
            self.screen.set_clip(None)
        
        # Boss 2 victory story overlay
        if self.boss2_victory_story_active:
            # Create story overlay
            story_overlay = pygame.Surface((self.viewport_width * self.tile - 80, self.viewport_height * self.tile - 160), pygame.SRCALPHA)
            story_overlay.fill((0, 0, 0, 200))
            story_rect = story_overlay.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2))
            self.screen.blit(story_overlay, story_rect)
            
            # Create clipping region for text
            clip_rect = pygame.Rect(story_rect.left + 40, story_rect.top + 40, 
                                   story_rect.width - 80, story_rect.height - 80)
            self.screen.set_clip(clip_rect)
            
            # Boss 2 victory story content
            story_text = [
                "VICTORY!",
                "",
                "Tristan and his party made it to Tyick.",
                "But on their way to the Great Sage they fought a Mage using",
                "a strange dark Magic keeping them away from the Great Sage.",
                "Tristan and his party defeated him and made it to the Great Sage.",
                "The Great Sage said that the magic that he was using was dark dragon Magic!",
                "Then he also told them of a stone in each kingdom.",
                "Each one of the stones has a great amount of power and",
                "told them that is why Gredson is attacking the kingdoms.",
                "The Great Sage sends them to Reevin to find  the stone of  Reevin.",
                "And Send them off with some new troops. ",
                "So Tristan and his party head back to his homeland of Reevin.",
                "",
                "Press any key to continue..."
            ]
            
            # Render the story text with scrolling
            lines = story_text
            y_offset = clip_rect.top - self.boss2_story_scroll_offset
            max_width = clip_rect.width
            
            for line in lines:
                if line == "VICTORY!":
                    text = pygame.font.SysFont(None, 48).render(line, True, (255, 215, 0))
                elif line == "Press any key to continue...":
                    text = pygame.font.SysFont(None, 24).render(line, True, (255, 255, 200))
                else:
                    text = pygame.font.SysFont(None, 28).render(line, True, (255, 255, 200))
                
                text_rect = text.get_rect(center=(self.viewport_width * self.tile // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 35 if line == "" else 40
            
            # Reset clipping
            self.screen.set_clip(None)
        
        # Level 22 victory story overlay
        if self.level22_victory_story_active:
            # Create story overlay
            story_overlay = pygame.Surface((self.viewport_width * self.tile - 80, self.viewport_height * self.tile - 160), pygame.SRCALPHA)
            story_overlay.fill((0, 0, 0, 200))
            story_rect = story_overlay.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2))
            self.screen.blit(story_overlay, story_rect)
            
            # Create clipping region for text
            clip_rect = pygame.Rect(40, 40, self.viewport_width * self.tile - 80, self.viewport_height * self.tile - 160)
            self.screen.set_clip(clip_rect)
            
            # Story text for Level 22
            story_text = [
                "VICTORY!",
                "",
                "Tristan found the sword!",
                "With the sword in his possession they head straight towards Gredson.",
                "By the time Tristan in his party made it to",
                "Gredson the great sage was already there.",
                "",
                "The Great Sage  felt a strange power.",
                "The king of Gredson Rather",
                "found a legendary spear.",
                "And the dragons were about to be brought back!",
                "The Great Sage joins Tristan and they rush",
                "onward to defeat Rather once and for all!",
                "",
                "Press any key to continue..."
            ]
            
            # Render story text with scrolling
            lines = story_text
            y_offset = clip_rect.top - self.level22_story_scroll_offset
            max_width = clip_rect.width
            
            for line in lines:
                if line == "VICTORY!":
                    text = pygame.font.SysFont(None, 48).render(line, True, (255, 215, 0))
                elif line == "Press any key to continue...":
                    text = pygame.font.SysFont(None, 24).render(line, True, (255, 255, 200))
                else:
                    text = pygame.font.SysFont(None, 28).render(line, True, (255, 255, 200))
                
                text_rect = text.get_rect(center=(self.viewport_width * self.tile // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 35 if line == "" else 40
            
            # Reset clipping
            self.screen.set_clip(None)
        
        # Level 17 victory story overlay
        if self.level17_victory_story_active:
            # Create story overlay
            story_overlay = pygame.Surface((self.viewport_width * self.tile - 80, self.viewport_height * self.tile - 160), pygame.SRCALPHA)
            story_overlay.fill((0, 0, 0, 200))
            story_rect = story_overlay.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2))
            self.screen.blit(story_overlay, story_rect)
            
            # Create clipping region for text
            clip_rect = pygame.Rect(story_rect.left + 40, story_rect.top + 40, 
                                   story_rect.width - 80, story_rect.height - 80)
            self.screen.set_clip(clip_rect)
            
            # Level 17 victory story content
            story_text = [
                "VICTORY!",
                "",
                "Tristan and his party found Gredson preparing to attack Castle Reevin.",
                "Tristan Stopped them right before they attacked.",
                "One of the soldiers told them that they had",
                "another Army heading to get the stone of Tyick.",
                "The Great Sage then appeared and said ",
                "“If Gredson had four of the stones he could bring back dragons!”",
                "Then he told them of a sword by Gredson that could overpower the stones.",
                ""
                "Tristan then heads into the castle and",
                "tells his father about what has happened.",
                "Tristan's father then joins him with a few soldiers to finish",
                "this war and after the sword. They March closer to the final battle!",
                "",
                "Press any key to continue..."
            ]
            
            # Render the story text with scrolling
            lines = story_text
            y_offset = clip_rect.top - self.level17_story_scroll_offset
            max_width = clip_rect.width
            
            for line in lines:
                if line == "VICTORY!":
                    text = pygame.font.SysFont(None, 48).render(line, True, (255, 215, 0))
                elif line == "Press any key to continue...":
                    text = pygame.font.SysFont(None, 24).render(line, True, (255, 255, 200))
                else:
                    text = pygame.font.SysFont(None, 28).render(line, True, (255, 255, 200))
                
                text_rect = text.get_rect(center=(self.viewport_width * self.tile // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 35 if line == "" else 40
            
            # Level 23 victory story overlay
        if self.level23_victory_story_active:
            # Fill entire screen with black background
            s.fill((0, 0, 0))
            
            # Create story overlay
            story_overlay = pygame.Surface((self.viewport_width * self.tile - 80, self.viewport_height * self.tile - 160), pygame.SRCALPHA)
            story_overlay.fill((0, 0, 0, 200))
            story_rect = story_overlay.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2))
            s.blit(story_overlay, story_rect)
            
            # Create clipping region for text
            clip_rect = pygame.Rect(story_rect.left + 40, story_rect.top + 40, 
                                   story_rect.width - 80, story_rect.height - 80)
            s.set_clip(clip_rect)
            
            # Level 23 victory story content - END
            story_text = [
                "END",
                "",
                "Tristan has beaten Rather!",
                "The Dragon Rising has been stopped!",
                "Rather's son Hector becomes king of Gredson.",
                "The five Stones are put back where they",
                "belong along with the great sword.",
                "",
                "Peace spreads throughout Theron.For now.",
                "The Great Sage feels a strange dark magic coming into the near future.",
                "That is not led by the Gredson  but by something else.",
                ""
            ]
            
            # Render story text centered in the middle of the screen
            # Calculate total text height
            total_height = sum(35 if line == "" else 40 for line in story_text[:-1])
            # Start from center minus half the total height
            y_offset = (story_rect.height - total_height) // 2
            for i, line in enumerate(story_text):
                if i < len(story_text) - 1:
                    text = pygame.font.SysFont(None, 28).render(line, True, (255, 255, 200))
                    text_rect = text.get_rect(center=(self.viewport_width * self.tile // 2, story_rect.top + y_offset))
                    s.blit(text, text_rect)
                    y_offset += 35 if line == "" else 40
            
            # Reset clipping
            s.set_clip(None)
        
        # Character epilogue overlay
        if self.character_epilogue_active:
            # Fill entire screen with black background
            s.fill((0, 0, 0))
            
            # Use full screen for text without overlay
            clip_rect = pygame.Rect(40, 40, self.viewport_width * self.tile - 80, self.viewport_height * self.tile - 80)
            s.set_clip(clip_rect)
            
            # Get current character's epilogue
            if self.current_character_index < len(self.surviving_characters):
                current_character = self.surviving_characters[self.current_character_index]
                current_unit = self.surviving_character_objects[self.current_character_index]
                character_name = current_unit.name if current_unit.name else current_character
                
                # Get the base story text
                base_story = self.character_epilogues.get(current_character, [
                    f"{character_name}'S EPILOGUE",
                    "",
                    "This hero's story continues...",
                    ""
                ])
                
                # Update the title to use the character's actual name
                story_text = []
                for line in base_story:
                    if line.endswith("'S EPILOGUE"):
                        story_text.append(f"{character_name.upper()}'S EPILOGUE")
                    else:
                        story_text.append(line)
                
                # Just add the story text without progress or instructions
            else:
                story_text = ["No epilogue available"]
            
            # Render the story text with text wrapping
            wrapped_lines = []
            font_regular = pygame.font.SysFont(None, 28)
            font_title = pygame.font.SysFont(None, 36)
            
            for line in story_text:
                if line.endswith("'S EPILOGUE"):
                    wrapped_lines.append(line)  # Title lines don't wrap
                elif line == "":
                    wrapped_lines.append(line)  # Empty lines stay empty
                else:
                    # Wrap regular text lines
                    max_width = clip_rect.width - 40  # Leave some padding
                    wrapped = self.wrap_text(line, font_regular, max_width)
                    wrapped_lines.extend(wrapped)
            
            # Calculate total text height to center it
            total_height = sum(35 if line == "" else 40 for line in wrapped_lines)
            # Start from center minus half the total height
            y_offset = clip_rect.centery - total_height // 2
            
            for line in wrapped_lines:
                if line.endswith("'S EPILOGUE"):
                    text = font_title.render(line, True, (255, 215, 0))
                else:
                    text = font_regular.render(line, True, (255, 255, 200))
                
                text_rect = text.get_rect(center=(self.viewport_width * self.tile // 2, y_offset))
                s.blit(text, text_rect)
                y_offset += 35 if line == "" else 40
            
            # Reset clipping
            s.set_clip(None)
        
        # Credits overlay
        if self.credits_active:
            # Fill entire screen with black background
            s.fill((0, 0, 0))
            
            # Use full screen for text without overlay
            clip_rect = pygame.Rect(40, 40, self.viewport_width * self.tile - 80, self.viewport_height * self.tile - 80)
            s.set_clip(clip_rect)
            
            # Credits text - extensive like real game credits
            credits_text = [
                "HEROES OF THAREN",
                "",
                "",
                "CREATED BY",
                "",
                "MARK FLEETWOOD",
                "",
                "",
                "GAME DESIGN",
                "",
                "Mark Fleetwood",
                "",
                "",
                "PROGRAMMING",
                "",
                "Mark Fleetwood",
                "",
                "",
                "STORY",
                "",
                "Mark Fleetwood",
                "",
                "",
                "CHARACTER DESIGN",
                "",
                "Mark Fleetwood",
                "",
                "",
                "LEVEL DESIGN",
                "",
                "Mark Fleetwood",
                "",
                "",
                "CHARACTER ART",
                "",
                "Mark Fleetwood",
                "",
                "",
                "BATTLEFIELD ART",
                "",
                "Mark Fleetwood",
                "",
                "",
                "SPECIAL THANKS TO",
                "",
                "Clint Fleetwood",
                "Olivia Fleetwood",
                "",
                "THANK YOU FOR PLAYING",
                "HEROES OF THAREN",
                "",
                "",
                "Press any key to return to title screen..."
            ]
            
            # Render the scrolling credits text
            font_title = pygame.font.SysFont(None, 48)
            font_subtitle = pygame.font.SysFont(None, 36)
            font_regular = pygame.font.SysFont(None, 32)
            font_small = pygame.font.SysFont(None, 24)
            
            # Calculate total text height
            total_height = 60 + sum(35 if line == "" else 40 for line in credits_text[1:])
            
            # Start from bottom of screen and scroll up
            start_y = clip_rect.bottom - 20  # Start closer to visible area
            y_offset = start_y - self.credits_scroll_offset
            
            for line in credits_text:
                # Check if line is visible - use more generous bounds
                if y_offset > clip_rect.top - 100 and y_offset < clip_rect.bottom + 100:
                    if line == "HEROES OF THAREN":
                        text = font_title.render(line, True, (255, 215, 0))
                    elif line in ["PRESENTED BY", "CREATED BY", "GAME DESIGN", "PROGRAMMING", 
                                "STORY & NARRATIVE", "CHARACTER DESIGN", "LEVEL DESIGN", 
                                "CHARACTER ART", "BATTLEFIELD ART", "SOUND DESIGN", 
                                "SPECIAL THANKS TO", "AND TO YOU"]:
                        text = font_subtitle.render(line, True, (200, 200, 255))
                    elif line == "FLEETWOOD GAMES":
                        text = font_subtitle.render(line, True, (255, 215, 0))
                    elif line == "MARK FLEETWOOD":
                        text = font_regular.render(line, True, (255, 255, 255))
                    elif line == "THANK YOU FOR PLAYING!":
                        text = font_subtitle.render(line, True, (255, 255, 200))
                    elif line == "Press any key to return to title screen...":
                        text = font_small.render(line, True, (255, 255, 200))
                    elif line.startswith("Tristan -") or line.startswith("Lusia -") or line.startswith("Wen -"):
                        text = font_regular.render(line, True, (200, 255, 200))
                    else:
                        text = font_regular.render(line, True, (255, 255, 200))
                    
                    text_rect = text.get_rect(center=(self.viewport_width * self.tile // 2, y_offset))
                    s.blit(text, text_rect)
                
                y_offset += 35 if line == "" else 40
            
            # Reset clipping
            s.set_clip(None)
        
        # big victory/defeat text (exclude level 23)
            if self.state.victory and self.state.current_level != 23:
                big_font = pygame.font.SysFont(None, 72)
                victory_text = big_font.render(f"{self.get_level_name()} VICTORY!", True, (255, 215, 0))
                text_rect = victory_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 - 20))
                s.blit(victory_text, text_rect)
                
                sub_font = pygame.font.SysFont(None, 36)
                sub_text = sub_font.render("Advancing to next level...", True, (255, 255, 255))
                sub_rect = sub_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 + 30))
                s.blit(sub_text, sub_rect)
            else:
                # Check if Tristan was defeated for overlay text (exclude level 23)
                if self.state.current_level != 23:
                    tristan_defeated = False
                    for unit in self.state.units:
                        if unit.__class__.__name__ == 'Tristan' and unit.hp <= 0:
                            tristan_defeated = True
                            # Set game over state when Tristan is defeated
                            self.state.game_over = True
                            self.state.victory = False
                            break
                    
                    if tristan_defeated:
                        # Draw defeat screen and stop other drawing
                        big_font = pygame.font.SysFont(None, 96)
                        sub_font = pygame.font.SysFont(None, 48)
                        defeat_text = big_font.render("GAME OVER", True, (200, 50, 50))
                        tristan_text = sub_font.render("Tristan is defeated!", True, (255, 100, 100))
                        text_rect = defeat_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 - 40))
                        tristan_rect = tristan_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 + 20))
                        s.blit(defeat_text, text_rect)
                        s.blit(tristan_text, tristan_rect)
                        # Don't draw anything else when defeated
                        return
                    else:
                        # Generic defeat for other scenarios
                        big_font = pygame.font.SysFont(None, 72)
                        defeat_text = big_font.render("DEFEAT!", True, (200, 50, 50))
                        sub_font = pygame.font.SysFont(None, 36)
                        sub_text = sub_font.render("All units lost...", True, (255, 255, 255))
                        text_rect = defeat_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 - 20))
                        sub_rect = sub_text.get_rect(center=(self.viewport_width * self.tile // 2, self.viewport_height * self.tile // 2 + 30))
                        s.blit(defeat_text, text_rect)
                        s.blit(sub_text, sub_rect)
                        # Don't draw anything else when defeated
                        return
        
        # Always draw status bar last to keep it on top of overlays
        if not self.state.game_over:
            if self.state.current_phase == 'player':
                # Show player unit info if one is selected
                if self.state.selected:
                    u = self.state.selected
                    if hasattr(u, 'level') and u.team == 'player':
                        # Use custom name if available, otherwise use class name
                        unit_name = u.name if u.name else u.__class__.__name__
                        status = f"{self.get_level_name()} | PLAYER PHASE | Selected: {unit_name} Lv.{u.level} @{u.x},{u.y}\nHP: {u.hp}/{u.max_hp}  Moves: {u.moves_remaining}/{u.move}  Attacks: {u.attacks_remaining}/1\nEXP: {u.exp}/{u.exp_to_next_level}  Kills: {u.kills}  ATK: {u.atk}\nPress SPACE to end player phase"
                        if self.enable_scrolling:
                            status += "\nUse Arrow Keys or WASD to scroll battlefield"
                    else:
                        # Use custom name if available, otherwise use class name
                        unit_name = u.name if u.name else u.__class__.__name__
                        status = f"{self.get_level_name()} | PLAYER PHASE | Selected: {unit_name} @{u.x},{u.y}\nMoves: {u.moves_remaining}/{u.move}  Attacks: {u.attacks_remaining}/1\nPress SPACE to end player phase"
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
                if self.state.current_level == 23:
                    status = f"{self.get_level_name()} VICTORY! Game Complete!"
                else:
                    status = f"{self.get_level_name()} VICTORY! Advancing to next level..."
            else:
                # Check if Tristan was defeated
                tristan_defeated = False
                for unit in self.state.units:
                    if unit.__class__.__name__ == 'Tristan' and unit.hp <= 0:
                        tristan_defeated = True
                        break
                
                if tristan_defeated:
                    status = "DEFEAT! Tristan is defeated!"
                else:
                    status = "DEFEAT! Tristan is defeated!"
        else:
            status = "No active unit"
        
        lines = status.strip().split('\n')
        # Calculate needed height for all lines
        status_height = max(60, len(lines) * 20 + 10)  # Minimum 60px, expand based on content
        
        # Position status bar to touch bottom of screen
        screen_height = self.screen.get_height()
        status_bar_rect = pygame.Rect(0, screen_height - status_height, self.viewport_width * self.tile, status_height)
        
        # Clear and fill status bar area with solid black
        pygame.draw.rect(self.screen, (0, 0, 0), status_bar_rect)
        
        # Draw status text lines
        y_offset = status_bar_rect.top + 5
        for line in lines:
            text = self.font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(centerx=status_bar_rect.centerx, y=y_offset)
            self.screen.blit(text, text_rect)
            y_offset += 20

    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
        words = text.split()
        wrapped_lines = []
        current_line = []
        
        for word in words:
            # Test if adding this word would exceed max width
            test_line = ' '.join(current_line + [word])
            text_surface = font.render(test_line, True, (255, 255, 255))
            
            if text_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                # If current line has content, add it to wrapped lines
                if current_line:
                    wrapped_lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Single word is too long, add it anyway
                    wrapped_lines.append(word)
        
        # Add any remaining words
        if current_line:
            wrapped_lines.append(' '.join(current_line))
        
        return wrapped_lines

    def start_character_epilogues(self):
        """Start the character epilogue system after level 23 victory"""
        # Find surviving player characters
        self.surviving_characters = []
        self.surviving_character_objects = []
        
        for unit in self.state.units:
            if unit.team == 'player' and unit.hp > 0:
                character_name = unit.__class__.__name__
                # Special handling for Soldier units to show both Soldier1 and Soldier2 epilogues
                if character_name == 'Soldier':
                    # Check if we've already added soldiers
                    soldier_count = sum(1 for name in self.surviving_characters if name.startswith('Soldier'))
                    if soldier_count == 0:
                        self.surviving_characters.append('Soldier1')
                        self.surviving_character_objects.append(unit)
                    elif soldier_count == 1:
                        self.surviving_characters.append('Soldier2')
                        self.surviving_character_objects.append(unit)
                elif character_name in self.character_epilogues:
                    self.surviving_characters.append(character_name)
                    self.surviving_character_objects.append(unit)
        
        # Define character acquisition order (when they join the party)
        acquisition_order = ['Archer', 'Mage', 'Horse', 'Srodman', 'Knight', 'Horsearcher', 'Healer', 'Ballistician', 'Knig', 'Soldier1', 'Soldier2', 'Great_sage']
        
        # Reorder surviving characters based on acquisition order, but put Tristan last
        ordered_characters = []
        ordered_objects = []
        
        # First, add all characters except Tristan in acquisition order
        for char_name in acquisition_order:
            if char_name != 'Tristan':
                for i, existing_char in enumerate(self.surviving_characters):
                    if existing_char == char_name or (char_name in ['Soldier1', 'Soldier2'] and existing_char == char_name):
                        ordered_characters.append(existing_char)
                        ordered_objects.append(self.surviving_character_objects[i])
                        break
        
        # Add Tristan last if he's alive
        tristan_unit = None
        for unit in self.state.units:
            if unit.__class__.__name__ == 'Tristan' and unit.hp > 0:
                tristan_unit = unit
                break
        
        if tristan_unit:
            ordered_characters.append('Tristan')
            ordered_objects.append(tristan_unit)
        
        # Update the surviving lists with the new order
        self.surviving_characters = ordered_characters
        self.surviving_character_objects = ordered_objects
        
        if self.surviving_characters:
            character_names = [unit.name if unit.name else char_class for unit, char_class in zip(self.surviving_character_objects, self.surviving_characters)]
            print(f"Starting character epilogues for: {', '.join(character_names)}")
            self.current_character_index = 0
            self.character_epilogue_active = True
        else:
            print("No surviving characters found for epilogues")
            self.running = False  # Return to title screen

    def advance_character_epilogue(self):
        """Advance to the next character epilogue or end the game"""
        self.current_character_index += 1
        
        if self.current_character_index >= len(self.surviving_characters):
            # All epilogues shown, start credits
            self.character_epilogue_active = False
            self.credits_active = True
            self.credits_timer = 0.0
            self.credits_duration = 135.0  # Show credits for 135 seconds
            self.credits_scroll_offset = 0.0
            self.credits_scroll_speed = 1.0  # Scroll speed for credits
            
            # Change music to 1.mp3 for credits
            self.music_channel.stop()
            if hasattr(self, 'player_phase_music'):
                try:
                    self.music_channel.play(self.player_phase_music, -1)  # Loop credits music
                    self.music_channel.set_volume(0.4)
                    print("Credits music started")
                except pygame.error as e:
                    print(f"Could not play credits music: {e}")
            
            print("All character epilogues completed. Starting credits.")
        else:
            current_char = self.surviving_characters[self.current_character_index]
            current_unit = self.surviving_character_objects[self.current_character_index]
            display_name = current_unit.name if current_unit.name else current_char
            print(f"Showing epilogue for {display_name}")

    
