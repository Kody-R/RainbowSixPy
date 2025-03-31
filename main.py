from game_data import operators, missions, gear_catalog, mission_maps
from utils import calculate_synergy_bonus
from mission_state import MissionState
import random

def show_operators():
    print("\n--- OPERATOR ROSTER ---")
    for idx, op in enumerate(operators, 1):
        print(f"[{idx}] {op.codename} ({op.role})")

def choose_team(required_roles):
    team = []
    print("\nSelect 2–4 operators by number (separated by space):")
    show_operators()
    indices = input("Your team: ").split()

    for i in indices:
        try:
            selected = operators[int(i) - 1]
            team.append(selected)
        except:
            print(f"Invalid index: {i}")

    if not (2 <= len(team) <= 4):
        print("Team must be 2–4 members.")
        return None

    # Check required roles
    team_roles = [op.role for op in team]
    for req in required_roles:
        if req not in team_roles:
            print(f"Missing required role: {req}")
            return None

    print("\nTeam confirmed:")
    for op in team:
        print(f" - {op.codename} ({op.role})")
    return team

def equip_team(team):
    print("\n--- GEAR LOADOUT ---")
    from game_data import gear_catalog

    for op in team:
        print(f"\nCurrent loadout for {op.codename}: {', '.join(op.get_gear_names()) or 'None'}")
        change = input(f"Would you like to change {op.codename}'s loadout? (y/n): ").strip().lower()

        if change != 'y':
            continue
        
        op.clear_gear()
        # Show gear catalog
        print("\nAvailable Gear:")
        for idx, g in enumerate(gear_catalog, 1):
            print(f"[{idx}] {g.name} [{g.type}] — Damage: {g.damage}, Noise: {g.noise}, Effect: {g.effect or 'None'}, Weight: {g.weight}")

        print(f"Max allowed gear weight: {op.max_gear_weight}")
        print("Enter gear numbers separated by space (primary, sidearm, then utilities/gadgets):")
        indices = input("Your choices: ").split()

        # Reset gear (soft reset — just remove previous and reassign from scratch)
        op.primary = None
        op.sidearm = None
        op.gadgets = []

        for i in indices:
            try:
                gear = gear_catalog[int(i) - 1]
                if not op.assign_gear(gear):
                    print(f"Skipping {gear.name} due to weight limit.")
            except:
                continue


def explore_mission(team, mission):
    state = MissionState()
    zones = mission_maps[mission.name]
    current_zone = zones["Entry Point"]
    visited = set()

    while current_zone:
        current_zone.show_info()
        if current_zone.name not in visited:
            visited.add(current_zone.name)

        # Handle encounter
        if current_zone.encounter and not current_zone.cleared:
            handle_zone_encounter(team, current_zone,state)
            current_zone.cleared = True

        # Loot
        if current_zone.loot:
            print("Collecting loot...")
            for op in team:
                for item in current_zone.loot:
                    # Give items to first op with space
                    if len(op.gadgets) < 2:
                        from game_data import gear_catalog
                        for g in gear_catalog:
                            if g.name == item:
                                op.assign_gear(g)
                                print(f"{op.codename} collected {item}")
                                break
                        break
            current_zone.loot = []

        # Move to next zone
        if not current_zone.next_zones:
            print("🚁 Mission complete — reached extraction!")
            break

        print(f"\n📶 Current Alert Level: {state.alert}/100")
        print("\nAvailable paths:")
        for idx, nz in enumerate(current_zone.next_zones, 1):
            print(f"{idx}. {nz}")
        choice = int(input("Choose your path: ")) - 1
        current_zone = zones[current_zone.next_zones[choice]]


def mission_encounter(team):
    print("\n--- Mission In Progress ---")
    encounters = [
        {"desc": "Locked door ahead. Hack or breach?", "type": "tech"},
        {"desc": "Guard patrol. Sneak past or engage?", "type": "stealth"},
        {"desc": "Camera system detected. Avoid or disable?", "type": "tech"},
        {"desc": "Intel stash found. Secure or ignore?", "type": "marksmanship"},
        {"desc": "Enemy entrenched. Suppress or flank?", "type": "marksmanship"},
        {"desc": "Tripwire detected. EMP or disarm?", "type": "tech"}
    ]

    for encounter in random.sample(encounters, 3):
        print(f"\nEncounter: {encounter['desc']}")
        print("Team:")
        for idx, op in enumerate(team, 1):
            print(f"[{idx}] {op.codename} ({op.status}) — HP: {op.health} — Gear: {', '.join(op.get_gear_names())}")

        idx = int(input("Choose an operator by number: ")) - 1
        op = team[idx]

        print("\nChoose action:")
        print("1. Attempt normally")
        print("2. Use gear item")
        action = input("Choice: ")

        used_gear = None
        if action == "2":
            if not op.gadgets:
                print("No gadgets available. Proceeding normally.")
            else:
                print(f"Gadgets: {', '.join([g.name for g in op.gadgets])}")
                item_name = input("Enter item name to use: ").strip()
                for g in op.gadgets:
                    if g.name.lower() == item_name.lower():
                        used_gear = g
                        op.gadgets.remove(g)
                        print(f"{op.codename} used {g.name}.")
                        break
                else:
                    print("Invalid item name. Proceeding normally.")

        # Apply gear effects
        bonus = 0
        auto_success = False

        if used_gear:
            if used_gear.name.lower() == "drone":
                print("📡 Drone boosts situational awareness.")
                bonus += 3
            elif used_gear.name.lower() == "emp" and encounter["type"] == "tech":
                print("✔️ EMP bypassed the electronic system. Encounter skipped.")
                continue
            elif used_gear.name.lower() == "medkit":
                op.heal(30)
                continue
            elif used_gear.name.lower() == "breach charge":
                print("💥 Forced entry, but noisy! Success guaranteed, enemy alerted.")
                auto_success = True
                op.apply_damage(random.randint(5, 20))  # loud breach has risk
                continue

        # Stat resolution
        stat = getattr(op, encounter["type"])
        roll = random.randint(1, 10)
        synergy = calculate_synergy_bonus(op, encounter["type"])
        success_chance = stat + roll + bonus + synergy
        print(f"🎯 Roll = {stat} + {roll} + gear bonus({bonus}) + synergy({synergy}) = {success_chance}")


        print(f"{op.codename} rolls {stat} + {roll} + bonus({bonus}) = {success_chance}")

        if auto_success or success_chance >= 12:
            print("✔️ Silent Success!")
        elif 9 <= success_chance < 12:
            print("⚠️ Partial Success. Enemy alerted.")
            op.apply_damage(random.randint(5, 15))
        else:
            print("❌ Failure! You’ve been engaged.")
            dmg = random.randint(20, 40)
            op.apply_damage(dmg)
            if not op.is_alive():
                print(f"☠️ {op.codename} is KIA!")

    print("\n--- Mission Summary ---")
    for op in team:
        print(f"{op.codename}: {op.health} HP — {op.status}")

def handle_zone_encounter(team, zone, state):
    print("\n⚔️ Zone Encounter:")
    encounter = zone.encounter
    encounter_type = encounter["type"]
    print(f"\n⚔️ Zone Encounter ({encounter_type.upper()}) — Alert Level: {state.alert}/100")

    for idx, op in enumerate(team, 1):
        print(f"[{idx}] {op.codename} — HP: {op.health} — {op.status}")

    op = team[int(input("Choose an operator by number: ")) - 1]

    print("1. Attempt normally\n2. Use gadget")
    choice = input("Choice: ")

    bonus = 0
    if choice == "2" and op.gadgets:
        print(f"Gadgets: {', '.join([g.name for g in op.gadgets])}")
        item = input("Use which gadget? ").strip()
        used = None
        for g in op.gadgets:
            if g.name.lower() == item.lower():
                used = g
                op.gadgets.remove(g)
                break

        if used:
            if used.name == "EMP" and encounter["type"] == "tech":
                print("EMP disables electronics. You bypass the threat.")
                return
            elif used.name == "Drone":
                bonus += 3
                print("Drone increases success chance.")
            elif used.name == "Medkit":
                op.heal(30)
                return

    stat = getattr(op, encounter_type)
    roll = random.randint(1, 10)
    synergy = calculate_synergy_bonus(op, encounter_type)
    difficulty = state.get_difficulty_modifier()
    success = stat + roll + bonus + synergy - difficulty

    print(f"🎯 {op.codename} rolls: {stat} + {roll} + gear({bonus}) + synergy({synergy}) - alert_penalty({difficulty}) = {success}")

    if success >= 12:
        print("✔️ Success — no alert.")
    elif success >= 9:
        print("⚠️ Partial — you succeeded, but were spotted.")
        op.apply_damage(random.randint(5, 15))
    else:
        print("❌ Failed — damage taken.")
        op.apply_damage(random.randint(20, 40))


def start_mission(mission):
    mission.show_briefing()
    team = None
    while not team:
        team = choose_team(mission.required_roles)
    equip_team(team)
    explore_mission(team, mission)
    print(f"\nMission '{mission.name}' completed.")


def main_menu():
    while True:
        print("\n==== RAINBOW SIX: TEXT STRATEGY ====")
        print("1. View Operators")
        print("2. Start Mission")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            show_operators()
        elif choice == "2":
            print("\n--- MISSIONS ---")
            for idx, mission in enumerate(missions, 1):
                print(f"[{idx}] {mission.name} ({mission.difficulty})")
            m_idx = int(input("Choose mission: ")) - 1
            start_mission(missions[m_idx])
        elif choice == "3":
            break

if __name__ == "__main__":
    main_menu()
