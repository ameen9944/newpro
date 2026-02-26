import pygame
import random

class PowerUp:
    def __init__(self, x, y, power_type):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.power_type = power_type
        self.speed = 2
        self.active = True

        # Define power-up types and their effects
        self.types = {
            'speed_boost': {'color': (255, 255, 0), 'duration': 300},  # Yellow, 5 seconds
            'extra_life': {'color': (0, 255, 0), 'duration': 0},  # Green, instant
            'rapid_fire': {'color': (255, 0, 255), 'duration': 240},  # Magenta, 4 seconds
            'shield': {'color': (0, 255, 255), 'duration': 300},  # Cyan, 5 seconds
        }

    def update(self):
        if self.active:
            self.rect.y += self.speed

    def draw(self, screen):
        if self.active:
            color = self.types[self.power_type]['color']
            pygame.draw.rect(screen, color, self.rect)
            # Add a border for visibility
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

    @staticmethod
    def spawn_random(x, y):
        power_types = ['speed_boost', 'extra_life', 'rapid_fire', 'shield']
        power_type = random.choice(power_types)
        return PowerUp(x, y, power_type)
