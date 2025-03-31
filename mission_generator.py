import random
from mission import Mission
from mission_map import Zone

# === Data ===

ENVIRONMENTS = {
    "Urban": {"tech_bonus": 1},
    "Jungle": {"stealth_bonus": 1, "tech_penalty": 1},
    "Arctic": {"marksmanship_penalty": 1, "stamina_penalty": 1},
    "Underground": {"tech_bonus": 2, "stealth_penalty": 1},
    "Mountain": {"stamina_bonus": 1, "marksmanship_bonus": 1},
    "Coastal": {},
    "Desert": {"tech_penalty": 1, "marksmanship_bonus": 1},
}

LOCATIONS = [
    "Amazon Jungle Outpost", "Arctic Research Base", "Oil Rig, North Sea",
    "Kremlin, Moscow", "Eiffel Tower, Paris", "UN HQ, New York",
    "Colosseum, Rome", "Pentagon, USA", "Cargo Ship - Pacific",
    "Underground Bunker, Iceland", "Cheyenne Mountain Complex",
    "Island Fortress, Philippines", "Desert Base, Libya"
]

LOCATION_ENVIRONMENTS = {
    "Amazon Jungle Outpost": "Jungle",
    "Arctic Research Base": "Arctic",
    "Oil Rig, North Sea": "Coastal",
    "Kremlin, Moscow": "Urban",
    "Eiffel Tower, Paris": "Urban",
    "UN HQ, New York": "Urban",
    "Colosseum, Rome": "Urban",
    "Pentagon, USA": "Underground",
    "Cargo Ship - Pacific": "Coastal",
    "Underground Bunker, Iceland": "Underground",
    "Cheyenne Mountain Complex": "Mountain",
    "Island Fortress, Philippines": "Coastal",
    "Desert Base, Libya": "Desert"
}

OBJECTIVE_CHAINS = [
    ["Infiltrate compound", "Secure server room", "Extract via helipad"],
    ["Sabotage radar array", "Evade patrols", "Destroy weapons cache"],
    ["Neutralize HVT", "Plant tracking device", "Escape undetected"],
    ["Hack drone uplink", "Retrieve intel", "Regroup at rendezvous"]
]

ENEMY_TYPES = [
    "PMC Guards", "Narco Militia", "Corrupt Soldiers", "Tech Cultists",
    "Urban Terror Cell", "Biohazard Researchers", "Smugglers", "AI Defense Grid"
]

INTEL_LEVELS = ["Minimal", "Low", "Medium", "High"]

ADJECTIVES = ["Iron", "Shadow", "Crimson", "Phantom", "Silent", "Night", "Ghost", "Cold", "Obsidian"]
NOUNS = ["Fang", "Storm", "Blade", "Whisper", "Hammer", "Pulse", "Hawk", "Net", "Spire", "Warden"]

MISSION_TYPES = {
    "Extract": "🛩️ Extraction",
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

# === Generator ===

def generate_random_mission(index):
    location = random.choice(LOCATIONS)
    terrain = LOCATION_ENVIRONMENTS.get(location, "Urban")
    terrain_effect = ENVIRONMENTS.get(terrain, {})
    objective_steps = random.choice(OBJECTIVE_CHAINS)
    difficulty = random.choice(["Medium", "Hard", "Very Hard"])
    enemies = random.choice(ENEMY_TYPES)
    intel = random.choice(INTEL_LEVELS)
    name = generate_codename()

    # Create zones
    zone_names = ["Entry Point"] + [f"{step}" for step in objective_steps] + ["Extraction"]
    map_data = {}

    for i, zname in enumerate(zone_names):
        encounter_type = random.choice(["tech", "stealth", "marksmanship"])
        alert = random.randint(0, 100)
        loot = get_dynamic_loot(encounter_type, alert_level=alert)
        next_zones = [zone_names[i + 1]] if i + 1 < len(zone_names) else []
        map_data[zname] = Zone(
            name=zname,
            description=f"Zone Objective: {zname} — in {terrain} terrain.",
            encounter={"type": encounter_type} if zname != "Extraction" else None,
            loot=loot,
            next_zones=next_zones
        )

    mission_type = infer_mission_type(objective_steps)
    mission = Mission(name, ", ".join(objective_steps), location, difficulty, enemies, intel, terrain, terrain_effect)
    mission.terrain = terrain
    mission.terrain_effect = terrain_effect
    mission.mission_type = mission_type 
    return mission, map_data
