class Zone:
    def __init__(self, name, description, encounter=None, loot=None, next_zones=None):
        self.name = name
        self.description = description
        self.encounter = encounter  # Can be None or a dict
        self.loot = loot or []      # List of item names
        self.next_zones = next_zones or []  # Zone names this connects to
        self.cleared = False

    def show_info(self):
        print(f"\n🗺️ Zone: {self.name}")
        print(self.description)
        if self.loot:
            print(f"  🔍 Loot found: {', '.join(self.loot)}")
        if hasattr(self, "hazard") and self.hazard:
            print(f"  ⚠️ Environmental Hazard: {self.hazard}")
        if self.encounter and not self.cleared:
            print("  ⚠️ Threat detected here.")
        elif not self.encounter:
            print("  ✅ Clear.")
