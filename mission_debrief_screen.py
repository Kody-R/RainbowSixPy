import pygame
from ui_elements import Button

class MissionDebriefScreen:
    def __init__(self, team, mission, back_callback):
        self.team = team
        self.mission = mission
        self.back_button = Button("Return to Menu", (400, 600), back_callback)
        self.font = pygame.font.SysFont("arial", 20)

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            return self.back_button.callback()
        return self

    def render(self, screen):
        screen.fill((10, 10, 30))

        title = pygame.font.SysFont("arial", 32).render(f"\U0001F4CB Mission Debrief: {self.mission.name}", True, (255, 255, 255))
        screen.blit(title, (50, 30))

        details = [
            f"Location: {self.mission.location}",
            f"Objective: {self.mission.objective}",
            f"Status: COMPLETED"
        ]
        for i, line in enumerate(details):
            label = self.font.render(line, True, (200, 200, 200))
            screen.blit(label, (50, 80 + i * 25))

        screen.blit(self.font.render("Operator Results:", True, (255, 255, 0)), (50, 170))

        for i, op in enumerate(self.team):
            result = f"{op.codename} - Status: {op.status}, HP: {op.health}, XP: {op.xp}, Level: {op.level}"
            label = self.font.render(result, True, (180, 255, 180) if op.is_alive() else (255, 100, 100))
            screen.blit(label, (50, 200 + i * 30))

        self.back_button.draw(screen)