from operators import Operator
from enemy import Enemy
from gear import Gear

# 🎮 Gear Catalog
gear_catalog = [
    Gear("Adrenaline Shot", "utility", noise=0, damage=0, effect="boost stamina", weight=2, rarity="Common", role_lock=None),
    Gear("Armor Plates", "utility", noise=0, damage=0, effect="reduce damage", weight=2, rarity="Common", role_lock=None),
    Gear("AR-33", "primary", noise=6, damage=8, effect=None, weight=1, rarity="Common", role_lock=None),
    Gear("Breach Charge", "utility", noise=10, damage=0, effect="force entry", weight=1, rarity="Common", role_lock=None),
    Gear("C4 Charge", "utility", noise=10, damage=0, effect="high-explosive", weight=3, rarity="Epic", role_lock="Assault"),
    Gear("Desert Eagle", "sidearm", noise=7, damage=6, effect="high power", weight=2, rarity="Common", role_lock=None),
    Gear("Drone", "gadget", noise=0, damage=0, effect="scout", weight=2, rarity="Common", role_lock=None),
    Gear("EMP", "utility", noise=0, damage=0, effect="disable electronics", weight=2, rarity="Common", role_lock=None),
    Gear("EMP Mine", "utility", noise=0, damage=0, effect="trap for electronics", weight=2, rarity="Epic", role_lock="Tech"),
    Gear("Five-Seven", "sidearm", noise=2, damage=4, effect="armor piercing", weight=1, rarity="Rare", role_lock=None),
    Gear("Flashbang", "utility", noise=0, damage=0, effect="stun", weight=1, rarity="Common", role_lock=None),
    Gear("Hacking Pad", "gadget", noise=0, damage=0, effect="multi-system override", weight=2, rarity="Epic", role_lock="Tech"),
    Gear("Holo Projector", "gadget", noise=0, damage=0, effect="decoy", weight=2, rarity="Common", role_lock=None),
    Gear("M4A1", "primary", noise=5, damage=7, effect=None, weight=2, rarity="Common", role_lock=None),
    Gear("Medkit", "utility", noise=0, damage=0, effect="heal", weight=2, rarity="Common", role_lock=None),
    Gear("Mini Drone", "gadget", noise=0, damage=0, effect="reveal enemies", weight=1, rarity="Common", role_lock=None),
    Gear("MK18 CQBR", "primary", noise=5, damage=8, effect="compact assault", weight=2, rarity="Rare", role_lock="Assault"),
    Gear("Motion Sensor", "gadget", noise=0, damage=0, effect="detect movement", weight=1, rarity="Rare", role_lock="Recon"),
    Gear("Nano Medkit", "utility", noise=0, damage=0, effect="heal + revive", weight=2, rarity="Legendary", role_lock="Medic"),
    Gear("Portable Cover", "utility", noise=0, damage=0, effect="reduce ranged damage", weight=3, rarity="Rare", role_lock="Defense"),
    Gear("Signal Jammer", "gadget", noise=0, damage=0, effect="block sensors", weight=2, rarity="Common", role_lock=None),
    Gear("Silenced Pistol", "sidearm", noise=2, damage=4, effect=None, weight=1, rarity="Common", role_lock=None),
    Gear("Smoke Grenade", "utility", noise=0, damage=0, effect="line-of-sight blocker", weight=1, rarity="Common", role_lock=None),
    Gear("SMG", "primary", noise=4, damage=6, effect=None, weight=1, rarity="Common", role_lock=None),
    Gear("Sniper Rifle", "primary", noise=8, damage=10, effect=None, weight=1, rarity="Common", role_lock=None),
    Gear("Sentry Gun", "gadget", noise=0, damage=0, effect="auto-fire defense", weight=4, rarity="Legendary", role_lock="Defense"),
    Gear("SPAS-12", "primary", noise=9, damage=10, effect="blast control", weight=3, rarity="Epic", role_lock="Assault"),
    Gear("Suppressed SMG", "primary", noise=2, damage=5, effect="silent fire", weight=2, rarity="Common", role_lock=None),
    Gear("Tactical Shotgun", "primary", noise=8, damage=9, effect="breach boost", weight=3, rarity="Common", role_lock=None),
    Gear("Vector .45", "primary", noise=3, damage=6, effect="rapid fire", weight=2, rarity="Rare", role_lock="Recon"),
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
       lambda: Enemy("PMC Sniper", "Sniper", 15, 9, "long_range"),
       lambda: Enemy("PMC Heavy", "Standard", 28, 6, "hold_position"),
       lambda: Enemy("Security Drone", "Drone", 12, 5, "surveil"),
       lambda: Enemy("Tech Operative", "Support", 16, 4, "boost")
    ],

    "Jungle": [
        lambda: Enemy("Militia Scout", "Standard", 18, 6, "patrol"),
        lambda: Enemy("Tracker", "Sniper", 14, 8, "long_range"),
        lambda: Enemy("Camouflaged Gunner", "Standard", 21, 7, "ambush"),
        lambda: Enemy("Booby Trap Setter", "Support", 16, 5, "trap"),
        lambda: Enemy("Insect Drone", "Drone", 10, 6, "surveil")
    ],

 "Arctic": [
    lambda: Enemy("Recon Drone", "Drone", 10, 6, "surveil"),
    lambda: Enemy("Snow Guard", "Standard", 22, 4, "patrol"),
    lambda: Enemy("Frost Sniper", "Sniper", 15, 9, "long_range"),
    lambda: Enemy("Cryo Engineer", "Support", 17, 4, "boost"),
    lambda: Enemy("Heavy Sled Trooper", "Standard", 26, 7, "hold_position")
],

    "Underground": [
    lambda: Enemy("Tunnel Patrol", "Standard", 18, 5, "patrol"),
    lambda: Enemy("Signal Operator", "Support", 16, 5, "boost"),
    lambda: Enemy("Claustro Drone", "Drone", 11, 5, "surveil"),
    lambda: Enemy("Mine Layer", "Support", 15, 4, "trap"),
    lambda: Enemy("Bunker Rifleman", "Standard", 22, 6, "hold_position")
],

    "Mountain": [
    lambda: Enemy("Sniper Scout", "Sniper", 14, 9, "long_range"),
    lambda: Enemy("Mountain Rifleman", "Standard", 20, 5, "patrol"),
    lambda: Enemy("Rock Guard", "Standard", 24, 6, "hold_position"),
    lambda: Enemy("Avalanche Drone", "Drone", 10, 6, "surveil"),
    lambda: Enemy("Comms Relay Tech", "Support", 16, 4, "boost")
],

   "Coastal": [
    lambda: Enemy("Merc Raider", "Standard", 20, 6, "patrol"),
    lambda: Enemy("Pier Sniper", "Sniper", 15, 9, "long_range"),
    lambda: Enemy("Beach Assault Bot", "Drone", 12, 6, "surveil"),
    lambda: Enemy("Harbor Heavy", "Standard", 26, 7, "hold_position"),
    lambda: Enemy("Tide Support Officer", "Support", 17, 5, "boost")
],

    "Desert": [
    lambda: Enemy("Desert Watchman", "Standard", 19, 6, "patrol"),
    lambda: Enemy("Command Drone", "Drone", 10, 6, "surveil"),
    lambda: Enemy("Sniper Jackal", "Sniper", 14, 9, "long_range"),
    lambda: Enemy("Dust Storm Gunner", "Standard", 23, 7, "hold_position"),
    lambda: Enemy("Supply Mule", "Support", 16, 4, "boost")
]

}

elite_enemies = {
    "Urban": [
        lambda: Enemy("PMC Enforcer", "Elite", 30, 8, "suppress"),
        lambda: Enemy("Urban Sniper Elite", "Sniper", 25, 11, "long_range"),
        lambda: Enemy("City Breacher", "Elite", 28, 7, "entry"),
        lambda: Enemy("Urban Hacker", "Support", 24, 5, "jam"),
        lambda: Enemy("Ballistic Shieldman", "Elite", 35, 6, "push")
    ],
    "Jungle": [
        lambda: Enemy("Militia Commander", "Elite", 28, 7, "ambush"),
        lambda: Enemy("Silent Marksman", "Sniper", 22, 10, "long_range"),
        lambda: Enemy("Jungle Phantom", "Elite", 26, 8, "flank"),
        lambda: Enemy("Tribal Warcaller", "Support", 23, 6, "boost"),
        lambda: Enemy("Stalker Unit", "Elite", 24, 9, "pursue")
    ],
    "Arctic": [
        lambda: Enemy("Frost Unit Alpha", "Elite", 30, 8, "suppress"),
        lambda: Enemy("Polar Sharpshooter", "Sniper", 23, 11, "long_range"),
        lambda: Enemy("Thermal Raider", "Elite", 28, 7, "entry"),
        lambda: Enemy("Blizzard Operator", "Support", 25, 5, "disrupt"),
        lambda: Enemy("Cryo Enforcer", "Elite", 32, 6, "slow")
    ],
    "Underground": [
        lambda: Enemy("Subterra Enforcer", "Elite", 27, 7, "hold_position"),
        lambda: Enemy("Deep Range Tech", "Sniper", 22, 10, "long_range"),
        lambda: Enemy("Sapper Veteran", "Elite", 28, 6, "trap"),
        lambda: Enemy("Burrower Scout", "Elite", 25, 7, "roam"),
        lambda: Enemy("Cave Howler", "Support", 23, 5, "alert")
    ],
    "Mountain": [
        lambda: Enemy("Summit Enforcer", "Elite", 29, 8, "patrol"),
        lambda: Enemy("Cliff Sniper Elite", "Sniper", 24, 11, "long_range"),
        lambda: Enemy("Rockfall Veteran", "Elite", 31, 7, "ambush"),
        lambda: Enemy("Oxygen Tech", "Support", 22, 4, "heal"),
        lambda: Enemy("Highlands Bruiser", "Elite", 33, 6, "push")
    ],
    "Coastal": [
        lambda: Enemy("Dockside Raider", "Elite", 28, 7, "suppress"),
        lambda: Enemy("Shoreline Marksman", "Sniper", 23, 10, "long_range"),
        lambda: Enemy("Port Saboteur", "Elite", 26, 6, "jam"),
        lambda: Enemy("Sea Guard Elite", "Standard", 30, 8, "hold_position"),
        lambda: Enemy("Coastal Tech", "Support", 24, 5, "boost")
    ],
    "Desert": [
        lambda: Enemy("Sandstorm Enforcer", "Elite", 30, 8, "patrol"),
        lambda: Enemy("Jackal Elite", "Sniper", 24, 10, "long_range"),
        lambda: Enemy("Sunblade Veteran", "Elite", 27, 7, "ambush"),
        lambda: Enemy("Nomad Support", "Support", 23, 5, "boost"),
        lambda: Enemy("Scorch Trooper", "Elite", 31, 6, "burn")
    ]
}


boss_enemies = {
    "Urban": [
        lambda: Enemy("Commander Varga", "Boss", 45, 10, "coordinate"),
        lambda: Enemy("The Architect", "Boss", 48, 8, "fortify"),
        lambda: Enemy("Specter Knox", "Boss", 42, 11, "flank"),
        lambda: Enemy("Chief Mauer", "Boss", 47, 9, "boost")
    ],
    "Jungle": [
        lambda: Enemy("Colonel Rojas", "Boss", 42, 9, "trap"),
        lambda: Enemy("The Warden", "Boss", 46, 8, "track"),
        lambda: Enemy("General Uko", "Boss", 44, 10, "ambush"),
        lambda: Enemy("Silent Beast", "Boss", 43, 11, "predator")
    ],
    "Arctic": [
        lambda: Enemy("Overseer Nyrov", "Boss", 44, 10, "boost"),
        lambda: Enemy("The Ice Claw", "Boss", 47, 9, "slow"),
        lambda: Enemy("Commander Reznik", "Boss", 45, 11, "precision"),
        lambda: Enemy("Frostbreaker", "Boss", 49, 8, "jam")
    ],
    "Underground": [
        lambda: Enemy("The Signal", "Boss", 40, 9, "jam"),
        lambda: Enemy("Warden Kreel", "Boss", 43, 10, "hold_position"),
        lambda: Enemy("Ghost Echo", "Boss", 45, 8, "disorient"),
        lambda: Enemy("Subnet", "Boss", 41, 11, "disable")
    ],
    "Mountain": [
        lambda: Enemy("Warlord Hesse", "Boss", 46, 11, "control"),
        lambda: Enemy("Stone Talon", "Boss", 48, 9, "suppress"),
        lambda: Enemy("High Sentinel", "Boss", 44, 10, "elevate"),
        lambda: Enemy("Peak Phantom", "Boss", 42, 12, "stealth")
    ],
    "Coastal": [
        lambda: Enemy("Admiral Tyvek", "Boss", 43, 10, "suppress"),
        lambda: Enemy("Breaker Vance", "Boss", 46, 9, "board"),
        lambda: Enemy("Captain Mira", "Boss", 45, 10, "coordinate"),
        lambda: Enemy("Riptide", "Boss", 47, 8, "flood")
    ],
    "Desert": [
        lambda: Enemy("The Jackal King", "Boss", 47, 11, "command"),
        lambda: Enemy("Windshear", "Boss", 44, 10, "disrupt"),
        lambda: Enemy("Mirage", "Boss", 43, 12, "mislead"),
        lambda: Enemy("Scarab", "Boss", 48, 9, "ambush")
    ]
}

