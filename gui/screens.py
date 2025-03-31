from ui_elements import Button
from global_map_screen import GlobalMapScreen

# This should be set externally in your main script
campaign = None

class MainMenuScreen:
    def __init__(self):
        self.buttons = [
            Button("Start Random Mission", (100, 100), self.start_mission),
            Button("View Operators", (100, 160), self.view_operators),
            Button("Global Map", (100, 220), self.view_map),
            Button("Exit", (100, 280), self.exit_game),
        ]

    def handle_event(self, event):
        for btn in self.buttons:
            if btn.handle_event(event):
                return btn.callback()
        return self

    def render(self, screen):
        for btn in self.buttons:
            btn.draw(screen)

    def start_mission(self):
        print("Starting Mission...")  # Replace with actual screen switch
        return self

    def view_operators(self):
        print("Viewing Operators...")  # Replace with actual screen switch
        return self

    def view_map(self):
        return GlobalMapScreen(campaign, lambda: main_menu_screen)

    def exit_game(self):
        import pygame
        pygame.quit()
        exit()

main_menu_screen = MainMenuScreen()
