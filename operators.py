class Operator:
    def __init__(self, name, codename, role, stealth, marksmanship, tech, leadership, stamina):
        self.name = name
        self.codename = codename
        self.role = role
        self.stealth = stealth
        self.marksmanship = marksmanship
        self.tech = tech
        self.leadership = leadership
        self.stamina = stamina
        self.health = 100
        self.status = "Active"
        self.primary = None
        self.sidearm = None
        self.gadgets = []  # gadgets/utilities
        self.max_gear_weight = 6  # max carry weight
        
    def is_alive(self):
        return self.health > 0

    def apply_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.status = "KIA"
            self.health = 0
        elif self.health <= 30:
            self.status = "Critical"
        elif self.health <= 60:
            self.status = "Wounded"
        elif self.health <= 85:
            self.status = "Lightly Injured"
        else:
            self.status = "Active"

    def current_loadout_weight(self):
        weight = 0
        if self.primary:
            weight += self.primary.weight
        if self.sidearm:
            weight += self.sidearm.weight
        for g in self.gadgets:
            weight += g.weight
        return weight

    def assign_gear(self, item):
        if self.current_loadout_weight() + item.weight > self.max_gear_weight:
            print(f"{self.codename} can't carry more weight!")
            return False

        if item.type == "primary":
            self.primary = item
        elif item.type == "sidearm":
            self.sidearm = item
        elif item.type in ("gadget", "utility"):
            self.gadgets.append(item)
        return True

    def get_gear_names(self):
        names = []
        if self.primary:
            names.append(self.primary.name)
        if self.sidearm:
            names.append(self.sidearm.name)
        names.extend([g.name for g in self.gadgets])
        return names

    def __str__(self):
        return (f"{self.codename} ({self.name}) - {self.role}\n"
                f"  Stealth: {self.stealth}  Marksmanship: {self.marksmanship}\n"
                f"  Tech: {self.tech}  Leadership: {self.leadership}  Stamina: {self.stamina}\n"
                f"  Health: {self.health}  Status: {self.status}\n"
                 f"  Loadout: {', '.join(self.get_gear_names()) if self.get_gear_names() else 'None'}")
    
    def use_equipment(self, item_name):
        if item_name in self.equipment:
            print(f"{self.codename} used {item_name}.")
            self.equipment.remove(item_name)
            return True
        else:
            print(f"{self.codename} does not have {item_name}.")
            return False

    def heal(self, amount):
        if self.health <= 0:
            print(f"{self.codename} is KIA and can't be healed.")
            return
        self.health += amount
        if self.health > 100:
            self.health = 100
        print(f"{self.codename} healed to {self.health} HP.")
        self.apply_damage(0)  # Re-evaluate status

    def clear_gear(self):
        self.primary = None
        self.sidearm = None
        self.gadgets = []

