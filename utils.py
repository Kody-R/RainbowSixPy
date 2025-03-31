def calculate_synergy_bonus(op, encounter_type):
    synergy_bonus = 0

    # Role-based synergy
    if op.role == "Hacker" and encounter_type == "tech":
        synergy_bonus += 2
    if op.role == "Recon" and encounter_type == "stealth":
        synergy_bonus += 2
    if op.role == "Assault" and encounter_type == "marksmanship":
        synergy_bonus += 2

    # Gear-based synergy
    gear_names = op.get_gear_names()
    if "Drone" in gear_names and encounter_type in ["stealth", "tech"]:
        synergy_bonus += 2
    if "EMP" in gear_names and encounter_type == "tech":
        synergy_bonus += 1
    if "Sniper Rifle" in gear_names and encounter_type == "marksmanship":
        synergy_bonus += 1
    if "Silenced Pistol" in gear_names and encounter_type == "stealth":
        synergy_bonus += 1
    if "Breach Charge" in gear_names and encounter_type == "tech":
        synergy_bonus -= 1  # Penalty for brute-force gear in stealth

    return synergy_bonus
