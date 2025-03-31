import pygame
from ui_elements import Button
from game_data import gear_catalog
from mission_briefing_screen import MissionBriefingScreen

class GearLoadoutScreen:
    def __init__(self, campaign,team, on_complete, back_callback):
        self.campaign = campaign
        self.team = team
        self.index = 0
        self.operator = self.team[self.index]
        self.on_complete = on_complete
        self.back_button = Button("Back", (50, 620), back_callback)
        self.next_button = Button("Next Operator", (700, 620), self.next_operator)
        self.font = pygame.font.SysFont("arial", 20)
        self.scroll_offset = 0
        self.scroll_speed = 30

    def next_operator(self):
        if self.index + 1 < len(self.team):
            self.index += 1
            self.operator = self.team[self.index]
            self.scroll_offset = 0
            return self

        return self.on_complete(self.team, self.campaign)


    def handle_event(self, event):
        if self.back_button.handle_event(event):
            return self.back_button.callback()
        if self.next_button.handle_event(event):
            return self.next_button.callback()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.scroll_offset = max(self.scroll_offset - self.scroll_speed, 0)
            elif event.button == 5:
                self.scroll_offset += self.scroll_speed
            else:
                x, y = event.pos
                for idx, gear in enumerate(gear_catalog):
                    y_pos = 150 + idx * 30 - self.scroll_offset
                    if 50 <= x <= 600 and y_pos <= y <= y_pos + 25:
                        if self.operator.can_use(gear):
                            self.operator.assign_gear(gear)
        return self

    def render(self, screen):
        screen.fill((10, 10, 10))
        op = self.operator
        title = pygame.font.SysFont("arial", 28).render(f"📦 Gear Loadout: {op.codename} ({op.role})", True, (255, 255, 255))
        screen.blit(title, (50, 30))

        current = self.font.render(f"Loadout: {', '.join(op.get_gear_names()) or 'None'}", True, (200, 200, 200))
        screen.blit(current, (50, 70))

        weight = self.font.render(f"Current Weight: {op.current_loadout_weight()} / {op.max_gear_weight}", True, (200, 200, 200))
        screen.blit(weight, (50, 100))

        screen.blit(self.font.render("Available Gear:", True, (255, 255, 0)), (50, 130))

        for idx, gear in enumerate(gear_catalog):
            y_pos = 150 + idx * 30 - self.scroll_offset
            if 150 <= y_pos <= 580:
                if not op.can_use(gear):
                    continue
                label = self.font.render(
                    f"{gear.name} [{gear.type}] - {gear.rarity} ({gear.weight}w)", True, (255, 255, 255)
                )
                screen.blit(label, (50, y_pos))

        self.back_button.draw(screen)
        self.next_button.draw(screen)
