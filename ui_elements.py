import pygame

class Button:
    def __init__(self, text, pos, callback):
        self.text = text
        self.pos = pos
        self.callback = callback
        self.font = pygame.font.SysFont("arial", 28)
        self.rect = pygame.Rect(pos[0], pos[1], 300, 40)

    def draw(self, screen):
        pygame.draw.rect(screen, (80, 80, 200), self.rect)
        label = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(label, (self.pos[0] + 10, self.pos[1] + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
