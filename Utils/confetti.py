import pygame
import random

pygame.init()

class Confetti(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.get_random_color(), (size // 2, size // 2), size // 2)  # draw a colored circle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.y += self.speed

    def get_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class PlayConfetti:
    def __init__(self, screen, num):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.confetti_group = pygame.sprite.Group()

        self.create_confetti(num)

    def create_confetti(self, num_confetti):
        for i in range(num_confetti):
            x = random.randint(0, self.width)
            y = random.randint(-500, -50)
            size = random.randint(5, 20)
            confetti = Confetti(x, y, size)
            self.confetti_group.add(confetti)

    def update_confetti(self):
        for confetti in self.confetti_group:
            confetti.update()
            if confetti.rect.y > self.height:
                self.confetti_group.remove(confetti)

    def run(self, isWin = True):
        # check for win condition
        if isWin:
            self.confetti_group.draw(self.screen)
            self.update_confetti()
