import random

class Enemy:
    def __init__(self, name, type_, hp, accuracy, behavior, threat_level=1):
        self.name = name
        self.type = type_
        self.hp = hp
        self.max_hp = hp
        self.accuracy = accuracy
        self.behavior = behavior  # e.g., 'patrol', 'long_range', 'surveil', etc.
        self.threat_level = threat_level
        self.status = "Active"

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.status = "Down"
            self.hp = 0
            print(f"{self.name} eliminated.")
        else:
            print(f"{self.name} hit! {self.hp} HP remaining.")

    def act(self, squad):
        if not self.is_alive():
            return None

        print(f"\n🎯 {self.name} ({self.behavior}) takes action!")

        if self.behavior == "patrol":
            target = self.choose_target(squad)
            self.attack(target)

        elif self.behavior == "long_range":
            target = self.choose_target(squad, priority="low_hp")
            self.attack(target)

        elif self.behavior == "boost":
            print(f"📢 {self.name} issues tactical orders — enemy accuracy boosted!")
            return "boost"

        elif self.behavior == "surveil":
            print(f"👁️ {self.name} scans the field — alert increased!")
            return "alert_up"

    def choose_target(self, squad, priority=None):
        alive = [op for op in squad if op.is_alive()]
        if not alive:
            return None
        if priority == "low_hp":
            return min(alive, key=lambda x: x.health)
        return random.choice(alive)

    def attack(self, target):
        if not target:
            return

        roll = random.randint(1, 10)
        total = self.accuracy + roll
        print(f"🎲 {self.name} rolls {self.accuracy} + {roll} = {total}")

        if total >= 12:
            dmg = random.randint(15, 30)
            print(f"💥 {target.codename} hit for {dmg} damage!")
            target.apply_damage(dmg)
        else:
            print(f"🫣 {self.name} missed {target.codename}!")
