import random
import pygame

CELL_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 8
HUD_WIDTH = 300
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE + HUD_WIDTH
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

pygame.init()
FONT = pygame.font.SysFont("arial", 18)

class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.color = (70, 70, 100)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (200, 200, 255), self.rect, 2)
        label = FONT.render(self.text, True, (255, 255, 255))
        screen.blit(label, (self.rect.x + 10, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

# === Grid System ===
class GridCell:
    def __init__(self, x, y, terrain="flat", obstacle=False, occupant=None):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.obstacle = obstacle
        self.occupant = occupant

class GridMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[GridCell(x, y) for y in range(height)] for x in range(width)]

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None

    def place_obstacles(self, count=10):
        for _ in range(count):
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            self.grid[x][y].obstacle = True

    def place_operator(self, operator, x, y):
        cell = self.get_cell(x, y)
        if cell and not cell.obstacle and not cell.occupant:
            operator.set_position(x, y)
            cell.occupant = operator
            return True
        return False

    def has_line_of_sight(self, x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        sx = -1 if x1 > x2 else 1
        sy = -1 if y1 > y2 else 1
        if dx > dy:
            err = dx / 2.0
            while x != x2:
                if (x, y) != (x1, y1) and self.grid[x][y].obstacle:
                    return False
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y2:
                if (x, y) != (x1, y1) and self.grid[x][y].obstacle:
                    return False
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        return True

# === Game Functions ===
def draw_grid(screen, grid):
    for x in range(grid.width):
        for y in range(grid.height):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cell = grid.get_cell(x, y)
            base_color = (50, 50, 50)
            if cell.obstacle:
                base_color = (120, 60, 60)
            elif (x + y) % 2 == 0:
                base_color = (60, 60, 70)
            pygame.draw.rect(screen, base_color, rect)
            pygame.draw.rect(screen, (20, 20, 20), rect, 1)
            if cell.occupant:
                pygame.draw.circle(screen, cell.occupant.color,
                                   rect.center, CELL_SIZE // 3)
                hp_pct = max(cell.occupant.health, 0) / 100
                bar_width = int(CELL_SIZE * hp_pct)
                bar_color = (0, 255, 0) if hp_pct > 0.5 else (255, 255, 0) if hp_pct > 0.25 else (255, 0, 0)
                pygame.draw.rect(screen, bar_color, (rect.x, rect.y + CELL_SIZE - 6, bar_width, 5))
 
# === Unit Base Class ===
class Unit:
    def __init__(self, codename, color):
        self.codename = codename
        self.health = 100
        self.color = color
        self.x = 0
        self.y = 0
        self.ap = 2
        self.range = 3

    def is_alive(self):
        return self.health > 0

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def move_to(self, new_x, new_y, grid):
        if self.ap <= 0:
            return False
        dest = grid.get_cell(new_x, new_y)
        if dest and not dest.obstacle and not dest.occupant:
            grid.get_cell(self.x, self.y).occupant = None
            self.set_position(new_x, new_y)
            dest.occupant = self
            self.ap -= 1
            return True
        return False

    def reset_ap(self):
        self.ap = 2

    def is_adjacent_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) == 1

    def in_range(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) <= self.range

    def attack(self, target, grid, log):
        if self.ap <= 0:
            return False
        if self.in_range(target) and grid.has_line_of_sight(self.x, self.y, target.x, target.y):
            hit_chance = max(30, 90 - (abs(self.x - target.x) + abs(self.y - target.y)) * 15)
            roll = random.randint(1, 100)
            if roll <= hit_chance:
                damage = random.randint(10, 30)
                target.health -= damage
                log.append(f"{self.codename} hits {target.codename} for {damage}!")
                if target.health <= 0:
                    log.append(f"{target.codename} is down!")
            else:
                log.append(f"{self.codename} missed {target.codename}! (Roll: {roll})")
            self.ap -= 1
            return True
        else:
            log.append(f"{target.codename} is blocked or out of range!")
            return False

class Operator(Unit):
    pass

class Enemy(Unit):
    def take_turn(self, grid, target, log):
        self.reset_ap()
        while self.ap > 0:
            if self.in_range(target) and grid.has_line_of_sight(self.x, self.y, target.x, target.y):
                self.attack(target, grid, log)
                break
            dx = target.x - self.x
            dy = target.y - self.y
            step_x = 1 if dx > 0 else -1 if dx < 0 else 0
            step_y = 1 if dy > 0 else -1 if dy < 0 else 0
            if abs(dx) > abs(dy):
                moved = self.move_to(self.x + step_x, self.y, grid)
            else:
                moved = self.move_to(self.x, self.y + step_y, grid)
            if not moved:
                break

# === Game Functions ===
def draw_grid(screen, grid):
    for x in range(grid.width):
        for y in range(grid.height):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cell = grid.get_cell(x, y)
            color = (40, 40, 40)
            if cell.obstacle:
                color = (100, 0, 0)
            elif cell.occupant:
                color = cell.occupant.color
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (80, 80, 80), rect, 1)
            if cell.occupant:
                hp_pct = max(cell.occupant.health, 0) / 100
                bar_width = int(CELL_SIZE * hp_pct)
                bar_color = (0, 255, 0) if hp_pct > 0.5 else (255, 255, 0) if hp_pct > 0.25 else (255, 0, 0)
                pygame.draw.rect(screen, bar_color, (rect.x, rect.y + CELL_SIZE - 6, bar_width, 5))

def draw_hud(screen, player, log):
    panel_x = GRID_WIDTH * CELL_SIZE
    pygame.draw.rect(screen, (30, 30, 30), (panel_x, 0, HUD_WIDTH, SCREEN_HEIGHT))
    info_lines = [
        f"Codename: {player.codename}",
        f"Health: {player.health}",
        f"AP: {player.ap}",
        f"Range: {player.range}"
    ]
    for i, line in enumerate(info_lines):
        text = FONT.render(line, True, (255, 255, 255))
        screen.blit(text, (panel_x + 10, 10 + i * 25))

    pygame.draw.line(screen, (200, 200, 200), (panel_x, 120), (SCREEN_WIDTH, 120))
    log_title = FONT.render("Combat Log:", True, (255, 255, 255))
    screen.blit(log_title, (panel_x + 10, 130))
    for i, entry in enumerate(reversed(log[-6:])):
        entry_text = FONT.render(entry, True, (220, 220, 220))
        screen.blit(entry_text, (panel_x + 10, 160 + i * 20))

def draw_buttons(screen, buttons):
    for button in buttons:
        button.draw(screen)

# === Main Loop ===
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Rainbow Six Grid Test")
    clock = pygame.time.Clock()

    grid = GridMap(GRID_WIDTH, GRID_HEIGHT)
    grid.place_obstacles()

    player = Operator("CHAVEZ", (0, 255, 0))
    enemy = Enemy("TANGO", (255, 0, 0))

    log = []
    buttons = []

    def end_turn():
        nonlocal player_turn
        log.append("End Turn clicked")
        player_turn = False

    def attack():
        player.attack(enemy, grid, log)

    buttons.append(Button("Attack", SCREEN_WIDTH - HUD_WIDTH + 20, 350, 100, 30, attack))
    buttons.append(Button("End Turn", SCREEN_WIDTH - HUD_WIDTH + 20, 390, 100, 30, end_turn))

    placed = False
    while not placed:
        x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
        placed = grid.place_operator(player, x, y)

    placed = False
    while not placed:
        x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
        placed = grid.place_operator(enemy, x, y)

    player_turn = True
    player.reset_ap()

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_grid(screen, grid)
        draw_hud(screen, player, log)
        draw_buttons(screen, buttons)
        pygame.display.flip()

        if not player.is_alive():
            log.append("Game Over. Player is down.")
            break
        if not enemy.is_alive():
            log.append("Enemy defeated. Victory!")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if player_turn:
                    dx, dy = 0, 0
                    if event.key == pygame.K_UP:
                        dy = -1
                    elif event.key == pygame.K_DOWN:
                        dy = 1
                    elif event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    new_x = player.x + dx
                    new_y = player.y + dy
                    moved = player.move_to(new_x, new_y, grid)
                    if moved:
                        log.append(f"{player.codename} moved to ({new_x},{new_y})")
                    if player.ap <= 0:
                        log.append(f"{player.codename}'s turn ended.")
                        player_turn = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    btn.handle_event(event)

        if not player_turn:
            log.append("--- Enemy Turn ---")
            enemy.take_turn(grid, player, log)
            log.append("--- Player Turn ---")
            player.reset_ap()
            player_turn = True

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
