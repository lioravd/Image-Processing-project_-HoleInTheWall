import pygame

def countdown(screen, num):
    # Create circular background surface
    background_surface = pygame.Surface((250, 250), pygame.SRCALPHA)
    pygame.draw.circle(background_surface, (0, 0, 0), (125, 125), 125)
    pygame.draw.circle(background_surface, (255, 255, 255), (125, 125), 120)

    # Render number text
    font = pygame.font.Font(None, 200)
    number_text = font.render(str(num), True, (0, 0, 0))

    # Get text and background surface dimensions
    number_text_rect = number_text.get_rect()
    background_surface_rect = background_surface.get_rect()
    number_text_rect.center = background_surface_rect.center

    # Stop playing countdown sound
    if num == 0:
        # Render start text
        fontStart = pygame.font.Font(None, 100)
        start_text = fontStart.render("START", True, (0, 0, 0))
        # Get text and background surface dimensions
        start_text_rect = start_text.get_rect()
        start_text_rect.center = background_surface_rect.center
        number_text = start_text
        number_text_rect = start_text_rect

    # Center the background surface on the screen
    background_surface_rect.center = screen.get_rect().center

    # Display the background surface and number text on the screen
    background_surface.blit(number_text, number_text_rect)
    screen.blit(background_surface, background_surface_rect)

    # Update the screen
    pygame.display.update()

    # Wait for 1 second
    pygame.time.wait(1000)


def playCountdown(self):
    # Load sound
    countdown_sound = pygame.mixer.Sound("../sounds/game-countdown.wav")

    # Start the countdown
    countdown_sound.play()
    for num in range(3, -1, -1):
        countdown(self.screen, num)
    countdown_sound.stop()
