class Gear:
    def __init__(self, name, type_, noise=0, damage=0, effect=None, weight=1):
        self.name = name
        self.type = type_  # e.g. 'primary', 'sidearm', 'utility', 'gadget'
        self.noise = noise  # 0 = silent, 10 = loud
        self.damage = damage
        self.effect = effect  # a function or string to trigger effect
        self.weight = weight

    def __str__(self):
        return (f"{self.name} [{self.type}]\n"
                f"  Damage: {self.damage}, Noise: {self.noise}, Weight: {self.weight}\n"
                f"  Effect: {self.effect if self.effect else 'None'}")
