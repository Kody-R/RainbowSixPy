
from game_data import gear_catalog, default_operators, TYPE_ICONS
from utils import calculate_synergy_bonus
from mission_state import MissionState
from save_system import list_saves, load_campaign, save_campaign
from campaign import CampaignState
from mission_generator import generate_random_mission
import random

mission_maps = {}


def choose_campaign():
    print("\n==== RAINBOW SIX - CAMPAIGN SYSTEM ====")
    print("1. New Game")
    print("2. Load Game")
    choice = input("Choose: ")

    if choice == "1":
        name = input("Name your campaign: ")
        state = CampaignState(name=name, operators=default_operators)
        save_campaign(name, state)
        return state
    elif choice == "2":
        saves = list_saves()
        if not saves:
            print("No saves found. Starting new game.")
            return CampaignState(name="Default", operators=default_operators)
        print("\nAvailable Saves:")
        for idx, s in enumerate(saves, 1):
            print(f"{idx}. {s}")
        index = int(input("Load which campaign? ")) - 1
        return load_campaign(saves[index])
    else:
        return choose_campaign()

def show_operators(campaign):
    print("\n--- OPERATOR ROSTER ---")
    for idx, op in enumerate(campaign.operators, 1):
        print(f"[{idx}] {op.codename} ({op.role}) — Level {op.level}, XP: {op.xp}, Status: {op.status}")

def choose_team(campaign):
    team = []
    print("\nSelect 2–4 operators by number (separated by space):")
    show_operators(campaign)
    indices = input("Your team: ").split()

    for i in indices:
        try:
            selected = campaign.operators[int(i) - 1]
            team.append(selected)
        except:
            print(f"Invalid index: {i}")

    if not (2 <= len(team) <= 4):
        print("Team must be 2–4 members.")
        return None

    print("\nTeam confirmed:")
    for op in team:
        print(f" - {op.codename} ({op.role})")
    return team

def equip_team(team):
    print("\n--- GEAR LOADOUT ---")
    for op in team:
        print(f"\nCurrent loadout for {op.codename}: {', '.join(op.get_gear_names()) or 'None'}")
        change = input(f"Would you like to change {op.codename}'s loadout? (y/n): ").strip().lower()
        if change != 'y':
            continue

        op.clear_gear()
        print("\nAvailable Gear:")
        for idx, g in enumerate(gear_catalog, 1):
            if not op.can_use(g):
                continue
            print(f"[{idx}] {g.name} [{g.type}] — {g.rarity} — Effect: {g.effect or 'None'}")
        print(f"Max allowed gear weight: {op.max_gear_weight}")
        indices = input("Enter gear numbers separated by space: ").split()
        for i in indices:
            try:
                gear = gear_catalog[int(i) - 1]
                if not op.assign_gear(gear):
                    print(f"Skipping {gear.name} due to weight limit.")
            except:
                continue

def handle_zone_encounter(team, zone, state):
    import random
    print("\n⚔️ Zone Encounter:")
    encounter = zone.encounter
    encounter_type = encounter["type"]
    print(f"Encounter Type: {encounter_type.upper()} — Alert Level: {state.alert}/100")

    avg_level = sum(op.level for op in team) / len(team)

    # Terrain suggestion
    terrain = zone.description.lower()
    recommended = "Overwatch"
    if "jungle" in terrain or "underground" in terrain:
        recommended = "Stealth Entry"
    elif "mountain" in terrain or "desert" in terrain:
        recommended = "Rush"
    elif "urban" in terrain:
        recommended = "Overwatch"
    elif "arctic" in terrain:
        recommended = "Caution Sweep"
    print(f"\n🌎 Terrain suggests using: {recommended}")

    print("\n📐 Choose a squad formation:")
    print("1. Stealth Entry (boost stealth, penalize marksmanship)")
    print("2. Overwatch (balanced, no modifiers)")
    print("3. Rush (boost marksmanship, penalize stealth)")

    formation_options = {
        "4": ("Caution Sweep", "boost tech, reduce alert penalties", 3),
        "5": ("Lockdown", "defense boost, but higher success threshold", 4),
        "6": ("Phantom Column", "bonus stealth & evasion", 5),
        "7": ("Kill Box", "heavy weapons bonus, +alert on fail", 6)
    }

    for key, (name, desc, lvl) in formation_options.items():
        if avg_level >= lvl:
            print(f"{key}. {name} ({desc})")
        else:
            print(f"{key}. [Locked — requires avg level {lvl}]")

    valid_choices = [str(i) for i in range(1, 4)] + [k for k, (_, _, lvl) in formation_options.items() if avg_level >= lvl]

    formation_input = input("Formation: ")
    while formation_input not in valid_choices:
        formation_input = input("Invalid. Choose available formation: ")

    formation_map = {
        "1": "stealth",
        "2": "balanced",
        "3": "marksmanship",
        "4": "tech",
        "5": "defense",
        "6": "phantom",
        "7": "killbox"
    }
    formation = formation_map[formation_input]

    leader_bonus = max(op.leadership for op in team) // 5

    if hasattr(zone, "hazard") and zone.hazard:
        print(f"\n⚠️ Hazard in this zone: {zone.hazard}")
        for op in team:
            if zone.hazard == "Surveillance Cameras":
                print(f"{op.codename} affected by Surveillance Cameras — Alert +10")
                state.raise_alert(10)
            elif zone.hazard == "Wildlife Ambush":
                print(f"{op.codename} ambushed by wildlife — HP -10")
                op.apply_damage(10)
            elif zone.hazard == "Hypothermia":
                print(f"{op.codename} suffers Hypothermia — stamina -1")
                op.stamina = max(1, op.stamina - 1)
            elif zone.hazard == "Toxic Gas":
                print(f"{op.codename} breathes toxic gas — HP -5")
                op.apply_damage(5)
            elif zone.hazard == "Rockslide":
                print(f"{op.codename} caught in rockslide — HP -10")
                op.apply_damage(10)
            elif zone.hazard == "Tidal Flooding":
                print(f"{op.codename} slowed by flooding — Alert +5")
                state.raise_alert(5)
            elif zone.hazard == "Heatstroke":
                print(f"{op.codename} suffers Heatstroke — stamina -2")
                op.stamina = max(1, op.stamina - 2)

    print("\n🎖 Resolving encounter for each squad member:")

    for op in team:
        if not op.is_alive():
            print(f"❌ {op.codename} is KIA — Skipping.")
            continue

        print(f"\n➡️ {op.codename} — HP: {op.health}, Status: {op.status}")

        formation_bonus = 0
        extra_effects = ""
        if formation == "stealth" and encounter_type == "stealth":
            formation_bonus = 2
        elif formation == "marksmanship" and encounter_type == "marksmanship":
            formation_bonus = 2
        elif formation == "tech" and encounter_type == "tech":
            formation_bonus = 2
        elif formation == "defense":
            formation_bonus = 1
            extra_effects = "threshold+1"
        elif formation == "phantom" and encounter_type in ["stealth", "tech"]:
            formation_bonus = 2
            print("🕶️ Phantom Column: enhanced stealth & evasion")
        elif formation == "killbox" and encounter_type == "marksmanship":
            formation_bonus = 3
            extra_effects = "high_alert"
            print("💀 Kill Box: overwhelming firepower — but risky")

        if formation == "stealth" and encounter_type == "marksmanship":
            formation_bonus = -2
        elif formation == "rush" and encounter_type == "stealth":
            formation_bonus = -2

        bonus = 0
        if op.gadgets:
            print(f"Gadgets available for {op.codename}: {', '.join(g.name for g in op.gadgets)}")
            use_gadget = input("Use a gadget? (y/n): ").strip().lower()
            if use_gadget == "y":
                item = input("Use which gadget? ").strip()
                used = next((g for g in op.gadgets if g.name.lower() == item.lower()), None)
                if used:
                    op.gadgets.remove(used)
                    if used.name == "EMP" and encounter_type == "tech":
                        print("EMP disables threat for this operator.")
                        continue
                    elif used.name == "Flashbang":
                        print("💥 Flashbang boosts encounter success.")
                        bonus += 2
                    elif used.name == "Drone":
                        print("🛰️ Drone used for scouting.")
                        bonus += 3
                    elif used.name == "Medkit":
                        op.heal(30)
                        continue
                    elif used.name == "Armor Plates":
                        op.health += 10
                        print("🛡️ Armor equipped.")
                    elif used.name == "Adrenaline Shot":
                        op.stamina += 2
                        print("⚡ Adrenaline boost applied.")

        stat = getattr(op, encounter_type)
        roll = random.randint(1, 10)
        synergy = calculate_synergy_bonus(op, encounter_type)
        difficulty = state.get_difficulty_modifier()

        ability = 0
        if op.ability == "Breach Expert" and "Breach Charge" in op.get_gear_names():
            print("🔧 Breach Expert bonus: +2")
            ability += 2
        elif op.ability == "Intel Scanner" and encounter_type == "stealth":
            print("🛰️ Intel Scanner bonus: +1")
            ability += 1
        elif op.ability == "Sharpshooter" and encounter_type == "marksmanship":
            print("🎯 Sharpshooter bonus: +2")
            ability += 2
        elif op.ability == "Tactical Boost":
            print("🗣️ Tactical Boost: +1 to all team stamina")
            for teammate in team:
                teammate.stamina += 1
        elif op.ability == "Silent Strike" and encounter_type == "stealth":
            print("🎭 Silent Strike: Reduced alert on partials")
        elif op.ability == "System Cracker" and encounter_type == "tech":
            print("💻 System Cracker: +1")
            ability += 1
        elif op.ability == "Shock & Awe" and encounter_type == "marksmanship":
            print("💥 Shock & Awe: stuns enemies")
            bonus += 1
        elif op.ability == "Combat Medic" and op.health < 50:
            print("🩺 Combat Medic auto-heals")
            op.heal(10)
        elif op.ability == "Adaptive Ops":
            print("🌀 Adaptive Ops: +1 to random stat")
            ability += random.choice([0, 1])
        elif op.ability == "Fortify":
            print("🛡️ Fortify: reduce incoming damage")
            bonus += 1

        total = stat + roll + bonus + synergy + ability + formation_bonus + leader_bonus - difficulty
        print(f"{op.codename} rolls: {stat} + {roll} + bonus({bonus}) + synergy({synergy}) + ability({ability}) + formation({formation_bonus}) + leader({leader_bonus}) - penalty({difficulty}) = {total}")

        success_threshold = 12
        if extra_effects == "threshold+1":
            success_threshold += 1

        if total >= success_threshold:
            print("✔️ Success — no alert.")
        elif total >= 9:
            print("⚠️ Partial — detected!")
            if op.ability != "Silent Strike" and formation != "tech":
                state.raise_alert(10)
            elif formation == "tech":
                print("🔧 Caution Sweep reduces alert penalty.")
                state.raise_alert(5)
            op.apply_damage(random.randint(5, 15))
        else:
            print("❌ Failure — heavily engaged!")
            op.apply_damage(random.randint(20, 40))
            state.raise_alert(30 if extra_effects == "high_alert" else 20)

    print(f"\n📊 Encounter complete. Alert level is now {state.alert}/100.")



def explore_mission(team, mission, campaign):
    state = MissionState()
    zones = mission_maps[mission.name]
    current_zone = zones["Entry Point"]
    visited = set()

    while current_zone:
        current_zone.show_info()
        if current_zone.name not in visited:
            visited.add(current_zone.name)
        if current_zone.encounter and not current_zone.cleared:
            handle_zone_encounter(team, current_zone, state)
            current_zone.cleared = True

        if current_zone.loot:
            print("Collecting loot...")
            for op in team:
                for item in current_zone.loot:
                    if len(op.gadgets) < 2:
                        gear = next((g for g in gear_catalog if g.name == item), None)
                        if gear:
                            op.assign_gear(gear)
                            print(f"{op.codename} collected {item}")
                            break
            current_zone.loot = []

        if not current_zone.next_zones:
            print("🚁 Mission complete — reached extraction!")
            for op in team:
                if op.status != "KIA":
                    earned = 50 + (op.stamina * 2)
                    print(f"{op.codename} earns {earned} XP")
                    op.gain_xp(earned)
            campaign.mark_mission_complete(mission)
            save_campaign(campaign.name, campaign)
            break

        print(f"\n📶 Current Alert Level: {state.alert}/100")
        print("\nAvailable paths:")
        for idx, nz in enumerate(current_zone.next_zones, 1):
            print(f"{idx}. {nz}")
        choice = int(input("Choose your path: ")) - 1
        current_zone = zones[current_zone.next_zones[choice]]

def start_mission(campaign):
    # Generate random mission and map
    mission, zones = generate_random_mission(len(campaign.completed_missions))
    mission_maps[mission.name] = zones
    campaign.generated_missions[mission.name] = mission
    print(f"Ἑ5 Generated Mission: {mission.name}")

    mission.show_briefing()
    team = None
    while not team:
        team = choose_team(campaign)
    equip_team(team)
    explore_mission(team, mission, campaign)
    print(f"\nMission '{mission.name}' completed.")

def show_campaign_map(campaign):
    print("\n🌍 GLOBAL OPS MAP")

    all_locations = list(set(m.location for m in campaign.generated_missions.values()))
    all_locations = sorted(all_locations)

    for loc in all_locations:
        missions_here = [m for m in campaign.generated_missions.values() if m.location == loc]
        for m in missions_here:
            icon = TYPE_ICONS.get(m.mission_type, "❓")
            status = "✅" if m.name in campaign.completed_missions else "🔲"
            print(f"{status} {icon} {loc} — {m.name} ({m.mission_type})")


def main_menu(campaign):
    while True:
        print("\n==== RAINBOW SIX: TEXT STRATEGY ====")
        print("1. View Operators")
        print("2. Start Mission")
        print("3. View Global Campaign Map")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            show_operators(campaign)
        elif choice == "2":
            start_mission(campaign)
        elif choice == "3":
            show_campaign_map(campaign)
        elif choice == "4":
            break


if __name__ == "__main__":
    campaign = choose_campaign()
    main_menu(campaign)

