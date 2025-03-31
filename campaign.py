class CampaignState:
    def __init__(self, name, operators, completed_missions=None, unlocked_gear=None):
        self.name = name
        self.operators = operators
        self.completed_missions = completed_missions or []
        self.unlocked_gear = unlocked_gear or set()

    def mark_mission_complete(self, mission_name):
        if mission_name not in self.completed_missions:
            self.completed_missions.append(mission_name)

    def unlock_gear(self, gear_name):
        self.unlocked_gear.add(gear_name)

    def is_gear_unlocked(self, gear_name):
        return gear_name in self.unlocked_gear
