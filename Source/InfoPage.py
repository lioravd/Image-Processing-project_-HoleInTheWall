import pygame, sys
from Utils import utilities as utl
from Utils.button import Button
from Source.GameRun import StartGame
from Source.figureMatching import is_in_pos
import time
import threading

def infoPage(self):
    x, y = self.screen.get_size()

    CONT_EVENT = pygame.USEREVENT + 2

    CONT = Button(image=None, pos=(x / 2, 50 + 220),
                  text_input="Start Game", font=utl.get_font(40), base_color="#d7fcd4", hovering_color="Green",
                  shadow_color="#609966", event=CONT_EVENT)

    # Threads
    camera_surface = None
    runThread = True

    def th_func():
        while runThread:
            if camera_surface != None:
                btns = [CONT]
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

        MOUSE_POS = pygame.mouse.get_pos()
        utl.printTitleWithShadow(self, 40, (x/2, 50), "Games Rules:")
        utl.printInfoText(self, 30, "In this game, you have three lives.", (x / 2, 50+50), "#d7fcd4")
        utl.printInfoText(self, 30, "Avoid walls to keep your lives, and pass through them to earn points.", (x / 2, 50+80), "#d7fcd4")
        utl.printInfoText(self, 30, "Passing a wall earns you maximum 100 points, partial success earns less,", (x / 2, 50+110), "#d7fcd4")
        utl.printInfoText(self, 30, "and failure earns you 0 points.", (x / 2, 50+140), "#d7fcd4")
        utl.printInfoText(self, 30, "Pass all walls to win each level, but be careful not to lose all your lives!", (x / 2, 50+170), "#d7fcd4")

        for button in [CONT]:
            button.update(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runThread = False
                pygame.quit()
                sys.exit()
            if event.type == CONT_EVENT:
                runThread = False
                calibrationPage(self)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONT.checkForInput(MOUSE_POS):
                    runThread = False
                    calibrationPage(self)

        pygame.display.update()

def calibrationPage(self):
    x, y = self.screen.get_size()

    rect_width = x/4
    rect_height = y-150
    border_width = 4
    rect_color = (0, 0, 255)  # red with alpha of 128 (50% transparent)

    press_sound = pygame.mixer.Sound("../sounds/in_positions.wav")

    # Create a new thread and start it
    calibration_image = self.calibration_image
    rect_x, rect_y, camera_surface = None, None, None
    inPosition = False

    def th_func_one_player():
        nonlocal inPosition
        res = [False, False, False]
        i = 0
        while not all(res):
            print(res)
            if camera_surface != None:
                res[i % len(res)] = is_in_pos([rect_x, rect_y, rect_width, rect_height], camera_surface, calibration_image)
            time.sleep(0.1)
            i += 1
        inPosition = True

    def th_func_two_player():
        nonlocal inPosition
        res = [False, False, False]
        i = 0
        while not all(res):
            print(res)
            if camera_surface != None:
                res[i % len(res)] = is_in_pos([rect_x1, rect_y1, rect_width, rect_height], camera_surface, calibration_image) \
                                    and is_in_pos([rect_x2, rect_y2, rect_width, rect_height], camera_surface, calibration_image)
            time.sleep(0.1)
            i += 1
        inPosition = True

    if self.currentPlayer.numOfPlayers == 1:
        th = threading.Thread(target=th_func_one_player)
    else:
        th = threading.Thread(target=th_func_two_player)
    th.start()



    while True:
        # Get the next frame from the video capture
        cap = self.cam.get_image()
        camera_surface = pygame.transform.scale(cap, self.screen.get_size())  # Scale the frame surface to fill the display surface
        self.screen.blit(camera_surface, (0, 0))

        MOUSE_POS = pygame.mouse.get_pos()
        if self.currentPlayer.numOfPlayers == 1:
            utl.printTitleWithShadow(self, 50, (x/2, 50), "Get In Position")
            # Draw a rectangle
            rect_x = x/2 - rect_width/2
            rect_y = y-rect_height

            pygame.draw.rect(self.screen, rect_color, (rect_x, rect_y, rect_width, rect_height), border_width)

        else:
            utl.printTitleWithShadow(self, 50, (x / 2, 50), "Get In Positions")
            # Draw a rectangle
            rect_x1 = x/2 - rect_width/2 - 200
            rect_y1 = y-rect_height
            pygame.draw.rect(self.screen, rect_color, (rect_x1, rect_y1, rect_width, rect_height), border_width)
            rect_x2 = x/2 - rect_width/2 + 200
            rect_y2 = y-rect_height
            pygame.draw.rect(self.screen, rect_color, (rect_x2, rect_y2, rect_width, rect_height), border_width)


        # CONT = Button(image=None, pos=(x/2, y - 50),
        #               text_input="Start Game", font=utl.get_font(30), base_color="#d7fcd4", hovering_color="Green", shadow_color="#609966")
        if inPosition:
            press_sound.play()
            StartGame(self)

        # for button in [CONT]:
        #     button.changeColor(MOUSE_POS)
        #     button.update(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if CONT.checkForInput(MOUSE_POS):
        #             StartGame(self)

        pygame.display.update()