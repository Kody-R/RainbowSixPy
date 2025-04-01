from ui_elements import Button
from global_map_screen import GlobalMapScreen
from operator_screen import OperatorRosterScreen
from team_select_screen import TeamSelectScreen
from gear_loadout_screen import GearLoadoutScreen
from mission_briefing_screen import MissionBriefingScreen
from mission_gameplay_screen import MissionGameplayScreen
from mission_debrief_screen import MissionDebriefScreen

class MainMenuScreen:
    def __init__(self, campaign):
        self.campaign = campaign
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
        return TeamSelectScreen(self.campaign, self.launch_mission_with_team, lambda: self)

    def view_operators(self):
        return OperatorRosterScreen(self.campaign, lambda: self)

    def launch_mission_with_team(self, team, campaign):
        return GearLoadoutScreen(campaign, team, self.launch_mission_briefing, lambda: self)


    def launch_mission_briefing(self, team, campaign):
        return MissionBriefingScreen(campaign, team, self.launch_gameplay, lambda: self)


    def launch_gameplay(self, team, mission):
        return MissionGameplayScreen(team, mission, self.campaign, self.launch_debrief)

    def launch_debrief(self, team, mission):
        return MissionDebriefScreen(team, mission, lambda: self)

    def view_map(self):
        return GlobalMapScreen(self.campaign, lambda: self)

    def exit_game(self):
        import pygame
        pygame.quit()
        exit()
