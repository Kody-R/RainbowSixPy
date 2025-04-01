import pygame
from ui_elements import Button
from gear_loadout_screen import GearLoadoutScreen

class TeamSelectScreen:
    def __init__(self, campaign, on_team_confirm, back_callback):
        self.campaign = campaign
        self.operators = campaign.operators
        self.selected = []
        self.on_team_confirm = on_team_confirm
        self.back_button = Button("Back", (50, 620), back_callback)
        self.confirm_button = Button("Confirm Team", (700, 620), self.confirm_team)
        self.font = pygame.font.SysFont("arial", 20)
        self.scroll_offset = 0
        self.scroll_speed = 30

    def confirm_team(self):
        if 2 <= len(self.selected) <= 4:
            return GearLoadoutScreen(self.campaign, self.selected, self.on_team_confirm, lambda: self)
        return self  # stay on screen if not valid

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            return self.back_button.callback()
        if self.confirm_button.handle_event(event):
            return self.confirm_button.callback()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # scroll up
                self.scroll_offset = max(self.scroll_offset - self.scroll_speed, 0)
            elif event.button == 5:  # scroll down
                self.scroll_offset += self.scroll_speed
            else:
                x, y = event.pos
                for idx, op in enumerate(self.operators):
                    y_pos = 100 + idx * 40 - self.scroll_offset
                    if 50 <= x <= 450 and y_pos <= y <= y_pos + 35:
                        if op in self.selected:
                            self.selected.remove(op)
                        elif len(self.selected) < 4:
                            self.selected.append(op)

        return self

    def render(self, screen):
        screen.fill((15, 15, 15))
        title = pygame.font.SysFont("arial", 30).render("🔧 Select Your Team (2-4)", True, (255, 255, 255))
        screen.blit(title, (50, 30))

        # Scrollable operator list
        for idx, op in enumerate(self.operators):
            y_pos = 100 + idx * 40 - self.scroll_offset
            if 100 <= y_pos <= 600:
                text = f"{op.codename} ({op.role}) - {op.status}"
                color = (100, 255, 100) if op in self.selected else (255, 255, 255)
                label = self.font.render(text, True, color)
                screen.blit(label, (50, y_pos))

        # Selected operator slots
        slot_x = 550
        for i in range(4):
            rect = pygame.Rect(slot_x, 100 + i * 100, 400, 80)
            pygame.draw.rect(screen, (50, 50, 100), rect)
            if i < len(self.selected):
                op = self.selected[i]
                label = self.font.render(f"{op.codename} ({op.role})", True, (255, 255, 255))
                screen.blit(label, (slot_x + 10, 100 + i * 100 + 10))

        self.back_button.draw(screen)
        self.confirm_button.draw(screen)
