import pygame
from ui_elements import Button
from mission_generator import generate_random_mission
from mission_gameplay_screen import MissionGameplayScreen
from main import mission_maps 

class MissionBriefingScreen:
    def __init__(self, campaign, team, on_launch, back_callback):
        self.campaign = campaign
        self.team = team
        self.mission, self.map_data = generate_random_mission(len(campaign.completed_missions))
        self.on_launch = on_launch
        self.back_button = Button("Back", (50, 620), back_callback)
        self.launch_button = Button("Launch Mission", (700, 620), self.launch)
        self.font = pygame.font.SysFont("arial", 20)

    def launch(self):
        # Generate new mission + zone map
        mission, zones = generate_random_mission(len(self.campaign.completed_missions))
        self.mission = mission
        mission_maps[mission.name] = zones  # 🔥 Store the zone map!

        # Save the mission to the campaign
        self.campaign.generated_missions[mission.name] = mission

        # Proceed to gameplay screen
        return MissionGameplayScreen(self.team, mission, zones, self.campaign, self.on_launch)



    def handle_event(self, event):
        if self.back_button.handle_event(event):
            return self.back_button.callback()
        if self.launch_button.handle_event(event):
            return self.launch_button.callback()
        return self

    def render(self, screen):
        screen.fill((10, 10, 30))

        title = pygame.font.SysFont("arial", 28).render(f"\U0001f4cb Mission Briefing: {self.mission.name}", True, (255, 255, 255))
        screen.blit(title, (50, 30))

        lines = [
            f"Location: {self.mission.location}",
            f"Objective: {self.mission.objective}",
            f"Difficulty: {self.mission.difficulty}",
            f"Enemy Presence: {self.mission.enemies}",
            f"Intel Level: {self.mission.intel_level}",
            f"Terrain: {self.mission.terrain} ({', '.join(self.mission.terrain_effect.keys()) or 'None'})",
        ]

        for i, line in enumerate(lines):
            label = self.font.render(line, True, (200, 200, 200))
            screen.blit(label, (50, 80 + i * 30))

        # Team preview
        screen.blit(self.font.render("Selected Team:", True, (255, 255, 0)), (550, 80))
        for idx, op in enumerate(self.team):
            text = f"{op.codename} ({op.role}) - Loadout: {', '.join(op.get_gear_names()) or 'None'}"
            label = self.font.render(text, True, (200, 200, 200))
            screen.blit(label, (550, 110 + idx * 30))

        self.back_button.draw(screen)
        self.launch_button.draw(screen)