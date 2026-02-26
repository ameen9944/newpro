import pygame

class Player:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.base_speed = speed
        self.lives = 3
        self.score = 0
        self.shield_active = False
        self.shield_timer = 0
        self.shield_duration = 300  # 5 seconds at 60 FPS

        # Power-up effects
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        self.rapid_fire_active = False
        self.rapid_fire_timer = 0
        self.shoot_cooldown = 0

    def move(self, keys, screen_width, screen_height):
        # Manual movement in all directions
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < screen_width - self.rect.width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < screen_height - self.rect.height:
            self.rect.y += self.speed

    def activate_shield(self):
        if not self.shield_active:
            self.shield_active = True
            self.shield_timer = self.shield_duration

    def update_shield(self):
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False

    def update_power_ups(self):
        # Update speed boost
        if self.speed_boost_active:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed_boost_active = False
                self.speed = self.base_speed
            else:
                self.speed = self.base_speed * 2

        # Update rapid fire
        if self.rapid_fire_active:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer <= 0:
                self.rapid_fire_active = False

        # Update shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def can_shoot(self):
        if self.rapid_fire_active:
            return self.shoot_cooldown <= 0
        else:
            return True

    def apply_power_up(self, power_type):
        if power_type == 'speed_boost':
            self.speed_boost_active = True
            self.speed_boost_timer = 300  # 5 seconds
        elif power_type == 'extra_life':
            self.lives += 1
        elif power_type == 'rapid_fire':
            self.rapid_fire_active = True
            self.rapid_fire_timer = 240  # 4 seconds
        elif power_type == 'shield':
            self.activate_shield()

    def shoot(self, bullets):
        bullet = pygame.Rect(self.rect.x + self.rect.width // 2 - 5, self.rect.y, 10, 20)
        bullets.append(bullet)

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)
        if self.shield_active:
            # Draw shield as a larger, semi-transparent circle
            shield_color = (0, 255, 255, 100)  # Cyan with alpha
            shield_surface = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, shield_color, (shield_surface.get_width()//2, shield_surface.get_height()//2), shield_surface.get_width()//2)
            screen.blit(shield_surface, (self.rect.x - 10, self.rect.y - 10))
