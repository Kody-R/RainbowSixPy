import pygame
pygame.init()

from campaign import CampaignState
from game_data import default_operators
from screens import MainMenuScreen

# Setup game window
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Rainbow Six: Strategic Ops")

# Create campaign and main menu screen
campaign = CampaignState("Default", default_operators)
main_menu_screen = MainMenuScreen(campaign)
current_screen = main_menu_screen

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            current_screen = current_screen.handle_event(event)

    current_screen.render(screen)
    pygame.display.flip()

pygame.quit()
