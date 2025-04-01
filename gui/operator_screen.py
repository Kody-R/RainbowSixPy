import pygame
from ui_elements import Button

class OperatorRosterScreen:
    def __init__(self, campaign, back_callback):
        self.campaign = campaign
        self.back_button = Button("Back to Menu", (50, 600), back_callback)
        self.font = pygame.font.SysFont("arial", 20)

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            return self.back_button.callback()
        return self

    def render(self, screen):
        screen.fill((20, 20, 20))
        title = pygame.font.SysFont("arial", 32).render("\U0001f465 Operator Roster", True, (255, 255, 255))
        screen.blit(title, (50, 30))

        y_offset = 100
        for op in self.campaign.operators:
            text = (
                f"{op.codename} ({op.role}) — Level {op.level}, XP: {op.xp}, "
                f"Status: {op.status}, HP: {op.health}"
            )
            label = self.font.render(text, True, (200, 200, 200))
            screen.blit(label, (50, y_offset))
            y_offset += 30

        self.back_button.draw(screen)
