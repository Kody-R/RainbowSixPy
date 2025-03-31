from operators import Operator
from mission import Mission
from gear import Gear
from mission_map import Zone

# 🎮 Gear Catalog
gear_catalog = [
    Gear("AR-33", "primary", noise=6, damage=8),
    Gear("Silenced Pistol", "sidearm", noise=2, damage=4),
    Gear("SMG", "primary", noise=4, damage=6),
    Gear("Sniper Rifle", "primary", noise=8, damage=10),
    Gear("Drone", "gadget", effect="scout", weight=2),
    Gear("Medkit", "utility", effect="heal", weight=2),
    Gear("EMP", "utility", effect="disable electronics", weight=2),
    Gear("Breach Charge", "utility", effect="force entry", noise=10),
]

# 🔍 Helper function to get gear by name
def find_gear(name):
    for g in gear_catalog:
        if g.name == name:
            return g
    return None

# 🎖 Operators (with gear assigned via method)
op1 = Operator("John Clark", "SIX", "Commander", stealth=7, marksmanship=8, tech=5, leadership=10, stamina=9)
op1.assign_gear(find_gear("Silenced Pistol"))
op1.assign_gear(find_gear("Drone"))

op2 = Operator("Ding Chavez", "CHARGER", "Assault", stealth=6, marksmanship=9, tech=4, leadership=7, stamina=8)
op2.assign_gear(find_gear("AR-33"))
op2.assign_gear(find_gear("Breach Charge"))

op3 = Operator("Dietrich", "DOC", "Medic", stealth=5, marksmanship=6, tech=6, leadership=5, stamina=7)
op3.assign_gear(find_gear("SMG"))
op3.assign_gear(find_gear("Medkit"))

op4 = Operator("Louis Loiselle", "GHOST", "Recon", stealth=9, marksmanship=7, tech=5, leadership=4, stamina=9)
op4.assign_gear(find_gear("Sniper Rifle"))
op4.assign_gear(find_gear("Drone"))

op5 = Operator("Gustavo", "WIREFRAME", "Hacker", stealth=7, marksmanship=5, tech=10, leadership=5, stamina=6)
op5.assign_gear(find_gear("Silenced Pistol"))
op5.assign_gear(find_gear("EMP"))

op6 = Operator("Karen", "VIPER", "Infiltrator", stealth=10, marksmanship=6, tech=7, leadership=4, stamina=8)
op6.assign_gear(find_gear("SMG"))
op6.assign_gear(find_gear("EMP"))

operators = [op1, op2, op3, op4, op5, op6]

# 🎯 Missions
missions = [
    Mission("Operation Silent Storm", "Infiltrate and extract hostage", "Zurich, Switzerland", "Medium",
            enemies="Heavy Guard Patrol", intel_level="Moderate", required_roles=["Infiltrator", "Medic"]),
    Mission("Operation Iron Dagger", "Sabotage arms shipment", "Sao Paulo, Brazil", "Hard",
            enemies="Militia + Armed Drones", intel_level="Low", required_roles=["Hacker", "Assault"]),
    Mission("Operation Ghost Fang", "Assassinate cartel leader and exfil undetected", "Tijuana, Mexico", "Hard",
            enemies="Bodyguards + Sniper", intel_level="High", required_roles=["Sniper", "Commander"]),
    Mission("Operation Broken Silence", "Secure secret documents from embassy", "Berlin, Germany", "Medium",
            enemies="CCTV + Armed Guards", intel_level="Low", required_roles=["Hacker", "Recon"]),
    Mission("Operation Midnight Watch", "Prevent chemical weapon detonation", "London, UK", "Very Hard",
            enemies="Terrorists with timed device", intel_level="Minimal", required_roles=["Commander", "Tech"])
]

# 🗺️ Mission Maps
mission_maps = {
    "Operation Silent Storm": {
        "Entry Point": Zone(
            name="Entry Point",
            description="A dark alley leading to the compound's side door.",
            encounter={"type": "stealth"},
            next_zones=["Hallway"]
        ),
        "Hallway": Zone(
            name="Hallway",
            description="A dim hallway with footstep echoes and a flickering light.",
            encounter={"type": "tech"},
            loot=["Intel Folder"],
            next_zones=["Server Room", "Barracks"]
        ),
        "Server Room": Zone(
            name="Server Room",
            description="The main hub of communications — buzzing with electronics.",
            encounter={"type": "tech"},
            loot=["Data Stick"],
            next_zones=["Extraction"]
        ),
        "Barracks": Zone(
            name="Barracks",
            description="Enemy sleeping quarters. Some gear may be stashed here.",
            loot=["EMP", "Medkit"],
            next_zones=["Extraction"]
        ),
        "Extraction": Zone(
            name="Extraction",
            description="The rooftop helipad where evac will arrive.",
            next_zones=[]
        )
    }
}
