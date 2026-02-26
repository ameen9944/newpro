import pygame

class Bullet:
    def __init__(self, x, y, width, height, speed, direction= -1):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = direction  # -1 for up, 1 for down

    def update(self):
        self.rect.y += self.speed * self.direction

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)

    def off_screen(self, screen_height):
        return self.rect.y < 0 or self.rect.y > screen_height
