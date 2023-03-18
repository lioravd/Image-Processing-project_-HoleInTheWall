import pygame
import sys
import operator

from Utils.button import Button
from Utils import utilities as utl
from Utils import confetti as c
import Source.HomePage as HomePage


def menu_score(self):
    # Sort the score board by the score (highest to lowest)
    self.scoreTable.sort(key=operator.itemgetter(1), reverse=True)

    x, y = self.screen.get_size()
    # Load sound
    audience = pygame.mixer.Sound("../sounds/mixkit-girls-audience-applause-510.wav")

    # Start the countdown
    audience.play()
    confetti = c.PlayConfetti(self.screen, 1000)
    while True:
        # Get the next frame from the video capture
        cap = self.cam.get_image()
        camera_surface = pygame.transform.scale(cap, self.screen.get_size())

        self.screen.blit(camera_surface, (0, 0))
        confetti.run(True)

        SCORE_MOUSE_POS = pygame.mouse.get_pos()

        xT, yT = x / 2, y / 10
        text_rect = utl.printTitleWithShadow(self, 75, (xT, yT), "Score Board")
        wT = text_rect.width

        # Render the score board data
        offset = 50
        for i, (name, score) in enumerate(self.scoreTable[:10]):
            if i == 0:
                color = "#A31ACB"
            else:
                color = "#2DCDDF"
            utl.printText(self, 40, xT - 200 - offset, yT + 120 + i * 50, f"{i + 1}.  {name}", color)
            utl.printText(self, 40, xT - 200 + offset + wT, yT + 120 + i * 50, str(score), color)

        BACK = Button(image=None, pos=(70, y - 50), text_input="BACK", font=utl.get_font(40),
                      base_color="#d7fcd4", hovering_color="Green", shadow_color="#609966")

        BACK.changeColor(SCORE_MOUSE_POS)
        BACK.update(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                audience.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.checkForInput(SCORE_MOUSE_POS):
                    audience.stop()
                    HomePage.main_menu(self)

        pygame.display.update()
