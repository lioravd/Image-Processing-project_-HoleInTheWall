import pygame
import sys
import threading
from Utils.button import Button
from Utils import utilities as utl
import Source.PlayPage as PlayPage
import Source.ScorePage as ScorePage
import Source.TrailerPage as TrailerPage
import time
import threading


def main_menu(self):
    calib_color_off = "#865DFF"
    calib_color_on = "#647E68"
    calib_color = calib_color_off

    # Set up the timer
    TIMER_EVENT = pygame.USEREVENT + 1
    PHOTO_EXPIRE_TIME = self.PHOTO_EXPIRE_TIME

    PLAY_EVENT = pygame.USEREVENT + 2
    OPTIONS_EVENT = pygame.USEREVENT + 3
    TRAILER_EVENT = pygame.USEREVENT + 4
    QUIT_EVENT = pygame.USEREVENT + 5

    x, y = self.screen.get_size()
    PLAY_BUTTON = Button(image=None, pos=(190, y/2-60),text_input="PLAY", font=utl.get_font(45),
                         base_color="#d7fcd4", hovering_color="Green", shadow_color="#609966", event=PLAY_EVENT)
    OPTIONS_BUTTON = Button(image=None, pos=(130, y/2+30), text_input="SCORE BOARD", font=utl.get_font(40),
                            base_color="#d7fcd4", hovering_color="Green", shadow_color="#609966", event=OPTIONS_EVENT)
    TRAILER_BUTTON = Button(image=None, pos=(160, y/2+120), text_input="TRAILER", font=utl.get_font(45),
                            base_color="#d7fcd4", hovering_color="Green", shadow_color="#609966", event=TRAILER_EVENT)
    QUIT_BUTTON = Button(image=None, pos=(185, y/2+210), text_input="QUIT", font=utl.get_font(45),
                         base_color="#d7fcd4", hovering_color="Green", shadow_color="#609966", event=QUIT_EVENT)


    # Threads
    camera_surface = None
    runThread = True
    def th_func():
        while runThread:
            if camera_surface != None and self.calibration_image != None:
                btns = [PLAY_BUTTON, OPTIONS_BUTTON, TRAILER_BUTTON, QUIT_BUTTON]
                for button in btns:
                    button.changeColorDelagate(camera_surface, self.calibration_image)
                    button.update(self.screen)
                isSelectedList = [button.isSelected for button in btns]
                if isSelectedList.count(True) == 1:
                    btn = btns[isSelectedList.index(True)]
                    btn.checkForInputDelagate()
            time.sleep(0.05)


    th = threading.Thread(target=th_func)
    th.start()


    self.sound_background.play(loops=-1)  #FIXME - enable
    while True:
        self.clock.tick(200)
        # Get the next frame from the video capture
        cap = self.cam.get_image()
        camera_surface = pygame.transform.scale(cap, self.screen.get_size()) # Scale the frame surface to fill the display surface
        self.screen.blit(camera_surface, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        utl.printTitleWithShadow(self, 135, (x/2, round(y/7)), "Hole In The Wall")


        CALIBRATION_BUTTON = Button(image=None, pos=(140, y-50), text_input="Take Photo", font=utl.get_font(30),
                                    base_color=calib_color, hovering_color="#395B64", shadow_color="#FFFFD0")

        for button in [CALIBRATION_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(self.screen)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, TRAILER_BUTTON, QUIT_BUTTON]:
            button.update(self.screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sound_background.stop()
                runThread = False
                th.join()
                pygame.quit()
                sys.exit()
            if event.type == TIMER_EVENT:
                calib_color = calib_color_off
                pygame.time.set_timer(TIMER_EVENT, PHOTO_EXPIRE_TIME)
            if event.type == PLAY_EVENT:
                runThread = False
                th.join()
                PlayPage.menu_play(self)
            if event.type == OPTIONS_EVENT:
                runThread = False
                th.join()
                ScorePage.menu_score(self)
            if event.type == TRAILER_EVENT:
                runThread = False
                th.join()
                self.sound_background.stop()
                TrailerPage.menu_trailer(self)
            if event.type == QUIT_EVENT:
                # Raise the QUIT event
                runThread = False
                th.join()
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    runThread = False
                    PlayPage.menu_play(self)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    runThread = False
                    ScorePage.menu_score(self)
                if TRAILER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    runThread = False
                    self.sound_background.stop()
                    TrailerPage.menu_trailer(self)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Raise the QUIT event
                    runThread = False
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                    break
                if CALIBRATION_BUTTON.checkForInput(MENU_MOUSE_POS):
                    calib_color = calib_color_on
                    self.captureCalibrationImage(camera_surface)
                    pygame.time.set_timer(TIMER_EVENT, PHOTO_EXPIRE_TIME)
        pygame.display.update()






