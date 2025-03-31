class MissionState:
    def __init__(self):
        self.alert = 0  # Global alert level

    def raise_alert(self, amount):
        self.alert += amount
        if self.alert > 100:
            self.alert = 100

    def get_difficulty_modifier(self):
        if self.alert < 30:
            return 0
        elif self.alert < 60:
            return 1
        elif self.alert < 90:
            return 2
        else:
            return 3
