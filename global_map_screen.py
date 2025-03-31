import pygame
from ui_elements import Button

TYPE_ICONS = {
    "Extraction": "🛩️",
    "Sabotage": "💣",
    "Cyber": "💻",
    "Assault": "🔫",
    "Rescue": "🚑",
    "Demolition": "🔥",
    "Unknown": "❓"
}

class GlobalMapScreen:
    def __init__(self, campaign, back_callback):
        self.campaign = campaign
        self.back_button = Button("Back to Menu", (50, 600), back_callback)
        self.font = pygame.font.SysFont("arial", 20)

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            return self.back_button.callback()
        return self

    def render(self, screen):
        screen.fill((10, 10, 30))
        title = pygame.font.SysFont("arial", 32).render("🌍 Global Operations Map", True, (255, 255, 255))
        screen.blit(title, (50, 30))

        missions = list(self.campaign.generated_missions.values())
        missions.sort(key=lambda m: m.location)

        y_offset = 100
        for m in missions:
            completed = m.name in self.campaign.completed_missions
            status_icon = "✅" if completed else "🔲"
            type_icon = TYPE_ICONS.get(getattr(m, "mission_type", "Unknown"), "❓")
            text = f"{status_icon} {type_icon} {m.location} — {m.name} ({m.mission_type})"
            label = self.font.render(text, True, (200, 200, 200))
            screen.blit(label, (50, y_offset))
            y_offset += 30

        self.back_button.draw(screen)