# 🎮 Rainbow Six: Strategic Ops

A tactical strategy game inspired by the classic Rainbow Six franchise, reimagined as a deep and immersive text-based and PyGame-driven campaign. You are in command of an elite multinational team tasked with completing high-stakes missions across the globe — each one more complex and dangerous than the last.

## 🌍 Game Overview

In **Rainbow Six: Strategic Ops**, you’ll:

- Recruit and manage a roster of unique operators
- Equip custom loadouts with diverse gear and gadgets
- Generate randomized missions with varied objectives and terrains
- Explore zone-based maps with strategic decision-making
- Engage in turn-based encounters influenced by synergy, gear, and environment
- Track progress and global operations through a persistent campaign

---

## 🛠 Features

### 🧑‍✈️ Operator System

- Each operator has a codename, role (e.g., Assault, Tech, Recon), and attributes like **stealth**, **tech**, and **marksmanship**.
- Operators gain XP, level up, unlock rare gear, and can be wounded or killed.

### 🔫 Gear and Loadouts

- Assign gear based on rarity, weight limits, and role compatibility.
- Gear includes silenced weapons, EMPs, medkits, drones, flashbangs, and more.
- Strategic choices impact outcomes during missions.

### 🧭 Mission Generator

- Dynamic mission generator builds operations with objectives like:
  - Infiltration
  - Sabotage
  - Hostage Rescue
  - Extraction
- Missions occur in diverse terrains like **Urban**, **Jungle**, **Arctic**, and **Underground**, each with its own gameplay modifiers.

### 🧠 Encounter System

- Synergy mechanics combine operator roles, gear, and terrain to influence success.
- Failures can raise alert levels, cause injuries, or mission failure.

### 💾 Save System

- Campaigns can be saved, loaded, and continued with persistent progress.

### 🖥️ GUI (PyGame)

- A graphical interface complements the text-based core.
- View operator rosters, campaign map, and manage missions visually.

---

## 🧩 File Structure

- `main.py` – Core gameplay loop (text-based)
- `gui_main.py` – Launches PyGame-based interface
- `mission_generator.py` – Randomly builds missions
- `operators.py`, `gear.py`, `utils.py` – Core mechanics
- `screens.py`, `ui_elements.py`, `global_map_screen.py` – PyGame UI screens
- `save_system.py` – Save/load campaign states
- `game_data.py` – Initializes operator and gear catalogs

---

## 🚀 Getting Started

### Requirements

- Python 3.10+
- pygame

### Install Dependencies

```bash
pip install pygame
