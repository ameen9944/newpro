import pygame
import random

class Enemy:
    def __init__(self, x, y, width, height, behavior):
        self.rect = pygame.Rect(x, y, width, height)
        self.behavior = behavior
        self.speed = behavior["speed"]
        self.pattern = behavior["pattern"]
        self.direction = random.choice([-1, 1])  # For side movement
        self.health = 2  # Two hits to destroy
        self.evade_cooldown = 0  # Cooldown for dodging

    def update(self, screen_height, player_x=None, bullets=None):
        if self.evade_cooldown > 0:
            self.evade_cooldown -= 1

        if self.pattern == "charge":
            self.rect.y += self.speed
        elif self.pattern == "flock":
            self.rect.y += self.speed
            self.rect.x += self.direction * 2
            if self.rect.x <= 0 or self.rect.x >= 800 - self.rect.width:
                self.direction *= -1
        elif self.pattern == "retreat":
            if self.rect.y < screen_height // 2:
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed
        elif self.pattern == "zigzag":
            self.rect.y += self.speed
            self.rect.x += self.direction * 3
            if self.rect.x <= 0 or self.rect.x >= 800 - self.rect.width:
                self.direction *= -1
        elif self.pattern == "follow":
            if player_x is not None:
                if self.rect.x < player_x:
                    self.rect.x += self.speed
                elif self.rect.x > player_x:
                    self.rect.x -= self.speed
            self.rect.y += self.speed * 0.5
        elif self.pattern == "chase":
            if player_x is not None:
                # Aggressive chasing towards player
                if self.rect.x < player_x:
                    self.rect.x += self.speed
                elif self.rect.x > player_x:
                    self.rect.x -= self.speed
                self.rect.y += self.speed  # Always move down towards player

        # Dodging logic
        if bullets and self.evade_cooldown == 0:
            for bullet in bullets:
                if self.rect.colliderect(bullet.rect):
                    # Dodge the bullet
                    self.rect.x += 50 * self.direction  # Move to the side
                    self.evade_cooldown = 30  # Set cooldown

    def take_damage(self):
        self.health -= 1
        return self.health <= 0

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)

    @staticmethod
    def gemini_decide_behavior():
        behaviors = [
            {"speed": 2, "pattern": "chase"},  # Aggressive chasing
            {"speed": 3, "pattern": "charge"},
            {"speed": 1, "pattern": "flock"},
            {"speed": 2, "pattern": "retreat"},
            {"speed": 4, "pattern": "zigzag"},
            {"speed": 2, "pattern": "follow"},
        ]
        return random.choice(behaviors)
