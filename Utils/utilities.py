import pygame
import cv2

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (248, 6, 204) #(255, 0, 0)
orange = (251, 255, 0) #(255, 165, 0)



def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("../fonts/Sweets Smile.ttf", size)

def get_font_info(size):
    return pygame.font.Font("../fonts/Jackpot.ttf", size)

def get_text_font(size):
    return pygame.font.Font("../fonts/BasqueSmileDemo.ttf", size)

def get_gameOver_text_font(size):
    return pygame.font.Font("../fonts/TheMonkey-Regular.ttf", size)

def printGradientColotedText(self, size, text, centerPos):

    title_font = get_gameOver_text_font(size)
    title_text = title_font.render(text, True, black)
    title_rect = title_text.get_rect(center=centerPos)
    title_gradient = pygame.Surface((title_rect.width, title_rect.height))
    for i in range(title_gradient.get_height()):
        gradient_color = (red[0] + int((orange[0] - red[0]) * i / title_gradient.get_height()),
                          red[1] + int((orange[1] - red[1]) * i / title_gradient.get_height()),
                          red[2] + int((orange[2] - red[2]) * i / title_gradient.get_height()))
        pygame.draw.line(title_gradient, gradient_color, (0, i), (title_gradient.get_width(), i))
    self.screen.blit(title_gradient, title_rect) #, special_flags=pygame.BLEND_MAX)
    self.screen.blit(title_text, title_rect)


def printTitleWithShadow(self, size, centerPos, message):
    x, y = centerPos
    shadow2 = get_font(size).render(message, True, "#A459D1")
    shadow = get_font(size).render(message, True, "#F16767")
    text = get_font(size).render(message, True, "#FFB84C")
    rect = text.get_rect(center=centerPos)
    rect_shadow = text.get_rect(center=(x+size/25, y-size/25))
    rect_shadow2 = text.get_rect(center=(x+size/12, y-size/12))
    self.screen.blit(shadow2, rect_shadow2)
    self.screen.blit(shadow, rect_shadow)
    self.screen.blit(text, rect)
    return text.get_rect()

def printTextWithShadow(self, size, x, y, message):
    shadow = get_font(size).render(message, True, "#865DFF")
    text = get_font(size).render(message, True, "#3A1078")
    self.screen.blit(shadow, (x, y))
    self.screen.blit(text, (x+2, y-2))
    return text.get_rect()

def printText(self, size, x, y, message, color):
    text = get_font(size).render(message, True, color)
    self.screen.blit(text, (x, y))
    return text.get_rect()

def printInfoText(self, size, text, centerPos, color):
    SHADOW = get_text_font(size).render(text, True, "#647E68")
    TEXT = get_text_font(size).render(text, True, color)
    RECT = TEXT.get_rect(center=centerPos)
    x, y = centerPos
    RECT_SHADOW = SHADOW.get_rect(center=(x+1.5, y+1.5))
    self.screen.blit(SHADOW, RECT_SHADOW)
    self.screen.blit(TEXT, RECT)
