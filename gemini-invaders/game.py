import pygame
import random
from player import Player
from enemy import Enemy
from bullet import Bullet
from powerup import PowerUp
from trivia_api import TriviaAPI

class Game:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Gemini Invaders")
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Colors - More saturated and attractive
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 50, 50)  # Brighter red
        self.BLUE = (50, 100, 255)  # Deeper blue
        self.GREEN = (50, 255, 100)  # Bright green
        self.YELLOW = (255, 255, 0)  # Yellow for special targets
        self.PURPLE = (200, 50, 255)  # Purple for power-ups
        self.ORANGE = (255, 150, 50)  # Orange for UI

        # Game objects
        self.player = Player(self.WIDTH//2 - 25, self.HEIGHT - 60, 50, 50, 5)
        self.bullets = []
        self.enemies = []
        self.enemy_bullets = []
        self.power_ups = []
        self.special_targets = []  # Special targets for bonus points
        self.stars = []  # Background stars for visual appeal
        self.spawn_stars(50)  # Spawn background stars

        # Game state
        self.level = 1
        self.score = 0
        self.lives = 3
        self.running = True
        self.game_over = False
        self.between_levels = False # Added state for between levels
        self.trivia_api = TriviaAPI()
        self.current_question = None
        self.current_answer = None

        # Fonts
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)

        self.spawn_enemies(2)  # Fewer enemies
        self.spawn_special_targets(3)  # Spawn special targets

    def spawn_stars(self, count):
        for _ in range(count):
            x = random.randint(0, self.WIDTH)
            y = random.randint(0, self.HEIGHT)
            self.stars.append((x, y))

    def spawn_special_targets(self, count):
        for _ in range(count):
            x = random.randint(50, self.WIDTH - 50)
            y = random.randint(50, self.HEIGHT // 2)
            self.special_targets.append(pygame.Rect(x, y, 30, 30))

    def spawn_enemies(self, count):
        for _ in range(count):
            x = random.randint(50, self.WIDTH - 50)
            behavior = Enemy.gemini_decide_behavior()
            enemy = Enemy(x, 0, 40, 40, behavior)
            self.enemies.append(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over and not self.between_levels:
                    bullet = Bullet(self.player.rect.x + self.player.rect.width // 2 - 5, self.player.rect.y, 10, 20, 7)
                    self.bullets.append(bullet)
                if event.key == pygame.K_s and not self.game_over and not self.between_levels:
                    self.player.activate_shield()
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                if event.key == pygame.K_t and self.between_levels: # Press T to answer Trivia
                    self.resolve_trivia(True)

    def update(self):
        if self.game_over:
            return

        if self.between_levels:
            return

        keys = pygame.key.get_pressed()
        self.player.move(keys, self.WIDTH, self.HEIGHT)
        self.player.update_shield()
        self.player.update_power_ups()

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.off_screen(self.HEIGHT):
                self.bullets.remove(bullet)

        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.off_screen(self.HEIGHT):
                self.enemy_bullets.remove(bullet)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.HEIGHT, self.player.rect.x, self.bullets)

            # Enemy shooting (reduced for collection gameplay)
            if random.random() < 0.002: # 0.2% chance per frame
                bullet = Bullet(enemy.rect.x + enemy.rect.width // 2 - 5, enemy.rect.y + enemy.rect.height, 10, 20, 5, 1)
                self.enemy_bullets.append(bullet)


            # Check collision with player bullets (optional, for defense)
            for bullet in self.bullets[:]:
                if enemy.rect.colliderect(bullet.rect):
                    self.bullets.remove(bullet)
                    if enemy.take_damage():
                        self.enemies.remove(enemy)
                        self.score += 10
                    break

            # Check collision with player (game over if touched)
            if enemy.rect.colliderect(self.player.rect):
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    self.game_over = True

            # Check if enemy reaches bottom (remove without penalty in collection mode)
            if enemy.rect.y > self.HEIGHT:
                self.enemies.remove(enemy)

        # Check collision with enemy bullets
        for bullet in self.enemy_bullets[:]:
            if self.player.rect.colliderect(bullet.rect):
                self.enemy_bullets.remove(bullet)
                if not self.player.shield_active:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                # Shield absorbs the hit

        # Spawn new enemies if needed (fewer)
        if len(self.enemies) < 2:
            self.spawn_enemies(1)

        # Check collision with special targets (collection by touching)
        for target in self.special_targets[:]:
            if self.player.rect.colliderect(target):
                self.special_targets.remove(target)
                self.score += 50  # Bonus points for collecting special targets
                # Spawn new target
                x = random.randint(50, self.WIDTH - 50)
                y = random.randint(50, self.HEIGHT // 2)
                self.special_targets.append(pygame.Rect(x, y, 30, 30))

        # Update power-ups
        for power_up in self.power_ups[:]:
            power_up.update()
            if power_up.rect.y > self.HEIGHT:
                self.power_ups.remove(power_up)

            # Check collision with player
            if self.player.rect.colliderect(power_up.rect):
                self.player.apply_power_up(power_up.power_type)
                self.power_ups.remove(power_up)
                self.score += 25  # Bonus points for collecting power-ups

        # Spawn power-ups occasionally
        if random.random() < 0.001:  # 0.1% chance per frame
            x = random.randint(50, self.WIDTH - 50)
            power_up = PowerUp.spawn_random(x, 0)
            self.power_ups.append(power_up)

        # Level up
        if self.score // 100 > self.level - 1:
            self.level += 1
            self.spawn_enemies(2)
            if self.level % 3 == 0:  # Every 3 levels, spawn more special targets
                self.spawn_special_targets(2)
            self.between_levels = True
            self.start_trivia()


    def draw(self):
        self.screen.fill(self.BLACK)

        # Draw background stars
        for star in self.stars:
            pygame.draw.circle(self.screen, self.WHITE, star, 1)

        if not self.game_over:
            if not self.between_levels:
                # Draw special targets
                for target in self.special_targets:
                    pygame.draw.rect(self.screen, self.YELLOW, target)

                # Draw player
                self.player.draw(self.screen, self.BLUE)

                # Draw bullets
                for bullet in self.bullets:
                    bullet.draw(self.screen, self.GREEN)

                # Draw enemy bullets
                for bullet in self.enemy_bullets:
                    bullet.draw(self.screen, self.ORANGE)

                # Draw enemies
                for enemy in self.enemies:
                    enemy.draw(self.screen, self.RED)

                # Draw power-ups
                for power_up in self.power_ups:
                    power_up.draw(self.screen)

                # Draw UI
                score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
                lives_text = self.font.render(f"Lives: {self.lives}", True, self.WHITE)
                level_text = self.font.render(f"Level: {self.level}", True, self.WHITE)
                self.screen.blit(score_text, (10, 10))
                self.screen.blit(lives_text, (10, 50))
                self.screen.blit(level_text, (10, 90))
            else:
                # Draw trivia question
                question_text = self.font.render(self.current_question, True, self.WHITE)
                answer_text = self.small_font.render("Press T for True", True, self.GREEN)
                false_text = self.small_font.render("Press any other key for False", True, self.RED)
                self.screen.blit(question_text, (self.WIDTH//2 - question_text.get_width()//2, self.HEIGHT//2 - 50))
                self.screen.blit(answer_text, (self.WIDTH//2 - answer_text.get_width()//2, self.HEIGHT//2 + 20))
                self.screen.blit(false_text, (self.WIDTH//2 - false_text.get_width()//2, self.HEIGHT//2 + 50))
        else:
            # Game over screen
            game_over_text = self.font.render("Game Over", True, self.RED)
            restart_text = self.small_font.render("Press R to restart", True, self.WHITE)
            final_score_text = self.small_font.render(f"Final Score: {self.score}", True, self.WHITE)
            self.screen.blit(game_over_text, (self.WIDTH//2 - 100, self.HEIGHT//2 - 50))
            self.screen.blit(restart_text, (self.WIDTH//2 - 80, self.HEIGHT//2))
            self.screen.blit(final_score_text, (self.WIDTH//2 - 70, self.HEIGHT//2 + 30))

        pygame.display.flip()

    def reset_game(self):
        self.player = Player(self.WIDTH//2 - 25, self.HEIGHT - 60, 50, 50, 5)
        self.bullets = []
        self.enemies = []
        self.enemy_bullets = []
        self.power_ups = []
        self.special_targets = []
        self.level = 1
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.between_levels = False
        self.spawn_enemies(5)
        self.spawn_special_targets(3)

    def start_trivia(self):
        self.current_question, self.current_answer = self.trivia_api.get_trivia_question()
        if self.current_question is None:
            self.current_question = "No trivia questions available."
            self.current_answer = "True"

    def resolve_trivia(self, player_answer):
        if str(player_answer) == self.current_answer.lower():
            self.score += 50
            print("Correct Answer")
        else:
            self.lives -= 1
            print("Incorrect Answer")
            if self.lives <= 0:
                self.game_over = True

        self.between_levels = False
        self.current_question = None
        self.current_answer = None

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
