import os, random
import pygame
import Utils.utilities as utl
from Utils import countdown
from Source.ScorePage import menu_score


def StartGame(self):
    (screen_width, screen_height) = self.screen.get_size()

    # Create a surface for the image
    image_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

    # ~~~~~~~ Load the wall
    wall = pygame.image.load(self.paths["wallBackground"])
    transparency = 200              # Set the transparency value (0-255)
    wall.set_alpha(transparency)    # Set the alpha value of the image

    # ~~~~~~ Load all mask
    self.currentPlayer.initWallsOfLevel(self.paths["wallsImages"])
    self.currentPlayer.speedDim = self.levelSpeed[self.currentPlayer.level]

    # ~~~~~~~ Countdown
    self.sound_background.stop()
    countdown.playCountdown(self) # FIXME - remove comment
    self.game_background.play(loops=-1)

    # Run the game loop
    temp_score = 0
    self.currentPlayer.counter_success = 0
    not_lose = True
    while not_lose and not(self.currentPlayer.maskImagesIsEmpty()):
        # ~~~~~~~~ Load the mask image
        mask_image = getWallOfLevel(self)

        # ~~~~~~ Create a surface for the shape
        wall_surface = pygame.transform.scale(wall, mask_image.get_size())
        wall_surface.set_colorkey((0, 0, 0, 0))
        wall_surface.blit(mask_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Init values
        x = screen_width / 2 - mask_image.get_width() / 2
        y = 50 #screen_height - mask_image.get_height() / 2 - 30  # mask_image.get_height()/2
        (w, h) = wall_surface.get_size()

        running = True
        while running:
            self.clock.tick(60)

            # Capture a frame from the camera
            cap = self.cam.get_image()
            self.camera_surface = pygame.transform.scale(cap, self.screen.get_size())

            # Update Position
            x, y, w, h = getNewPos(self, x, y, w, h)

            # Check if the wall has reached the maximum size
            if x + w >= screen_width or y + h >= screen_height:
                running = False

            wall_scaled = pygame.transform.smoothscale(wall_surface, (w, h))

            image_surface.blit(self.camera_surface, (0, 0))  # Blit the camera surface onto the image surface
            image_surface.blit(wall_scaled, (x, y))  # Blit the shape onto the image surface
            self.screen.blit(image_surface, (0, 0))  # Blit the image surface onto the screen

            # Score Panel
            utl.printTextWithShadow(self, 40, 10, 0, f"Score: {self.currentPlayer.score}")
            utl.printTextWithShadow(self, 40, screen_width - 140, 0, f"Life: {self.currentPlayer.life}")
            utl.printTextWithShadow(self, 40, screen_width / 2 - 70, 0, f"Level: {self.currentPlayer.level}")

            # added score
            if self.addedScore_alpha > 0:
                # Update the added score value
                self.addedScore_alpha -= self.addedScore_speed
                if self.addedScore_alpha <= 0:
                    self.addedScore_alpha = 0

                # Draw the screen
                self.addedScore.set_alpha(self.addedScore_alpha)
                self.screen.blit(self.addedScore, self.addedScore_pos)

            # Update the display
            pygame.display.update()

            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    not_lose = False

        temp_score = self.passWallRecognition(self.camera_surface, mask_image, [x, y, w, h])

        if (self.currentPlayer.life == 0):
            not_lose = False

    gameOver(self)




def getNewPos(self, x, y, w, h):
    if self.currentPlayer.counter_success >= self.maxLimitToNextLevel:
        self.currentPlayer.counter_success = 0
        self.currentPlayer.speedDim["dw"] += 0.2
        self.currentPlayer.speedDim["dh"] += 0.2

    currentSpeedDims = self.currentPlayer.speedDim
    x -= currentSpeedDims["dw"] / 2
    y += currentSpeedDims["dy"]
    w += currentSpeedDims["dw"]
    h += currentSpeedDims["dh"]
    return x, y, w, h

def getWallOfLevel(self):
    next_mask_path = self.currentPlayer.getNextMaskPath()
    mask_image = pygame.image.load(next_mask_path).convert_alpha()
    mask_image = pygame.transform.scale(mask_image, (self.screen.get_width() / 2, self.screen.get_height() / 2))
    return mask_image

def gameOver(self):
    self.game_background.stop()

    # Load sound
    if (self.currentPlayer.life == 0):
        game_over_sound = pygame.mixer.Sound("../sounds/sad-trombone.wav")
    else:
        game_over_sound = pygame.mixer.Sound("../sounds/mixkit-game-over.wav")

    # Start the countdown
    self.sound_background.stop()
    game_over_sound.play()
    # Draw the "Game Over" title
    utl.printGradientColotedText(self, 160, "Game Over", (self.screen.get_width() / 2, self.screen.get_height() / 2 - 50))
    utl.printGradientColotedText(self, 95, f"Score: {self.currentPlayer.score}", (self.screen.get_width() / 2, self.screen.get_height() / 2 + 100))

    # Update the display
    pygame.display.update()

    # Wait for 2 second
    pygame.time.wait(4000)

    game_over_sound.stop()
    self.insertPlayerScore()

    self.currentPlayer = None
    menu_score(self)
