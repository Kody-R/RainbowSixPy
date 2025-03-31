
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
    print("\n⚔️ Zone Encounter:")
    encounter = zone.encounter
    encounter_type = encounter["type"]
    print(f"Encounter Type: {encounter_type.upper()} — Alert Level: {state.alert}/100")

    for idx, op in enumerate(team, 1):
        print(f"[{idx}] {op.codename} — HP: {op.health} — {op.status}")

    op = team[int(input("Choose an operator by number: ")) - 1]
    print("1. Attempt normally\n2. Use gadget")
    choice = input("Choice: ")

    bonus = 0
    if choice == "2" and op.gadgets:
        print(f"Gadgets: {', '.join([g.name for g in op.gadgets])}")
        item = input("Use which gadget? ").strip()
        used = next((g for g in op.gadgets if g.name.lower() == item.lower()), None)
        if used:
            op.gadgets.remove(used)
            if used.name == "EMP" and encounter_type == "tech":
                print("EMP disables electronics. You bypass the threat.")
                return
            elif used.name == "Drone":
                print("Drone increases success chance.")
                bonus += 3
            elif used.name == "Medkit":
                op.heal(30)
                return
            elif used.name == "Flashbang":
                print("💥 Flashbang used! Enemies stunned, easier success.")
                bonus += 2
            elif used.name == "Armor Plates":
                print("🛡️ Armor equipped. Reduced next damage.")
                op.health += 15
            elif used.name == "Adrenaline Shot":
                print("⚡ Boosted stamina!")
                op.stamina += 2

    stat = getattr(op, encounter_type)
    roll = random.randint(1, 10)
    synergy = calculate_synergy_bonus(op, encounter_type)
    difficulty = state.get_difficulty_modifier()
    success = stat + roll + bonus + synergy - difficulty

    print(f"{op.codename} rolls: {stat} + {roll} + bonus({bonus}) + synergy({synergy}) - penalty({difficulty}) = {success}")

    if success >= 12:
        print("✔️ Success — no alert.")
    elif success >= 9:
        print("⚠️ Partial — detected!")
        op.apply_damage(random.randint(5, 15))
        state.raise_alert(15)
    else:
        print("❌ Failure — heavily engaged!")
        op.apply_damage(random.randint(20, 40))
        state.raise_alert(25)

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
    mission, map_data = generate_random_mission(len(campaign.completed_missions))
    mission_maps[mission.name] = map_data
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

