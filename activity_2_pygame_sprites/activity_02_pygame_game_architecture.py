# Activity 2: Interactive Game Architecture: Game
# Loop & Sprite Collision

import pygame
import random
import sys

pygame.init()

# --------------------------------------------------
# SETUP
# --------------------------------------------------

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Activity 2: Sprite System & Collision Arena")

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 48)


# --------------------------------------------------
# COLORS
# --------------------------------------------------

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BLUE = (44, 94, 138)
RED = (220, 50, 50)
GREEN = (60, 200, 100)
YELLOW = (240, 210, 70)
GRAY = (100, 100, 100)


# --------------------------------------------------
# PLAYER SPRITE
# --------------------------------------------------

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # Transparent surface
        self.image = pygame.Surface(
            (40, 40),
            pygame.SRCALPHA
        )

        # Draw player
        pygame.draw.circle(
            self.image,
            BLUE,
            (20, 20),
            20
        )

        # Position
        self.rect = self.image.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2
            )
        )

        self.speed = 5

    def update(self):

        keys = pygame.key.get_pressed()

        # Left
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # Right
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Up
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed

        # Down
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Keep player inside screen
        self.rect.clamp_ip(
            pygame.Rect(
                0,
                0,
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
        )


# --------------------------------------------------
# OBSTACLE SPRITE
# --------------------------------------------------

class Obstacle(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface(
            (35, 35),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            self.image,
            RED,
            (0, 0, 35, 35),
            border_radius=5
        )

        self.rect = self.image.get_rect()

        self.speed_x = random.choice([-2, -1, 1, 2])
        self.speed_y = random.choice([-2, -1, 1, 2])

        self.respawn()

    def respawn(self):

        self.rect.x = random.randint(
            50,
            SCREEN_WIDTH - 50
        )

        self.rect.y = random.randint(
            50,
            SCREEN_HEIGHT - 50
        )

    def update(self):

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce from left/right
        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed_x *= -1

        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.speed_x *= -1

        # Bounce from top/bottom
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y *= -1

        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y *= -1


# --------------------------------------------------
# IMPACT PARTICLE
# --------------------------------------------------

class Particle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.velocity_x = random.uniform(-3, 3)
        self.velocity_y = random.uniform(-3, 3)

        self.size = random.randint(3, 7)

        self.alpha = 255

    def update(self):

        self.x += self.velocity_x
        self.y += self.velocity_y

        self.alpha -= 8

        if self.alpha < 0:
            self.alpha = 0

    def draw(self, surface):

        # Transparent particle surface
        particle_surface = pygame.Surface(
            (self.size * 2, self.size * 2),
            pygame.SRCALPHA
        )

        particle_surface.set_alpha(
            self.alpha
        )

        pygame.draw.circle(
            particle_surface,
            YELLOW,
            (
                self.size,
                self.size
            ),
            self.size
        )

        surface.blit(
            particle_surface,
            (
                int(self.x - self.size),
                int(self.y - self.size)
            )
        )

    def is_dead(self):

        return self.alpha <= 0


# --------------------------------------------------
# CREATE SPRITES
# --------------------------------------------------

player = Player()

player_group = pygame.sprite.Group()
player_group.add(player)

obstacle_group = pygame.sprite.Group()

for i in range(6):

    obstacle = Obstacle()

    obstacle_group.add(obstacle)


# --------------------------------------------------
# GAME VARIABLES
# --------------------------------------------------

score = 0
health = 3

particles = []

running = True


# --------------------------------------------------
# MAIN GAME LOOP
# --------------------------------------------------

while running:

    # --------------------------------------------------
    # 1. PROCESS INPUT
    # --------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False


    # --------------------------------------------------
    # 2. UPDATE GAME STATE
    # --------------------------------------------------

    player_group.update()

    obstacle_group.update()

    # Collision detection
    collisions = pygame.sprite.spritecollide(
        player,
        obstacle_group,
        False
    )

    if collisions:

        health -= 1

        # Create particles at player position
        for i in range(15):

            particles.append(
                Particle(
                    player.rect.centerx,
                    player.rect.centery
                )
            )

        # Respawn collided obstacles
        for obstacle in collisions:

            obstacle.respawn()

            # Add score
            score += 10

        # Move player back to center
        player.rect.center = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )

        # Game over
        if health <= 0:

            health = 3
            score = 0

            # Reset obstacles
            for obstacle in obstacle_group:

                obstacle.respawn()


    # Update particles
    for particle in particles:

        particle.update()

    # Remove dead particles
    particles = [
        particle
        for particle in particles
        if not particle.is_dead()
    ]


    # --------------------------------------------------
    # 3. RENDER
    # --------------------------------------------------

    screen.fill(BLACK)

    # Draw obstacles
    obstacle_group.draw(screen)

    # Draw player
    player_group.draw(screen)

    # Draw particles
    for particle in particles:

        particle.draw(screen)


    # --------------------------------------------------
    # HUD
    # --------------------------------------------------

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    health_text = font.render(
        f"Health: {health}",
        True,
        WHITE
    )

    fps_text = font.render(
        f"FPS: {clock.get_fps():.0f}",
        True,
        WHITE
    )

    controls_text = font.render(
        "Arrow Keys: Move | ESC: Quit",
        True,
        WHITE
    )


    screen.blit(
        score_text,
        (20, 20)
    )

    screen.blit(
        health_text,
        (20, 55)
    )

    screen.blit(
        fps_text,
        (20, 90)
    )

    screen.blit(
        controls_text,
        (20, 550)
    )


    # --------------------------------------------------
    # UPDATE DISPLAY
    # --------------------------------------------------

    pygame.display.flip()

    # Maintain 60 FPS
    clock.tick(FPS)


# --------------------------------------------------
# EXIT
# --------------------------------------------------

pygame.quit()
sys.exit()
