import random
import json
import os

from mission import Mission
from mission_map import Zone

# === Load External JSONs ===
def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

BASE_DIR = os.path.dirname(__file__)
LOCATION_PATH = os.path.join(BASE_DIR, "location.json")
ENEMIES_PATH = os.path.join(BASE_DIR, "enemy.json")

LOCATION_ENVIRONMENTS = load_json(LOCATION_PATH)
RAW_ENEMIES = load_json(ENEMIES_PATH)

# === Derived Mappings ===
LOCATIONS = [loc for terrain_locs in LOCATION_ENVIRONMENTS.values() for loc in terrain_locs]
location_to_terrain = {
    loc: terrain for terrain, locs in LOCATION_ENVIRONMENTS.items() for loc in locs
}

ENVIRONMENTS = {
    "Urban": {"tech_bonus": 1},
    "Jungle": {"stealth_bonus": 1, "tech_penalty": 1},
    "Arctic": {"marksmanship_penalty": 1, "stamina_penalty": 1},
    "Underground": {"tech_bonus": 2, "stealth_penalty": 1},
    "Mountain": {"stamina_bonus": 1, "marksmanship_bonus": 1},
    "Coastal": {},
    "Desert": {"tech_penalty": 1, "marksmanship_bonus": 1},
    "Transit": {"tech_bonus": 1,"stamina_penalty": 1,"stealth_penalty": 1},
    "Entertainment": {"stealth_bonus": 1,"marksmanship_penalty": 1,"leadership_bonus": 1}
}

OBJECTIVE_CHAINS = [
    ["Infiltrate compound", "Secure server room", "Extract via helipad"],
    ["Sabotage radar array", "Evade patrols", "Destroy weapons cache"],
    ["Neutralize HVT", "Plant tracking device", "Escape undetected"],
    ["Hack drone uplink", "Retrieve intel", "Regroup at rendezvous"],
    ["Breach facility gate", "Disable comms array", "Exfil via convoy"],
    ["Interrogate captured officer", "Secure data terminal", "Escape through sewer system"],
    ["Locate hostage", "Disarm perimeter traps", "Extract to safehouse"],
    ["Disable surveillance grid", "Plant false intel", "Exit without alerting guards"],
    ["Secure forward outpost", "Establish signal beacon", "Hold position until evac"],
    ["Intercept smuggler convoy", "Recover stolen tech", "Call in extraction"],
    ["Hack local network", "Upload virus", "Escape before lockdown"],
    ["Find and tag weapons cache", "Neutralize defenders", "Mark for airstrike"],
    ["Gain access via roof", "Take control of control room", "Clear extraction zone"],
    ["Jam radar dish", "Board enemy vehicle", "Plant explosive and escape"],
    ["Scout facility", "Map patrol routes", "Eliminate key targets"]
]


INTEL_LEVELS = ["Minimal", "Low", "Medium", "High"]

ADJECTIVES = ["Iron", "Shadow", "Crimson", "Phantom", "Silent", "Night", "Ghost", "Cold", "Obsidian"]
NOUNS = ["Fang", "Storm", "Blade", "Whisper", "Hammer", "Pulse", "Hawk", "Net", "Spire", "Warden"]

MISSION_TYPES = {
    "Extract": "🚁️ Extraction",
    "Sabotage": "💣 Sabotage",
    "Hack": "💻 Cyber",
    "Neutralize": "🔫 Assault",
    "Rescue": "🚑 Rescue",
    "Destroy": "🔥 Demolition"
}

def infer_mission_type(objective_chain):
    first = objective_chain[0].lower()
    if "extract" in first:
        return "Extraction"
    if "sabotage" in first:
        return "Sabotage"
    if "hack" in first:
        return "Cyber"
    if "neutralize" in first or "kill" in first:
        return "Assault"
    if "rescue" in first:
        return "Rescue"
    if "destroy" in first:
        return "Demolition"
    return "Unknown"

def generate_codename():
    return f"Operation {random.choice(ADJECTIVES)} {random.choice(NOUNS)}"

def get_dynamic_loot(encounter_type, alert_level):
    stealth = ["Silenced Pistol", "Mini Drone", "EMP", "Holo Projector"]
    combat = ["Armor Plates", "Medkit", "Flashbang", "C4 Charge"]
    tech = ["Hacking Pad", "Signal Jammer", "EMP Mine"]

    if alert_level < 30:
        if encounter_type == "stealth":
            return random.sample(stealth, k=1)
        elif encounter_type == "tech":
            return random.sample(tech, k=1)
    return random.sample(combat, k=1)

def generate_random_mission(index):
    location = random.choice(LOCATIONS)
    terrain = location_to_terrain.get(location, "Urban")
    terrain_effect = ENVIRONMENTS.get(terrain, {})
    objective_steps = random.choice(OBJECTIVE_CHAINS)
    difficulty = random.choice(["Medium", "Hard", "Very Hard"])

    # Enemy name (basic summary string)
    enemy_pool = RAW_ENEMIES.get(terrain, {}).get("regular", [])
    enemies = random.choice(enemy_pool)["name"] if enemy_pool else "Unknown Hostiles"

    intel = random.choice(INTEL_LEVELS)
    name = generate_codename()

    zone_names = ["Entry Point"] + [f"{step}" for step in objective_steps] + ["Extraction"]
    map_data = {}

    for i, zname in enumerate(zone_names):
        encounter_type = random.choice(["tech", "stealth", "marksmanship"])
        alert = random.randint(0, 100)
        loot = get_dynamic_loot(encounter_type, alert_level=alert)
        next_zones = [zone_names[i + 1]] if i + 1 < len(zone_names) else []

        zone_enemies = random.sample(enemy_pool, k=min(2, len(enemy_pool))) if enemy_pool else []

        z = Zone(
            name=zname,
            description=f"Zone Objective: {zname} — in {terrain} terrain.",
            encounter={"type": encounter_type} if zname != "Extraction" else None,
            loot=loot,
            next_zones=next_zones
        )
        z.enemies = zone_enemies
        map_data[zname] = z

    mission_type = infer_mission_type(objective_steps)
    mission = Mission(name, ", ".join(objective_steps), location, difficulty, enemies, intel, terrain, terrain_effect)
    mission.terrain = terrain
    mission.terrain_effect = terrain_effect
    mission.mission_type = mission_type
    return mission, map_data