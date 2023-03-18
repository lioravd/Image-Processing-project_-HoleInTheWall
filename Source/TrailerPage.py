import pygame
import sys
from Utils.button import Button
from Utils import utilities as utl
import Source.HomePage as HomePage

def menu_trailer(self):

    x, y = self.screen.get_size()

    self.trailer_movie_sound.play()

    self.screen.fill("#B99B6B")

    toStop = False
    text_input = "STOP"
    while True:
        # Get the next frame from the video capture
        # cap = self.cam.get_image()
        # camera_surface = pygame.transform.scale(cap, self.screen.get_size())  # Scale the frame surface to fill the display surface
        # self.screen.blit(camera_surface, (0, 0))

        SCORE_MOUSE_POS = pygame.mouse.get_pos()
        xT, yT = x / 2, y / 10
        text_rect = utl.printInfoText(self, 65, "The Trailer:", (xT, yT), "#251749")

        BACK = Button(image=None, pos=(70, y-50), text_input=text_input, font=utl.get_font(40),
                      base_color="#d7fcd4", hovering_color="Green", shadow_color="#609966")



        # Start playing the video
        for frame in self.trailer_movie.iter_frames():
            if toStop:
                break
            SCORE_MOUSE_POS = pygame.mouse.get_pos()
            # Convert video frame to Pygame surface
            surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            new_width = (x*2)//3
            new_height = (new_width*y) // x
            surface = pygame.transform.scale(surface, (new_width, new_height))
            surface_rect = surface.get_rect(center=(x // 2, y // 2))
            # Blit the surface to the Pygame display surface
            self.screen.blit(surface, surface_rect)

            BACK.changeColor(SCORE_MOUSE_POS)
            BACK.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.trailer_movie_sound.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK.checkForInput(SCORE_MOUSE_POS):
                        text_input = "BACK"
                        toStop = True
                        self.trailer_movie_sound.stop()

            # Update the Pygame display
            pygame.display.flip()
            # Limit the frame rate
            self.clock.tick_busy_loop(self.trailer_movie.fps)

        BACK.changeColor(SCORE_MOUSE_POS)
        BACK.update(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.trailer_movie_sound.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.checkForInput(SCORE_MOUSE_POS):
                    HomePage.main_menu(self)

        pygame.display.update()
