import pygame
import random
from ui_elements import Button
from utils import calculate_synergy_bonus
from mission_state import MissionState
from game_data import gear_catalog
from main import mission_maps
from save_system import save_campaign

class MissionGameplayScreen:
    def __init__(self, team, mission, zones, campaign, on_finish_callback):
        self.team = [op for op in team if op.is_alive()]
        self.mission = mission
        self.campaign = campaign
        self.on_finish_callback = on_finish_callback
        self.zones = zones
        self.current_zone = self.zones["Entry Point"]
        self.state = MissionState()
        self.back_button = Button("Exit Mission", (50, 620), self.handle_exit)
        self.use_gadget_button = Button("Use Gadget", (50, 570), self.activate_gadget_mode)
        self.selected_op = None
        self.message_log = []
        self.font = pygame.font.SysFont("arial", 20)
        self.finished = False
        self.flash_red = 0
        self.next_zone_buttons = []
        self.gadget_buttons = []
        self.gadget_mode = False
        self.generate_next_zone_buttons()

    def handle_exit(self):
        return self.on_finish_callback(self.team, self.mission)

    def log(self, msg):
        self.message_log.append(msg)
        if len(self.message_log) > 6:
            self.message_log.pop(0)

    def generate_next_zone_buttons(self):
        self.next_zone_buttons = []
        for idx, name in enumerate(self.current_zone.next_zones):
            btn = Button(f"Go to {name}", (550, 500 + idx * 40), lambda n=name: self.goto_zone(n))
            self.next_zone_buttons.append(btn)

    def goto_zone(self, name):
        self.current_zone = self.zones[name]
        self.generate_next_zone_buttons()
        return self

    def handle_mission_complete(self):
        for op in self.team:
            if op.status != "KIA":
                earned = 50 + (op.stamina * 2)
                self.log(f"{op.codename} earned {earned} XP")
                op.gain_xp(earned)

        self.campaign.mark_mission_complete(self.mission)
        save_campaign(self.campaign.name, self.campaign)

    def activate_gadget_mode(self):
        self.gadget_buttons.clear()
        if not self.selected_op:
            return self
        for idx, g in enumerate(self.selected_op.gadgets):
            btn = Button(g.name, (200, 570 - idx * 40), lambda name=g.name: self.use_gadget(name))
            self.gadget_buttons.append(btn)
        self.gadget_mode = True
        return self

    def use_gadget(self, item_name):
        op = self.selected_op
        g = next((g for g in op.gadgets if g.name == item_name), None)
        if not g:
            return self

        self.log(f"{op.codename} uses {g.name}")
        op.gadgets.remove(g)

        enc_type = self.current_zone.encounter["type"]

        if g.name == "EMP" and enc_type == "tech":
            self.log("EMP disables tech threat. Zone cleared.")
            self.current_zone.cleared = True
            return self
        elif g.name == "Drone":
            self.log("Drone increases success chance.")
        elif g.name == "Medkit":
            op.heal(30)
            return self
        elif g.name == "Flashbang":
            self.log("💥 Flashbang! Enemies stunned. Bonus gained.")
        elif g.name == "Armor Plates":
            self.log("🛡️ Armor on. Reduced damage.")
            op.health += 15
        elif g.name == "Adrenaline Shot":
            self.log("⚡ Boosted stamina!")
            op.stamina += 2

        self.gadget_mode = False
        return self

    def handle_event(self, event):
        if self.finished:
            return self.on_finish_callback(self.team, self.mission)

        if self.back_button.handle_event(event):
            return self.back_button.callback()
        if self.use_gadget_button.handle_event(event):
            return self.use_gadget_button.callback()
        for btn in self.next_zone_buttons:
            if btn.handle_event(event):
                return btn.callback()
        for btn in self.gadget_buttons:
            if self.gadget_mode and btn.handle_event(event):
                return btn.callback()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for idx, op in enumerate(self.team):
                if 600 <= x <= 950 and 100 + idx * 40 <= y <= 130 + idx * 40:
                    self.selected_op = op
                    break

            if self.selected_op and self.current_zone.encounter and not self.current_zone.cleared:
                self.attempt_encounter(self.selected_op)

        return self

    def attempt_encounter(self, op):
        enc_type = self.current_zone.encounter["type"]
        bonus = 0
        synergy = calculate_synergy_bonus(op, enc_type)
        roll = random.randint(1, 10)
        difficulty = self.state.get_difficulty_modifier()
        stat = getattr(op, enc_type)

        result = stat + roll + bonus + synergy - difficulty

        self.log(f"{op.codename} rolls {stat}+{roll}+{bonus}+{synergy}-{difficulty} = {result}")

        if result >= 12:
            self.log("✔️ Success — no alert.")
        elif result >= 9:
            self.log("⚠️ Partial success — detected.")
            op.apply_damage(random.randint(5, 15))
            self.flash_red = 10
            self.state.raise_alert(15)
        else:
            self.log("❌ Failure — heavy engagement!")
            op.apply_damage(random.randint(20, 40))
            self.flash_red = 20
            self.state.raise_alert(25)

        self.current_zone.cleared = True

        if self.current_zone.loot:
            for item in self.current_zone.loot:
                gear = next((g for g in gear_catalog if g.name == item), None)
                if gear:
                    for op in self.team:
                        if len(op.gadgets) < 2 and op.can_use(gear):
                            if op.assign_gear(gear):
                                self.log(f"{op.codename} collected {item}")
                                break
            self.current_zone.loot = []

        if not self.current_zone.next_zones:
            self.log("\U0001F6E1️ Mission Complete! Extraction reached.")
            self.handle_mission_complete()
            self.finished = True

    def render(self, screen):
        screen.fill((20, 20, 20))

        if self.flash_red > 0:
            overlay = pygame.Surface((1000, 700), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, min(120, self.flash_red * 10)))
            screen.blit(overlay, (0, 0))
            self.flash_red -= 1

        zone = self.current_zone

        title = pygame.font.SysFont("arial", 28).render(f"Zone: {zone.name}", True, (255, 255, 255))
        screen.blit(title, (50, 30))

        screen.blit(self.font.render(zone.description, True, (200, 200, 200)), (50, 70))

        y = 110
        if zone.encounter and not zone.cleared:
            screen.blit(self.font.render(f"Encounter: {zone.encounter['type']}", True, (255, 100, 100)), (50, y))
            y += 30
        elif not zone.encounter:
            screen.blit(self.font.render("Zone Clear.", True, (100, 255, 100)), (50, y))
            y += 30

        if zone.loot:
            screen.blit(self.font.render(f"Loot: {', '.join(zone.loot)}", True, (255, 255, 0)), (50, y))
            y += 30

        screen.blit(self.font.render(f"Alert Level: {self.state.alert}/100", True, (255, 80, 80)), (50, y + 20))

        # Operator list
        screen.blit(self.font.render("Team:", True, (255, 255, 255)), (600, 70))
        for idx, op in enumerate(self.team):
            color = (100, 255, 100) if op == self.selected_op else (255, 255, 255)
            text = f"{op.codename} - HP: {op.health} - {op.status}"
            label = self.font.render(text, True, color)
            screen.blit(label, (600, 100 + idx * 40))

        # Log
        for i, msg in enumerate(self.message_log):
            screen.blit(self.font.render(msg, True, (180, 180, 180)), (50, 500 + i * 20))

        self.back_button.draw(screen)
        self.use_gadget_button.draw(screen)
        for btn in self.next_zone_buttons:
            btn.draw(screen)
        if self.gadget_mode:
            for btn in self.gadget_buttons:
                btn.draw(screen)
