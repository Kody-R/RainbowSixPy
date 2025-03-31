import pygame
from screens import main_menu_screen, campaign as screens_campaign
from main import choose_campaign 


campaign = choose_campaign()
screens_campaign = campaign 

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rainbow Six: Strategic Ops")

clock = pygame.time.Clock()
running = True

# Starting screen
current_screen = main_menu_screen

while running:
    screen.fill((15, 15, 15))  # Dark theme
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        current_screen = current_screen.handle_event(event)

    current_screen.render(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
