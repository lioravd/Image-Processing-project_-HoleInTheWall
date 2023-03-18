import pygame
import sys, time, threading
from Utils.button import Button
from Utils import utilities as utl
import Source.HomePage as HomePage
from Source.InfoPage import infoPage
from Source.Player import Player

def menu_play(self):
    x, y = self.screen.get_size()

    PLAY_ONE_EVENT = pygame.USEREVENT + 2
    PLAY_TWO_EVENT = pygame.USEREVENT + 3

    PLAY_ONE = Button(image=None, pos=(x/2-100, y/7+70), text_input="1 Player", font=utl.get_font(40),
                      base_color="#d7fcd4", hovering_color="Green", shadow_color="#609966", event=PLAY_ONE_EVENT)
    PLAY_TWO = Button(image=None, pos=(x/2+100, y/7+70), text_input="2 Player", font=utl.get_font(40),
                      base_color="#d7fcd4", hovering_color="Green", shadow_color="#609966", event=PLAY_TWO_EVENT)
    PLAY_BACK = Button(image=None, pos=(70, y-50),
                        text_input="BACK", font=utl.get_font(40), base_color="#d7fcd4", hovering_color="Green", shadow_color="#609966")

    # Threads
    camera_surface = None
    runThread = True
    def th_func():
        while runThread:
            if camera_surface != None:
                btns = [PLAY_ONE, PLAY_TWO]
                for button in btns:
                    button.changeColorDelagate(camera_surface, self.calibration_image)
                    button.update(self.screen)
                isSelectedList = [button.isSelected for button in btns]
                if isSelectedList.count(True) == 1:
                    btn = btns[isSelectedList.index(True)]
                    btn.checkForInputDelagate()
            time.sleep(0.1)


    th = threading.Thread(target=th_func)
    th.start()

    while True:
        # Get the next frame from the video capture
        cap = self.cam.get_image()
        camera_surface = pygame.transform.scale(cap, self.screen.get_size())  # Scale the frame surface to fill the display surface
        self.screen.blit(camera_surface, (0, 0))

        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        utl.printTitleWithShadow(self, 50, (x/2, y/9), "Select Number Of Players")


        for button in [PLAY_BACK]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(self.screen)

        for button in [PLAY_ONE, PLAY_TWO]:
            button.update(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runThread = False
                pygame.quit()
                sys.exit()
            if event.type == PLAY_ONE_EVENT:
                runThread = False
                getPlayer(self, True)
            if event.type == PLAY_TWO_EVENT:
                runThread = False
                getPlayer(self, False)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_ONE.checkForInput(PLAY_MOUSE_POS):
                    runThread = False
                    getPlayer(self, True)
                if PLAY_TWO.checkForInput(PLAY_MOUSE_POS):
                    runThread = False
                    getPlayer(self, False)
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    runThread = False
                    HomePage.main_menu(self)

        pygame.display.update()

def getPlayer(self, isOnePlayer):
    x, y = self.screen.get_size()

    user_text = ''
    base_font = utl.get_text_font(32)

    # create rectangle
    input_rect = pygame.Rect(x / 2 - 150, y / 7 + 50, 300, 42)

    # color_active stores color(lightskyblue3) which gets active when input box is clicked by user
    color_passive = pygame.Color('lightskyblue3')
    color_active = "#FFB84C"

    active = False

    DONE_EVENT = pygame.USEREVENT + 2

    # Buttons:
    DONE = Button(image=None, pos=(x / 2, y / 7 + 110),
                  text_input="Continue", font=utl.get_font(40), base_color="#d7fcd4", hovering_color="Green",
                  shadow_color="#609966", event=DONE_EVENT)
    BACK = Button(image=None, pos=(70, y - 50),
                  text_input="BACK", font=utl.get_font(40), base_color="#d7fcd4", hovering_color="Green",
                  shadow_color="#609966")

    # Threads
    camera_surface = None
    runThread = True
    def th_func():
        while runThread:
            if camera_surface != None:
                btns = [DONE]
                for button in btns:
                    button.changeColorDelagate(camera_surface, self.calibration_image)
                    button.update(self.screen)
                isSelectedList = [button.isSelected for button in btns]
                if isSelectedList.count(True) == 1:
                    btn = btns[isSelectedList.index(True)]
                    btn.checkForInputDelagate()
            time.sleep(0.1)


    th = threading.Thread(target=th_func)
    th.start()

    while True:
        # Get the next frame from the video capture
        cap = self.cam.get_image()
        camera_surface = pygame.transform.scale(cap, self.screen.get_size())  # Scale the frame surface to fill the display surface
        self.screen.blit(camera_surface, (0, 0))

        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        if isOnePlayer:
            utl.printTitleWithShadow(self, 50, (x / 2, y / 7), "Enter Player Nickname:")
        else:
            utl.printTitleWithShadow(self, 50, (x / 2, y / 7), "Enter Group Nickname:")


        for button in [BACK]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(self.screen)

        for button in [DONE]:
            button.update(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runThread = False
                pygame.quit()
                sys.exit()
            if event.type == DONE_EVENT:
                runThread = False
                th.join()
                self.currentPlayer = Player(user_text, 1 if isOnePlayer else 2, self.calibration_image)
                chooseGameLevel(self)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.checkForInput(PLAY_MOUSE_POS):
                    runThread = False
                    menu_play(self)
                if DONE.checkForInput(PLAY_MOUSE_POS):
                    runThread = False
                    self.currentPlayer = Player(user_text, 1 if isOnePlayer else 2, self.calibration_image)
                    chooseGameLevel(self)
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                # Unicode standard is used for string formation
                else:
                    user_text += event.unicode

        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(self.screen, color, input_rect)
        text_surface = base_font.render(user_text, True, (255, 255, 255))

        # render at position stated in arguments
        self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # set width of textfield so that text cannot get outside of user's text input
        input_rect.w = max(input_rect.width, text_surface.get_width() + 10)

        pygame.display.update()


def chooseGameLevel(self):
    x, y = self.screen.get_size()

    EASY_EVENT = pygame.USEREVENT + 2
    MIDDLE_EVENT = pygame.USEREVENT + 3
    HARD_EVENT = pygame.USEREVENT + 4

    EASY = Button(image=None, pos=(x / 2 - 200, y / 7 + 70),
                  text_input="EASY", font=utl.get_font(40), base_color="#d7fcd4", hovering_color="Green",
                  shadow_color="#609966", event=EASY_EVENT)
    MIDDLE = Button(image=None, pos=(x / 2, y / 7 + 70),
                    text_input="MID", font=utl.get_font(40), base_color="#d7fcd4", hovering_color="Green",
                    shadow_color="#609966", event=MIDDLE_EVENT)
    HARD = Button(image=None, pos=(x / 2 + 200, y / 7 + 70),
                  text_input="HARD", font=utl.get_font(40), base_color="#d7fcd4", hovering_color="Green",
                  shadow_color="#609966", event=HARD_EVENT)
    BACK = Button(image=None, pos=(70, y - 50),
                  text_input="BACK", font=utl.get_font(40), base_color="#d7fcd4", hovering_color="Green",
                  shadow_color="#609966")

    # Threads
    camera_surface = None
    runThread = True
    def th_func():
        while runThread:
            if camera_surface != None:
                btns = [EASY, MIDDLE, HARD]
                for button in btns:
                    button.changeColorDelagate(camera_surface, self.calibration_image)
                    button.update(self.screen)
                isSelectedList = [button.isSelected for button in btns]
                if isSelectedList.count(True) == 1:
                    btn = btns[isSelectedList.index(True)]
                    btn.checkForInputDelagate()
            time.sleep(0.1)


    th = threading.Thread(target=th_func)
    th.start()

    while True:
        # Get the next frame from the video capture
        cap = self.cam.get_image()
        camera_surface = pygame.transform.scale(cap, self.screen.get_size())  # Scale the frame surface to fill the display surface
        self.screen.blit(camera_surface, (0, 0))

        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        utl.printTitleWithShadow(self, 50, (x/2, y/7), "Select Game Level")

        for button in [BACK]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(self.screen)

        for button in [EASY, MIDDLE, HARD]:
            button.update(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runThread = False
                pygame.quit()
                sys.exit()
            if event.type == EASY_EVENT:
                runThread = False
                self.currentPlayer.setLevel(1)
                infoPage(self)
            if event.type == MIDDLE_EVENT:
                runThread = False
                self.currentPlayer.setLevel(2)
                infoPage(self)
            if event.type == HARD_EVENT:
                runThread = False
                th.join()
                self.currentPlayer.setLevel(3)
                infoPage(self)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY.checkForInput(PLAY_MOUSE_POS):
                    runThread = False
                    self.currentPlayer.setLevel(1)
                    infoPage(self)
                if MIDDLE.checkForInput(PLAY_MOUSE_POS):
                    runThread = False
                    self.currentPlayer.setLevel(2)
                    infoPage(self)
                if HARD.checkForInput(PLAY_MOUSE_POS):
                    runThread = False
                    self.currentPlayer.setLevel(3)
                    infoPage(self)
                if BACK.checkForInput(PLAY_MOUSE_POS):
                    runThread = False
                    menu_play(self)

        pygame.display.update()
