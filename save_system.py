import pickle
import json
import os

SAVE_DIR = "saves"

def get_save_path(slot_name):
    return os.path.join(SAVE_DIR, f"{slot_name}.pkl")

def save_campaign(slot_name, campaign_state):
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(get_save_path(slot_name), "wb") as f:
        pickle.dump(campaign_state, f)
    print(f"💾 Campaign '{slot_name}' saved.")

def load_campaign(slot_name):
    path = get_save_path(slot_name)
    if not os.path.exists(path):
        print("❌ Save not found.")
        return None
    with open(path, "rb") as f:
        print(f"📂 Loaded campaign '{slot_name}'")
        return pickle.load(f)

def list_saves():
    if not os.path.exists(SAVE_DIR):
        return []
    return [f[:-4] for f in os.listdir(SAVE_DIR) if f.endswith(".pkl")]


MISSION_DIR = "data"
os.makedirs(MISSION_DIR, exist_ok=True)

def get_mission_json_path():
    return os.path.join(MISSION_DIR, "missions.json")


def load_missions_from_json():
    path = get_mission_json_path()
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        raw = json.load(f)
        from mission import Mission  # to avoid circular imports
        return {
            name: Mission(name, data["objective"], data["location"], data["difficulty"],
                          data["enemies"], data["intel_level"], data["terrain"], data["terrain_effect"])
            for name, data in raw.items()
        }
