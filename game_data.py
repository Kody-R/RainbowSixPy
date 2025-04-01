from operators import Operator
from enemy import Enemy
from gear import Gear

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
    Gear("M4A1", "primary", noise=5, damage=7, weight=2),
    Gear("Suppressed SMG", "primary", noise=2, damage=5, effect="silent fire", weight=2),
    Gear("Desert Eagle", "sidearm", noise=7, damage=6, effect="high power", weight=2),
    Gear("Tactical Shotgun", "primary", noise=8, damage=9, effect="breach boost", weight=3),
    Gear("Flashbang", "utility", effect="stun", weight=1),
    Gear("Armor Plates", "utility", effect="reduce damage", weight=2),
    Gear("Adrenaline Shot", "utility", effect="boost stamina", weight=2),
    Gear("Holo Projector", "gadget", effect="decoy", weight=2),
    Gear("Mini Drone", "gadget", effect="reveal enemies", weight=1),
    Gear("Signal Jammer", "gadget", effect="block sensors", weight=2),
    Gear("Vector .45", "primary", noise=3, damage=6, effect="rapid fire", weight=2, rarity="Rare", role_lock="Recon"),
    Gear("MK18 CQBR", "primary", noise=5, damage=8, effect="compact assault", weight=2, rarity="Rare", role_lock="Assault"),
    Gear("Five-Seven", "sidearm", noise=2, damage=4, effect="armor piercing", weight=1, rarity="Rare"),
    Gear("SPAS-12", "primary", noise=9, damage=10, effect="blast control", weight=3, rarity="Epic", role_lock="Assault"),
    Gear("C4 Charge", "utility", effect="high-explosive", noise=10, weight=3, rarity="Epic", role_lock="Assault"),
    Gear("Smoke Grenade", "utility", effect="line-of-sight blocker", weight=1, rarity="Common"),
    Gear("Motion Sensor", "gadget", effect="detect movement", weight=1, rarity="Rare", role_lock="Recon"),
    Gear("Hacking Pad", "gadget", effect="multi-system override", weight=2, rarity="Epic", role_lock="Tech"),
    Gear("Sentry Gun", "gadget", effect="auto-fire defense", weight=4, rarity="Legendary", role_lock="Defense"),
    Gear("Nano Medkit", "utility", effect="heal + revive", weight=2, rarity="Legendary", role_lock="Medic"),
    Gear("EMP Mine", "utility", effect="trap for electronics", weight=2, rarity="Epic", role_lock="Tech"),
    Gear("Portable Cover", "utility", effect="reduce ranged damage", weight=3, rarity="Rare", role_lock="Defense"),
]

# 🔍 Helper function to get gear by name
def find_gear(name):
    for g in gear_catalog:
        if g.name == name:
            return g
    return None

# 🎖 Operators (with gear assigned via method)
op1 = Operator("Domingo Chavez", "CHAVEZ", "Assault", stealth=6, marksmanship=9, tech=4, leadership=8, stamina=8, ability="Breach Expert")
op1.assign_gear(find_gear("AR-33"))
op1.assign_gear(find_gear("Breach Charge"))

op2 = Operator("Sam Driscoll", "HAWK", "Recon", stealth=9, marksmanship=7, tech=4, leadership=5, stamina=9, ability="Intel Scanner")
op2.assign_gear(find_gear("Silenced Pistol"))
op2.assign_gear(find_gear("Mini Drone"))

op3 = Operator("Dieter Weber", "WEBER", "Sniper", stealth=7, marksmanship=10, tech=3, leadership=6, stamina=7, ability="Sharpshooter")
op3.assign_gear(find_gear("Sniper Rifle"))
op3.assign_gear(find_gear("Drone"))

op4 = Operator("Eddie Price", "FALCON", "Commander", stealth=5, marksmanship=8, tech=6, leadership=10, stamina=7, ability="Tactical Boost")
op4.assign_gear(find_gear("Silenced Pistol"))
op4.assign_gear(find_gear("Adrenaline Shot"))

op5 = Operator("Louis Loiselle", "GHOST", "Recon", stealth=10, marksmanship=7, tech=5, leadership=4, stamina=9,ability="Silent Strike")
op5.assign_gear(find_gear("Suppressed SMG"))
op5.assign_gear(find_gear("Holo Projector"))

op6 = Operator("Tim Noonan", "LINK", "Tech", stealth=4, marksmanship=5, tech=10, leadership=6, stamina=6,ability="System Cracker")
op6.assign_gear(find_gear("EMP"))
op6.assign_gear(find_gear("Signal Jammer"))

op7 = Operator("Michael Granger", "BULLDOG", "Assault", stealth=4, marksmanship=8, tech=5, leadership=7, stamina=9,ability="Shock & Awe")
op7.assign_gear(find_gear("Tactical Shotgun"))
op7.assign_gear(find_gear("Flashbang"))

op8 = Operator("David Foster", "DOC", "Medic", stealth=5, marksmanship=6, tech=7, leadership=6, stamina=7,ability="Combat Medic")
op8.assign_gear(find_gear("SMG"))
op8.assign_gear(find_gear("Medkit"))

op9 = Operator("Antonio Ortega", "EDGE", "Infiltrator", stealth=10, marksmanship=6, tech=6, leadership=5, stamina=8,ability="Adaptive Ops")
op9.assign_gear(find_gear("SMG"))
op9.assign_gear(find_gear("EMP"))

op10 = Operator("Gus Werenski", "WATCHDOG", "Defense", stealth=6, marksmanship=7, tech=5, leadership=6, stamina=7,ability="Fortify")
op10.assign_gear(find_gear("AR-33"))
op10.assign_gear(find_gear("Armor Plates"))

# Default operator setup
default_operators = [op1, op2, op3, op4, op5, op6, op7, op8, op9, op10]

# Load from save or fallback to default
operators = default_operators


TYPE_ICONS = {
    "Extraction": "🛩️",
    "Sabotage": "💣",
    "Cyber": "💻",
    "Assault": "🔫",
    "Rescue": "🚑",
    "Demolition": "🔥",
    "Unknown": "❓"
}

# Define terrain-appropriate enemy pools
TERRAIN_ENEMIES = {
    "Urban": [
        lambda: Enemy("PMC Rifleman", "Standard", 20, 5, "patrol"),
        lambda: Enemy("PMC Sniper", "Sniper", 15, 9, "long_range")
    ],
    "Jungle": [
        lambda: Enemy("Militia Scout", "Standard", 18, 6, "patrol"),
        lambda: Enemy("Tracker", "Sniper", 14, 8, "long_range")
    ],
    "Arctic": [
        lambda: Enemy("Recon Drone", "Drone", 10, 6, "surveil"),
        lambda: Enemy("Snow Guard", "Standard", 22, 4, "patrol")
    ],
    "Underground": [
        lambda: Enemy("Tunnel Patrol", "Standard", 18, 5, "patrol"),
        lambda: Enemy("Signal Operator", "Support", 16, 5, "boost")
    ],
    "Mountain": [
        lambda: Enemy("Sniper Scout", "Sniper", 14, 9, "long_range")
    ],
    "Coastal": [
        lambda: Enemy("Merc Raider", "Standard", 20, 6, "patrol")
    ],
    "Desert": [
        lambda: Enemy("Desert Watchman", "Standard", 19, 6, "patrol"),
        lambda: Enemy("Command Drone", "Drone", 10, 6, "surveil")
    ]
}