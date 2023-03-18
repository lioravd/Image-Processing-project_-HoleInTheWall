import pygame
import threading
from Source.figureMatching import is_hand

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, shadow_color=None, event=None):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.shadow_color = shadow_color
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.press_sound = pygame.mixer.Sound("../sounds/mixkit-retro-game-notification-212.wav")
        self.isSelected = False
        self.isPressed = [False, False, False]
        self.i_press = 0

        # Define a custom event type
        self.EVENT_TYPE = event

        self.shadow = None
        if self.shadow_color is not None:
            self.shadow = self.font.render(self.text_input, True, self.shadow_color)

        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        if self.shadow is not None:
            (x, y) = self.text_rect.topleft
            screen.blit(self.shadow, (x+2, y+2))
            screen.blit(self.text, self.text_rect)

    def checkForInputDelagate(self):
        if all(self.isPressed):
            self.press_sound.play()
            my_event = pygame.event.Event(self.EVENT_TYPE)
            pygame.event.post(my_event)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) \
                and position[1] in range(self.rect.top, self.rect.bottom):
            self.press_sound.play()
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) \
                and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    # def changeColor(self, cap, ref_cap):
    #     if ref_cap != None:
    #         if self.th != None: self.th.join()
    #         self.th = threading.Thread(self.changeColorDelagate, args=(cap, ref_cap))
    #         self.th.start()

    def changeColorDelagate(self, cap, ref_cap):
        if ref_cap != None and is_hand([self.text_rect.x, self.text_rect.y, self.text_rect.width, self.text_rect.height], cap, ref_cap):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            self.isSelected = True
            self.isPressed[self.i_press % len(self.isPressed)] = True
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.isSelected = False
            self.isPressed = [False for i in range(len(self.isPressed))]

        self.i_press += 1
