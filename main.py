"""
Shimpei's Platformer - Bora Bora Cave
"""

import arcade
import os
import random

# Allowing main path to be used to access various files
MAIN_PATH = os.path.dirname(os.path.abspath(__file__))

# Game window properties
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Bora Bora Cave"

# Other game window properties, used for determining
# where the center of the screen is
SCREEN_X_CENTER = 800
SCREEN_Y_CENTER = 400

# Constants for camera boundaries
CAMERA_MAX_X = 1200
CAMERA_MAX_Y = 1440

# Scaling numbers for sprites
PLAYER_MAGMA_SCALE = 1
TILE_SCALE = 1.75
SPRITE_PIXEL_SIZE = 32
GAME_BACKGROUND_SCALING = 0.75
MENU_BACKGROUND_SCALING = 0.85
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALE
TILEMAP_HEIGHT = 40
TILEMAP_WIDTH = 50

# Constants for the text, sizes and font
MENU_FONT_SIZE = 120
FONT_SIZE = 32
LICENSE_FONT_SIZE = 18
CHOSEN_FONT = "Kenney Pixel"

# Constants for movement
MOVEMENT_SPEED = 8
GRAVITY = 1
JUMP = 16
MAGMA_FALL_SPEED = 6

# Constants for dash mechanic
DASH_SPEED = 18
SUPER_DASH = 1.75
DASH_DURATION = 1
DASH_DECREASE = 1/12
DASH_COOLDOWN = 10

# Constant for how long the player is invincible for, after dying
INVINCIBILITY_FRAMES = 60

# Constant for increasing the y value of the background 
# (so the player is more centered)
BACKGROUND_RISE = 40

# Constant for how fast the animation plays, larger value means slower
IDLE_ANIMATION_SPEED = 6
WALK_ANIMATION_SPEED = 4
JUMP_FALL_ANIMATION_SPEED = 12
DASH_ANIMATION_SPEED = 1
DEATH_ANIMATION_SPEED = 5
MAGMA_ANIMATION_SPEED = 10

# Constant for how many levels there are in the game
LEVEL_COUNT = 3

# Layer names from the tilemap
LAYER_NAME_PLATFORM = "Platforms"
LAYER_NAME_FOREGROUND = "Foreground"
LAYER_NAME_DONTTOUCH = "Don't Touch"
LAYER_NAME_CHECKPOINT = "Checkpoint"
LAYER_NAME_SUPER = "Super"
LAYER_NAME_FINISH = "Finish"

# Name for the player list containing the player sprites, and the 
# magma list with the magma sprites
PLAYER = "Player"
MAGMA = "Magma"

# Constants that represent how many textures each animation
# and the background has
IDLE_TEXTURE_COUNT = 8
WALK_TEXTURE_COUNT = 6
JUMP_TEXTURE_COUNT = 5
FALL_TEXTURE_COUNT = 4
DASH_TEXTURE_COUNT = 15
DEATH_TEXTURE_COUNT = 10
BACKGROUND_COUNT = 9
MAGMA_COUNT = 2

# Constants for seeing if the player is facing right or left
RIGHT = 0
LEFT = 1

# Starting position for the player for each level
PLAYER_START_X = 80
PLAYER_START_Y = 270

# Constant for controlling how often magma drops are spawned,
# and the range of where they can spawn
MAGMA_TIMER = 40
MAGMA_MAX_SPAWN_X = 50


def load_texture_pair(filename):
    """Loading a texture pair, takes an image and adds it as well as
    the horizontally flipped/mirrored image into a list"""
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

class Player(arcade.Sprite):
    """Player sprite, for animating the player"""

    def __init__(self):
        """Initialization of the player sprites, loading all the 
        textures for the animations"""

        # Inheriting methods from parent class, Sprite
        super().__init__()

        # Set the default state of the player to face right
        self.player_direction = RIGHT

        # Used when changing between the animations
        self.current_texture = 0
        self.scale = PLAYER_MAGMA_SCALE

        # Seeing the state of the player, to see which animations
        # to play
        self.jump = False
        self.walk = False
        self.dash = False

        # For changing the sprites if the player has a super dash
        self.super = 0

        # Loading textures for when the player is idle
        self.idle_textures = []
        self.idle_super_textures = []
        for i in range(IDLE_TEXTURE_COUNT):
            texture = load_texture_pair(f"{MAIN_PATH}/assets/player/\
player_idle/player_idle{i+1}.png")
            self.idle_textures.append(texture)
        for i in range(IDLE_TEXTURE_COUNT):
            texture = load_texture_pair(f"{MAIN_PATH}/assets/player_super\
/player_super_idle/player_super_idle{i+1}.png")
            self.idle_super_textures.append(texture)
        
        # Loading textures for when the player is walking
        self.walk_textures = []
        self.walk_super_textures = []
        for i in range(WALK_TEXTURE_COUNT):
            texture = load_texture_pair(f"{MAIN_PATH}/assets/player\
/player_walk/player_walk{i+1}.png")
            self.walk_textures.append(texture)
        for i in range(WALK_TEXTURE_COUNT):
            texture = load_texture_pair(f"{MAIN_PATH}/assets/\
player_super/player_super_walk/player_super_walk{i+1}.png")
            self.walk_super_textures.append(texture)

        # Loading textures for when the player is jumping (going up)
        self.jump_textures = []
        self.jump_super_textures = []
        for i in range(JUMP_TEXTURE_COUNT):
            texture = load_texture_pair(f"{MAIN_PATH}/assets/player/\
player_jump/player_jump{i+1}.png")
            self.jump_textures.append(texture)
        for i in range(JUMP_TEXTURE_COUNT):
            texture = load_texture_pair(f"{MAIN_PATH}/assets/player_super\
/player_super_jump/player_super_jump{i+1}.png")
            self.jump_super_textures.append(texture)
    
        # Loading textures for when the player is falling
        self.fall_textures = []
        self.fall_super_textures = []
        for i in range(FALL_TEXTURE_COUNT):
            texture = load_texture_pair(f"{MAIN_PATH}/assets/player/\
player_fall/player_fall{i+1}.png")
            self.fall_textures.append(texture)
        for i in range(FALL_TEXTURE_COUNT):
            texture = load_texture_pair(f"{MAIN_PATH}/assets/player_super\
/player_super_fall/player_super_fall{i+1}.png")
            self.fall_super_textures.append(texture)

        # Loading textures for when the player is dashing
        self.dash_textures = []
        self.dash_super_textures = []
        for i in range(DASH_TEXTURE_COUNT):
            texture = load_texture_pair(f"{MAIN_PATH}/assets/player/\
player_dash/player_dash{i+1}.png")
            self.dash_textures.append(texture)
        for i in range(DASH_TEXTURE_COUNT):
            texture = load_texture_pair(f"{MAIN_PATH}/assets/player_super\
/player_super_dash/player_super_dash{i+1}.png")
            self.dash_super_textures.append(texture)
        
        # Loading textures for when the player dies
        self.death_textures = []
        self.death_super_textures = []
        for i in range(DEATH_TEXTURE_COUNT):
            texture = load_texture_pair(f"{MAIN_PATH}/assets/player/\
player_death/player_death{i+1}.png")
            self.death_textures.append(texture)
        for i in range(DEATH_TEXTURE_COUNT):
            texture = load_texture_pair(f"{MAIN_PATH}/assets/player_super\
/player_super_death/player_super_death{i+1}.png")
            self.death_super_textures.append(texture)

        # Setting the initial texture
        # The [0] is for setting the initial texture (when the 
        # game is started), to be the first texture/item
        # in the idle_textues list
        self.texture = self.idle_textures[0][self.player_direction]

        # Setting up dash variables; the direction of the dash, 
        # the duration of the dash, and the cooldown of the dash
        self.dashing = False
        self.dash_direction_x = 0
        self.dash_direction_y = 0
        self.dash_duration = DASH_DURATION
        self.dash_cooldown = 0
        
        # Setting up variable to check if the player is dying or not
        self.dying = False


    def update_animation(self, delta_time):
        """Updating and animating the player sprite"""
        
        # Checking if the player is facing right or 
        # left, and flipping if we need to
        if self.change_x < 0 and self.player_direction == RIGHT:
            self.player_direction = LEFT
        elif self.change_x > 0 and self.player_direction == LEFT:
            self.player_direction = RIGHT

        # Animation for when the player is dying
        if self.dying:
            self.current_texture += 1
            if self.current_texture > DEATH_TEXTURE_COUNT * \
DEATH_ANIMATION_SPEED:
                self.current_texture = 0
            if self.current_texture < DEATH_TEXTURE_COUNT * \
DEATH_ANIMATION_SPEED:
                if self.super == 0:
                    frame = self.current_texture // DEATH_ANIMATION_SPEED
                    self.texture = self.death_textures\
[frame][self.player_direction]
                else:
                    frame = self.current_texture // DEATH_ANIMATION_SPEED
                    self.texture = self.death_super_textures\
[frame][self.player_direction]
            return
                
        # Animation for when the player is dashing
        if self.dashing == True:
            self.current_texture += 1
            if self.current_texture >= DASH_TEXTURE_COUNT * \
DASH_ANIMATION_SPEED:
                self.current_texture = 0
            if self.super == 0:
                frame = self.current_texture // DASH_ANIMATION_SPEED
                self.texture = self.dash_textures\
[frame][self.player_direction]
            else:
                frame = self.current_texture // DASH_ANIMATION_SPEED
                self.texture = self.dash_super_textures\
[frame][self.player_direction]
            return

        # Animation for when the player is idle, plays each 
        # image/frame for however long the animation speed is set to
        if self.change_x == 0 and self.change_y == 0:
            self.current_texture += 1
            if self.current_texture >= IDLE_TEXTURE_COUNT * \
IDLE_ANIMATION_SPEED:
                self.current_texture = 0
            if self.super == 0:
                frame = self.current_texture // IDLE_ANIMATION_SPEED
                self.texture = self.idle_textures\
[frame][self.player_direction]
                return
            else:
                frame = self.current_texture // IDLE_ANIMATION_SPEED
                self.texture = self.idle_super_textures\
[frame][self.player_direction]
                return

        # Animation for when the player is jumping
        if self.change_y > 0 and self.change_x == 0:
            self.current_texture += 1
            if self.current_texture >= JUMP_TEXTURE_COUNT * \
JUMP_FALL_ANIMATION_SPEED:
                self.current_texture = 0
            if self.super == 0:
                frame = self.current_texture // JUMP_FALL_ANIMATION_SPEED
                self.texture = self.jump_textures\
[frame][self.player_direction]
            else:
                frame = self.current_texture // JUMP_FALL_ANIMATION_SPEED
                self.texture = self.jump_super_textures\
[frame][self.player_direction]
            return

        # Animation for when the player is falling
        if self.change_y < 0 and self.change_x == 0:
            self.current_texture += 1
            if self.current_texture >= FALL_TEXTURE_COUNT * \
JUMP_FALL_ANIMATION_SPEED:
                self.current_texture = 0
            if self.super == 0:
                frame = self.current_texture // JUMP_FALL_ANIMATION_SPEED
                self.texture = self.fall_textures\
[frame][self.player_direction]
            else:
                frame = self.current_texture // JUMP_FALL_ANIMATION_SPEED
                self.texture = self.fall_super_textures\
[frame][self.player_direction]
            return

        # Animation for when the player is walking
        self.current_texture += 1
        if self.current_texture >= WALK_TEXTURE_COUNT * WALK_ANIMATION_SPEED:
            self.current_texture = 0
        if self.super == 0:
            frame = self.current_texture // WALK_ANIMATION_SPEED
            self.texture = self.walk_textures[frame][self.player_direction]
        else:
            frame = self.current_texture // WALK_ANIMATION_SPEED 
            self.texture = self.walk_super_textures\
[frame][self.player_direction]
            
    
    def dash_mechanic(self, direction_x, direction_y):
        """Initiating the dash mechanic, 
        setting x and y direction of the dash"""

        # If the player is not dashing currently, 
        # set the state of the dash to True, reset the current
        # texture of the player, set the change_y to 0 (so they move
        # in a straight line when gravity set to 0), and 
        # determine dash direction
        if not self.dashing:
            self.dashing = True
            self.change_y = 0
            self.current_texture = 0
            self.dash_direction_x = direction_x
            self.dash_direction_y = direction_y
        # Resetting the duration of the dash
        self.dash_duration = DASH_DURATION
        # Returning false, so the player can only dash once in the air
        # and the player cannot dash again in the air until
        # they hit the ground
        return False


    def on_update(self, delta_time):
        """Updating the animations of the 
        player and the dash mechanic"""

        # Checking if the player is dashing, and dashing the 
        # player with the multiplied movement speed in the direction
        # Setting the cooldown of the dash to the dash cooldown
        # constant, so when the player finishes dashing, the
        # self.dash_cooldown variable has the same value as the
        # dash cooldown constant
        if self.dashing:
            self.dash_cooldown = DASH_COOLDOWN
            if self.super == 0:
                self.center_x += DASH_SPEED * self.dash_direction_x
                self.center_y += DASH_SPEED * self.dash_direction_y
            elif self.super != 0:
                self.center_x += DASH_SPEED * \
self.dash_direction_x * SUPER_DASH
                self.center_y += DASH_SPEED * \
self.dash_direction_y * SUPER_DASH
            # Decreasing the duration of the dash until it reaches
            # zero, and the player is no longer dashing, 
            # resetting the super state of player
            self.dash_duration -= DASH_DECREASE
            if self.dash_duration <= 0:
                self.dashing = False
                self.super = 0

        # Call the update_animation method to handle 
        # animation and flipping
        self.update_animation(delta_time)


class MagmaDrop(arcade.Sprite):
    """Class for the magma drops, animations"""

    def __init__(self):
        """Initializing the magma drops, loading the textures and
        determining the spawn point of the magma drops"""

        # Inheriting methods from parent class, Sprite
        super().__init__()

        # For the animation of the magma drop, and 
        # the scaling of the magma drops
        self.current_texture = 0
        self.textures = []
        self.scale = PLAYER_MAGMA_SCALE

        # Loading the textures for the magma animation
        texture = arcade.load_texture(f"{MAIN_PATH}/assets/magma/magma1.png")
        self.textures.append(texture)
        texture = arcade.load_texture(f"{MAIN_PATH}/assets/magma/magma2.png")
        self.textures.append(texture)

        # Setting the spawnpoints of the magma drops
        self.spawn = [random.randint\
(0, GRID_PIXEL_SIZE * MAGMA_MAX_SPAWN_X), GRID_PIXEL_SIZE * TILEMAP_HEIGHT]


    def on_update(self, delta_time):
        """Updating the sprites for animation of the magma
        drop, and making the magma drop fall"""

        # Animation for the magma drop as it falls
        self.current_texture += 1
        if self.current_texture >= MAGMA_COUNT * MAGMA_ANIMATION_SPEED:
            self.current_texture = 0
        frame = self.current_texture // MAGMA_ANIMATION_SPEED
        self.texture = self.textures[frame]

        # Bringing the magma drop down at the set speed
        self.center_y -= MAGMA_FALL_SPEED

        # Once the magma drop reaches a specific height, 
        # remove from the spritelist, for performance purposes
        # Number -50 represents the y coordinate the magma drop has
        # to pass to be removed from the spritelist
        if self.center_y < -50:
            self.remove_from_sprite_lists()


class MainMenu(arcade.View):
    """Class for the main menu view"""

    def on_show_view(self):
        """Called when the view is changed to the main menu, 
        loading all of the sprites/textures, texts, and 
        music for the main menu"""

        # Loading the music for the main menu
        self.menu_music = arcade.load_sound(f"{MAIN_PATH}/\
assets/menu_music.mp3")

        # Setting up for background, and spritelist containing
        # the background layers
        self.background = None
        self.background_list = arcade.SpriteList()

        # Loading all of the background sprites, and adding them
        # to a spritelist, so they can be drawn
        for i in range(BACKGROUND_COUNT):
            self.background = arcade.Sprite(f"{MAIN_PATH}/assets/\
background/background{i+1}.png", MENU_BACKGROUND_SCALING)
            self.background.center_x = SCREEN_X_CENTER
            self.background.center_y = SCREEN_Y_CENTER
            self.background_list.append(self.background)

        # Adding text on the main menu view, for the title of the
        # game, click to play text, and the licensing for the
        # background assets
        # Coordinates left as numbers, as they are specific,
        # and unique to each text
        # Text is also left as string, as they are also
        # specific and unique
        self.title_text = arcade.Text("Bora Bora Cave", 400, 400, \
arcade.color.BLACK, MENU_FONT_SIZE, font_name = CHOSEN_FONT, bold = True)
        self.click_play_text = arcade.Text("Click Anywhere To Play", \
650, 340, arcade.color.BLACK, FONT_SIZE, font_name = CHOSEN_FONT)
        self.license_text_1 = arcade.Text("Background assets created by \
SlashDashGamesStudio, art made by Seetyaji - \
https://slashdashgamesstudio.itch.io/cave-background-assets", 100, 60, \
arcade.color.WHITE, LICENSE_FONT_SIZE, font_name = CHOSEN_FONT)
        self.license_text_2 = arcade.Text("License - Creative Commons \
Attribution v4.0 International" , 614, 30, arcade.color.WHITE, \
LICENSE_FONT_SIZE, font_name = CHOSEN_FONT)

        # Playing the main menu music, on loop
        # The 0.3 represents the volume of the menu music
        self.current_music = arcade.play_sound(self.menu_music, \
0.3, looping = True)


    def on_draw(self):
        """Drawing the main menu view on the window"""
        
        # Clearing the view, then drawing the main menu view
        self.clear()
        self.background_list.draw(pixelated=True)
        # Drawing the title text, instruction to start
        # playing (click), and licensing for the 
        # background assets
        self.title_text.draw()
        self.click_play_text.draw()
        self.license_text_1.draw()
        self.license_text_2.draw()

    
    def on_mouse_press(self, x, y, button, modifiers):
        """Running the actual game class if the screen is clicked
        when on the main menu view"""

        # Showing the MyGame view, drawing over the main menu view
        # but only if the view was left clicked, and stopping the
        # main menu music
        if button == arcade.MOUSE_BUTTON_LEFT:
            arcade.stop_sound(self.current_music)
            self.window.show_view(MyGame())


class EndScreen(arcade.View):
    """Class for the end screen view"""

    def on_show_view(self):
        """Called when the view is changed to the end screen, 
        and loading all of the sprites and the music for the screen"""

        # Resetting the position of the camera when
        # the end screen is called
        self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        # Loading the music for the end screen (same as the main menu)
        self.end_music = arcade.load_sound(f"{MAIN_PATH}/\
assets/menu_music.mp3")

        # Setting up for background, and spritelist containing
        # the background layers
        self.background = None
        self.background_list = arcade.SpriteList()

        # Loading all of the background sprites, and adding them
        # to a spritelist, so they can be drawn
        for i in range(BACKGROUND_COUNT):
            self.background = arcade.Sprite(f"{MAIN_PATH}/assets/\
background/background{i+1}.png", MENU_BACKGROUND_SCALING)
            self.background.center_x = SCREEN_X_CENTER
            self.background.center_y = SCREEN_Y_CENTER
            self.background_list.append(self.background)

        # Adding text on the end screen view, for telling the player
        # that they have completed the game, click to play again, and
        # press escape to quit
        # Coordinates left as numbers, as they are specific,
        # and unique to each text
        # Text is also left as string, as they are also
        # specific and unique
        self.win_text = arcade.Text("You Win!", 600, 400, \
arcade.color.BLACK, MENU_FONT_SIZE, font_name = CHOSEN_FONT, bold = True)
        self.click_replay_text = arcade.Text("Click To Play Again", \
670, 340, arcade.color.BLACK, FONT_SIZE, font_name = CHOSEN_FONT)
        self.escape_quit_text = arcade.Text("Press Escape To Quit", \
660, 300, arcade.color.BLACK, FONT_SIZE, font_name = CHOSEN_FONT)
        self.license_text_1 = arcade.Text("Background assets created by \
SlashDashGamesStudio, art made by Seetyaji - \
https://slashdashgamesstudio.itch.io/cave-background-assets", 100, 60, \
arcade.color.WHITE, LICENSE_FONT_SIZE, font_name = CHOSEN_FONT)
        self.license_text_2 = arcade.Text("License - Creative Commons \
Attribution v4.0 International" , 614, 30, arcade.color.WHITE, \
LICENSE_FONT_SIZE, font_name = CHOSEN_FONT)

        # Playing the end screen music, on loop
        # The 0.3 represents the volume of the end screen music
        self.current_music = arcade.play_sound(self.end_music, \
0.3, looping = True)


    def on_draw(self):
        """Drawing the main menu view on the window"""
        
        # Clearing the view, then drawing the end screen view
        self.clear()
        self.background_list.draw(pixelated=True)
        # Drawing the you win text, instruction for replaying
        # the game, and for closing the game, and licensing
        # for the background assets
        self.win_text.draw()
        self.click_replay_text.draw()
        self.escape_quit_text.draw()
        self.license_text_1.draw()
        self.license_text_2.draw()

    
    def on_mouse_press(self, x, y, button, modifiers):
        """Running the actual game class if the screen is clicked
        when on the end screen view"""

        # Showing the MyGame view, drawing over the end screen view
        # but only if the view was left clicked, and stopping the
        # end screen music
        if button == arcade.MOUSE_BUTTON_LEFT:
            arcade.stop_sound(self.current_music)
            self.window.show_view(MyGame())

    def on_key_press(self, key, modifiers):
        """Quitting the program if the player presses the escape key
        when on the end screen view"""

        # Closing the program when escape is pressed
        if key == arcade.key.ESCAPE:
            arcade.close_window()


class MyGame(arcade.View):
    """Main class for the game"""

    def __init__(self):
        """Initializing the game, run when the class is called"""

        # Inheriting from parent class, View
        super().__init__()

        # Setting up the scene variable, 
        # storing sprites and spritelists
        self.scene = None

        # Setting the starting level to be 1
        self.level = 1

        # Setting up the player sprite and magma sprite
        self.player_sprite = None
        self.magma_sprite = None

        # Setting up the physics engine for the game, and when you dash
        self.physics_engine = None
        self.dash_physics_engine = None

        # Setting up a camera that follows the player
        self.camera = None

        # Tracking which key is currently pressed, 
        # and if the jump needs to be reset
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.jump_needs_reset = False
    
        # Setting up the tilemap
        self.tile_map = None

        # Loading the music for the game
        self.level_music = arcade.load_sound(f"{MAIN_PATH}\
/assets/level_music.mp3")
        
        # Loading the audio when hitting a checkpoint
        self.checkpoint_audio = arcade.load_sound(f"{MAIN_PATH}/assets\
/checkpoint.mp3")

        # For tracking if the checkpoint audio has been played or not
        self.checkpoint_audio_played = False

        # Variable to store the last checkpoint the player has hit
        self.checkpoint = None

        # Setting variables for the creation of multiple magma drops
        self.new_magma = False
        self.new_magma_counter = MAGMA_TIMER

    def setup(self):
        """Setting up the game, maps, etc."""
        
        # Setting up the camera
        self.camera = arcade.Camera(self.window.width, self.window.height)

        # Checking if the player is dashing in the air, and not 
        # allowing them to dash again until they hit the ground
        self.dash_air = 0

        # Checking if the player has reached the end of the level,
        # and resetting it to zero if they have
        self.finish = 0

        # List to allow for the spawnpoint of the player to
        # change if they hit a checkpoint
        self.spawnpoint = [PLAYER_START_X, PLAYER_START_Y]

        # Setting up the background sprites and spritelist, for every
        # level so the parallax effect works as intended
        self.background = None
        self.background_list = arcade.SpriteList()

        # Starting the music, and setting the current_music variable
        # to it so the music can be restarted between levels
        # The value of 0.3 represents the volume of the level music
        self.current_music = arcade.play_sound(self.level_music\
, 0.3, looping=True)

        # Setting the invincibility frames of the player to
        # on initialization
        self.i_frames = 0

        # Name of tiled map that is being loaded
        map_name = f"{MAIN_PATH}/maps/map{self.level}.tmx"

        # Name of the layers in the tilemap, and setting 
        # spatial hash to true if required
        layer_options = {
            LAYER_NAME_PLATFORM: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_DONTTOUCH: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_CHECKPOINT: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_SUPER: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_FINISH: {
                "use_spatial_hash": True,
            },
        }

        # Loading in the specified map
        self.tile_map = arcade.load_tilemap\
(map_name, TILE_SCALE, layer_options)

        # Initializing the scene with the specified tilemap
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Creating the lists which will contain the various 
        # player sprites, and magma sprites
        self.scene.add_sprite_list(PLAYER)
        self.scene.add_sprite_list(MAGMA)

        # Setting up the player sprite, at the 
        # specified starting coordinates
        # The [0] and [1] used are for the index of the spawnpoint
        # list and, since the spawnpoint list is in the form of
        # [x coordinate, y coordinate], usage of the index number
        # allows for the x and y of the player to be set to the
        # x and y of the designated spawnpoint
        self.player_sprite = Player()
        self.player_sprite.center_x = self.spawnpoint[0]
        self.player_sprite.center_y = self.spawnpoint[1]
        self.scene.add_sprite(PLAYER, self.player_sprite)

        # Adds the player spritelist before the foreground layer, so
        # the foreground layer appears on top/in front of the player
        self.scene.add_sprite_list_before(PLAYER, LAYER_NAME_FOREGROUND)

        # Creating the first initial magma drop
        # The same thing as the player sprite, the [0] and [1]
        # are for the index number and item in the spawn list
        # and setting the x and y of the magma 
        # drop to those coordinates
        self.magma_sprite = MagmaDrop()
        self.magma_sprite.center_x = self.magma_sprite.spawn[0]
        self.magma_sprite.center_y = self.magma_sprite.spawn[1]
        self.scene.add_sprite(MAGMA, self.magma_sprite)

        # Adding the background sprites into the background 
        # spritelist, with the second one being connected 
        # (to the right) of the first one
        for i in range(BACKGROUND_COUNT):
            self.background = arcade.Sprite(f"{MAIN_PATH}/\
assets/background/background{i+1}.png", GAME_BACKGROUND_SCALING)
            self.background.left = 0
            self.background.center_x = (SCREEN_X_CENTER)
            self.background.center_y = (SCREEN_Y_CENTER)\
 + BACKGROUND_RISE
            self.background_list.append(self.background)

            self.background = arcade.Sprite(f"{MAIN_PATH}/\
assets/background/background{i+1}.png", GAME_BACKGROUND_SCALING)
            self.background.left = self.background.width
            self.background.center_x = (SCREEN_X_CENTER)
            self.background.center_y = (SCREEN_Y_CENTER)\
 + BACKGROUND_RISE
            self.background_list.append(self.background)

        # Adding the text for the explanations of keys and
        # the super mechanic
        # Coordinates are left as numbers as they are specific and
        # location of each text is unique
        # The actual text itself is also left as strings as they are
        # are also specific, for each block of text
        self.ad_move_draw = arcade.Text("To move left and right", 460, 380, \
arcade.color.BLACK, FONT_SIZE, font_name = CHOSEN_FONT)
        self.w_move_draw = arcade.Text("To jump", 1080, 380, \
arcade.color.BLACK, FONT_SIZE, font_name = CHOSEN_FONT)
        self.l_move_draw = arcade.Text(\
"To dash in the direction you are holding", 1860, 440, arcade.color.BLACK, \
FONT_SIZE, font_name = CHOSEN_FONT)
        self.super_draw = arcade.Text(\
"Touch this orb to obtain a super dash", 200, 400, arcade.color.BLACK, \
FONT_SIZE, font_name = CHOSEN_FONT)

        # Implementing platformer physics engine from arcade module
        self.physics_engine = arcade.PhysicsEnginePlatformer(\
self.player_sprite, gravity_constant = GRAVITY, \
walls = self.scene[LAYER_NAME_PLATFORM])


    def on_key_press(self, key, modifiers):
        """Called when a key is pressed, updating the 
        state of the pressed direction"""
        
        # When key is pressed, update the state of key press direction
        # to true and run update player speed method, and don't
        # allow the player to move when they are already dashing
        if key == arcade.key.W:
            if not self.player_sprite.dashing and not \
self.player_sprite.dying:
                self.up_pressed = True
                self.update_player_speed()
        elif key == arcade.key.A:
            if not self.player_sprite.dashing and not \
self.player_sprite.dying:
                self.left_pressed = True
                self.update_player_speed()
        elif key == arcade.key.D:
            if not self.player_sprite.dashing and not \
self.player_sprite.dying:
                self.right_pressed = True
                self.update_player_speed()

        # "Dashes" the player in the moving direction 
        # when the player hits 'L'
        if key == arcade.key.L:
            if not self.player_sprite.dying:
                # Only allowing the player to dash once in the air
                # and only if the cooldown of the dash has refreshed
                if self.dash_air and self.player_sprite.dash_cooldown <= 0:
                    # Implementing dash physics engine, 
                    # which has no gravity
                    # (shown by the gravity constant = 0)
                    self.dash_physics_engine = arcade.PhysicsEnginePlatformer\
(self.player_sprite, gravity_constant = 0, \
walls = self.scene[LAYER_NAME_PLATFORM])
                    # Determining the direction of the dash depending
                    # on the state of the key press directions
                    # Numbers of 1 and -1 show if the player should
                    # move to the left or right, and if 0, don't move
                    # in that axis at all
                    if self.right_pressed:
                        direction_x = 1
                    elif self.left_pressed:
                        direction_x = -1
                    else:
                        direction_x = 0
                    if self.up_pressed:
                        direction_y = 1
                    else: 
                        direction_y = 0
                    
                    # Only initiating the dash mechanic if the player
                    # is holding a direction, not if they are 
                    # standing still
                    if direction_x == 0 and direction_y == 0:
                        pass
                    else:
                        self.dash_air = self.player_sprite.dash_mechanic\
(direction_x, direction_y)
                
    
    def on_key_release(self, key, modifiers):
        """Called when the pressed key is released, 
        updating the state of the released direction"""
        
        # When the pressed key is released, update the state of the
        # key press direction to false and run 
        # update player speed method
        if key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False

        self.update_player_speed()

        
    def update_player_speed(self):
        """Moving the player, allowing for opposite directions
        to be pressed at the same time"""

        # Changing the x and y value of the player by the defined
        # movement speed constant, and allowing opposite directions
        # to be pressed at once, when one is released continue to
        # move in the direction which is being held
        self.player_sprite.change_x = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED
        else: 
            self.player_sprite.change_x = 0
        if self.up_pressed:
            if self.physics_engine.can_jump()\
                 and not self.jump_needs_reset:
                self.player_sprite.change_y = JUMP
                

    def center_camera_to_player(self):
        """Centering the game camera to the player"""
        
        # Setting the center of the screen to be the player
        screen_center_x = self.player_sprite.center_x - \
(SCREEN_X_CENTER)
        screen_center_y = self.player_sprite.center_y - \
(SCREEN_Y_CENTER)

        # Stop the screen from moving once the player 
        # reaches the edges of the map
        if screen_center_x < 0:
            screen_center_x = 0
        elif screen_center_x > CAMERA_MAX_X:
            screen_center_x = CAMERA_MAX_X
        if screen_center_y < 0:
            screen_center_y = 0
        elif screen_center_y > CAMERA_MAX_Y:
            screen_center_y = CAMERA_MAX_Y
        player_centered = screen_center_x, screen_center_y

        # Move the camera so the player is in the center
        # 1 represents the speed of which the camera moves (instant)
        self.camera.move_to(player_centered, 1)


    def on_update(self, delta_time):
        """Game Logic, checking for collisions with various layers,
        and updating player sprites and physics engines"""
        
        # Position the camera
        self.center_camera_to_player()

        # Implementing the parallax effect, changing the x and y 
        # values of the background sprites relative to the camera
        # The [0] and [1] again used for the index, as .position
        # returns a list in the form of [x coord, y coord], thus
        # allowing for the background position to change accordingly
        background_x = self.camera.position[0]
        background_y = self.camera.position[1] + \
(SCREEN_Y_CENTER)
        for count, sprite in enumerate(self.background_list):
            # Checking the layer number of the background, 
            # determining if the sprite is the one on the left or
            # right, offsetting the sprite 
            # (less if further/higher layer number)
            # The 2 used when determining the frame variable is for
            # checking if that background layer is on the left or
            # right as left would return a 0 value, while right
            # would return 1
            # The numbers determining the offset variable are used
            # for determining the varying speeds of the background
            # layers, to create the parallax effect, with further
            # layers being slower
            frame = count % 2
            offset = background_x / (1.2 ** (count + 1))
            final_offset = offset + (frame) * sprite.width
            sprite.left = final_offset
            # Setting the y value of the background sprite to
            # follow the camera, ensuring the background
            # doesn't move vertically
            sprite.center_y = background_y

        # Checking if the player has reached the end of the level
        if arcade.check_for_collision_with_list(self.player_sprite\
, self.scene[LAYER_NAME_FINISH]):
            if not self.player_sprite.dying:
                self.finish += 1

        # Updating the game and physics engine for player
        # movement, if the player is dashing then set the gravity to 0
        if self.player_sprite.dashing:
            self.dash_physics_engine.update()
        else:
            self.physics_engine.update()

        # Updating the player sprites, for the animations,
        # flipping of sprites, and dashing
        self.player_sprite.on_update(delta_time)

        # Calling the on_update method for all of the magma drops
        # that exist in the magma spritelist
        for item in self.scene[MAGMA]:
            item.on_update(delta_time)

        # Checking for collision with the edges of the screen,
        # if player does collide, don't let them go past
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > (GRID_PIXEL_SIZE * TILEMAP_WIDTH):
            self.player_sprite.right = (GRID_PIXEL_SIZE * TILEMAP_WIDTH)
        if self.player_sprite.top > (GRID_PIXEL_SIZE * TILEMAP_HEIGHT):
            self.player_sprite.top = (GRID_PIXEL_SIZE * TILEMAP_HEIGHT)

        # Decreasing the dash cooldown of the player
        self.player_sprite.dash_cooldown -= 1

        # Checking if the player is on the ground, and if they are,
        # reset the dash, so they can dash once in the air again, 
        # but only if the cooldown of the dash has reset
        if self.physics_engine.can_jump() and \
self.player_sprite.dash_cooldown <= 0:
            self.dash_air = True

        # Checking for collision with the super layer,
        # giving the player a super dash
        if arcade.check_for_collision_with_list(self.player_sprite\
, self.scene[LAYER_NAME_SUPER]):
            self.player_sprite.super += 1

        # Checking for collision with spikes (dont touch layer), and
        # setting the state of the dying variable 
        # in the player sprite to true
        if arcade.check_for_collision_with_lists(self.player_sprite, \
[self.scene[LAYER_NAME_DONTTOUCH], self.scene[MAGMA]])\
and not self.player_sprite.dying:
            # Only counting the death if the 
            # invincibility frames of the player is 0
            if self.i_frames < 0:
                self.player_sprite.dying = True
                self.player_sprite.dashing = False
                self.player_sprite.current_texture = 0
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0

        # Checking if the player sprite dying variable is set to
        # true, and if it is, and the death animation is finished,
        # respawn the player and reset their invincibility frames
        # Again, with the [0] and [1], as the spawnpoint list is in
        # the format of [x, y], allows for the x and y of the player
        # to be set to the specified coordinates
        if self.player_sprite.dying:
            if self.player_sprite.current_texture == DEATH_TEXTURE_COUNT * \
DEATH_ANIMATION_SPEED:
                self.player_sprite.dying = False
                self.player_sprite.super = 0
                self.player_sprite.center_x = self.spawnpoint[0]
                self.player_sprite.center_y = self.spawnpoint[1]
                self.checkpoint_audio_played = True
                self.i_frames = INVINCIBILITY_FRAMES

        # Decreasing the invincibility frames of the player
        self.i_frames -= 1

        # Checking for collision with the checkpoint layer
        checkpoints = arcade.check_for_collision_with_list(\
self.player_sprite, self.scene[LAYER_NAME_CHECKPOINT])
        # If there was a collision with the checkpoint layer,
        # get position and set new spawnpoint, only if the player
        # was not in the death animation
        # The [0] is used in checkpoints[0].position as the 
        # check_for_collision_with_list returns a list, so the [0]
        # allows the code to get the position
        # of the checkpoint/collision
        # Again, since .position returns a list in the format [x, y]
        # [0] and [1] are used to get the x and y coordinate of the
        # collided checkpoint, to assign to the spawnpoint list
        if checkpoints:
            if not self.player_sprite.dying:
                self.checkpoint = checkpoints[0].position
                self.spawnpoint = [self.checkpoint[0], self.checkpoint[1]]
                # Checking if the checkpoint audio has already been
                # played for the collision, and if not then playing the
                # audio
                # The 0.1 represent the volume of the checkpoint audio
                if not self.checkpoint_audio_played:
                    arcade.play_sound(self.checkpoint_audio, 0.1)
                    self.checkpoint_audio_played = True
        # Resetting the state of the checkpoint audio being played
        # when the player is no longer in collision with the
        # checkpoint layer
        if not checkpoints:
            self.checkpoint_audio_played = False

        # Decreasing the timer of the magma counter, and if it
        # reaches zero, ie. a new magma drop is to be created,
        # set new_magma to true
        self.new_magma_counter -= 1
        if self.new_magma_counter == 0:
            self.new_magma = True

        # Creating new magma sprites, at the random x coordinates,
        # and resetting the new magma variables
        # [0] and [1] used as magma_sprite.spawn list is in the
        # format [x, y], thus allows the x and y of the magma drop
        # to be set accordingly
        if self.new_magma:
            self.magma_sprite = MagmaDrop()
            self.magma_sprite.center_x = self.magma_sprite.spawn[0]
            self.magma_sprite.center_y = self.magma_sprite.spawn[1]
            self.scene.add_sprite(MAGMA, self.magma_sprite)
            self.new_magma_counter = MAGMA_TIMER
            self.new_magma = False

        # Checking if the player has reached the finish line for
        # the level, and increasing the level number by 1 if they have
        # unless they are on the last level, in which the end screen
        # view will be called
        if self.finish != 0:
            # Stopping the background music,
            # so it is restarted between levels
            arcade.stop_sound(self.current_music)
            # Removing all of the sprites from the background_list
            # when transitioning between levels, for performance
            # purposes
            self.background_list = None
            if self.level == LEVEL_COUNT:
                self.window.show_view(EndScreen())
            else:
                self.level += 1
                # Loading the new level
                self.setup()


    def on_show_view(self):
        """Called when the view is changed to the game,
        running the setup method"""
        
        self.setup()


    def on_draw(self):
        """Drawing the screen on the window"""

        # Clearing the screen
        self.clear()

        # Drawing parallax background
        self.background_list.draw(pixelated=True)

        # Drawing the scene, pixelated=true for higher quality map
        self.scene.draw(pixelated=True)

        # Drawing the explanation text of the movement keys if the
        # player is on the first level, and explanation of the super
        # orb if the player is on the second level, using 1 and 2
        # for checking the current level
        if self.level == 1:
            self.ad_move_draw.draw()
            self.w_move_draw.draw()
            self.l_move_draw.draw()
        elif self.level == 2:
            self.super_draw.draw()

        # Activating and using the camera
        self.camera.use()


def main():
    """Main function, called to start the game"""

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(MainMenu())
    arcade.run()

# Running the main function if the program is run directly
if __name__ == "__main__":
    main()