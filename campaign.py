class CampaignState:
    def __init__(self, name, operators, completed_missions=None, unlocked_gear=None, generated_missions=None):
        self.name = name
        self.operators = operators
        self.completed_missions = completed_missions or []
        self.unlocked_gear = unlocked_gear or set()
        self.generated_missions = generated_missions or {}  # key: mission.name, value: Mission object

    def mark_mission_complete(self, mission):
        if mission.name not in self.completed_missions:
            self.completed_missions.append(mission.name)
            self.generated_missions[mission.name] = mission  # store full mission for map reference


    def unlock_gear(self, gear_name):
        self.unlocked_gear.add(gear_name)

    def is_gear_unlocked(self, gear_name):
        return gear_name in self.unlocked_gear
