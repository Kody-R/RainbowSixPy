class Mission:
    def __init__(self, name, objective, location, difficulty, enemies, intel_level, required_roles=None):
        self.name = name
        self.objective = objective
        self.location = location
        self.difficulty = difficulty
        self.enemies = enemies  # Number or type of enemies
        self.intel_level = intel_level  # How much info you have ahead of time
        self.required_roles = required_roles if required_roles else []  # E.g., ["Sniper", "Hacker"]
        self.completed = False

    def show_briefing(self):
        print(f"\nMISSION: {self.name}")
        print(f"Location: {self.location}")
        print(f"Objective: {self.objective}")
        print(f"Difficulty: {self.difficulty}")
        print(f"Enemy Presence: {self.enemies}")
        print(f"Intel Level: {self.intel_level}")
        if self.required_roles:
            print(f"Required Roles: {', '.join(self.required_roles)}")
