# Activity 1: 2D Animation Principles & Kinematics
# Engine (Tweening & Morphing)

import pygame
import math
import sys

pygame.init()

# --------------------------------------------------
# SETUP
# --------------------------------------------------

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "Activity 1: 2D Animation, Tweening & Morphing Engine"
)

clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BLUE = (50, 120, 255)
GREEN = (60, 200, 100)
RED = (230, 70, 70)
YELLOW = (240, 210, 70)
GRAY = (150, 150, 150)


# --------------------------------------------------
# HELPER: LINEAR INTERPOLATION
# --------------------------------------------------

def lerp(a, b, t):
    """Linear interpolation between two numbers."""
    return a + (b - a) * t


def lerp_point(p1, p2, t):
    """Linear interpolation between two 2D points."""
    return (
        p1[0] + (p2[0] - p1[0]) * t,
        p1[1] + (p2[1] - p1[1]) * t
    )


# --------------------------------------------------
# EASING
# --------------------------------------------------

def ease_in_out(t):
    """
    Smooth ease-in/ease-out interpolation.
    t is expected to be between 0 and 1.
    """
    return t * t * (3 - 2 * t)


# --------------------------------------------------
# TASK 1.1: TWEENING
# --------------------------------------------------

# Multi-point path
path = [
    (100, 150),
    (250, 100),
    (400, 250),
    (550, 150),
    (700, 350)
]

tween_duration = 5.0
tween_time = 0.0


def get_spline_position(points, t):
    """
    Move an object along a multi-point path.

    t = 0 -> beginning
    t = 1 -> end
    """

    if t <= 0:
        return points[0]

    if t >= 1:
        return points[-1]

    # Determine which path segment we are on
    total_segments = len(points) - 1
    scaled_t = t * total_segments

    segment = int(scaled_t)

    if segment >= total_segments:
        segment = total_segments - 1

    local_t = scaled_t - segment

    # Ease the movement
    local_t = ease_in_out(local_t)

    return lerp_point(
        points[segment],
        points[segment + 1],
        local_t
    )


# --------------------------------------------------
# TASK 1.2: POLYGON MORPHING
# --------------------------------------------------

# Triangle
triangle = [
    (200, 150),
    (100, 350),
    (300, 350)
]

# --------------------------------------------------
# VERTEX CORRESPONDENCE RULE
#
# Triangle has 3 vertices.
# Rectangle has 4 vertices.
#
# We subdivide one triangle edge to create
# a fourth vertex.
# --------------------------------------------------

triangle_4 = [
    (200, 150),
    (150, 250),   # Added midpoint vertex
    (100, 350),
    (300, 350)
]

# Rectangle
rectangle = [
    (150, 150),
    (350, 150),
    (350, 350),
    (150, 350)
]

morph_time = 0.0
morph_duration = 3.0


def morph_polygon(poly_a, poly_b, t):
    """
    Morph two polygons with the same number
    of vertices using vertex interpolation.
    """

    result = []

    for a, b in zip(poly_a, poly_b):
        result.append(lerp_point(a, b, t))

    return result


# --------------------------------------------------
# TASK 1.3: BOUNCING BALL
# --------------------------------------------------

ball_x = 600
ball_y = 100

ball_vel_x = 2.0
ball_vel_y = 0.0

gravity = 0.5
restitution = 0.78

floor_y = 500
ball_radius = 25


# --------------------------------------------------
# DRAWING FUNCTIONS
# --------------------------------------------------

def draw_text(text, x, y, size=24):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, WHITE)
    screen.blit(surface, (x, y))


def draw_tweening():
    global tween_time

    screen.fill(BLACK)

    # Draw path
    pygame.draw.lines(
        screen,
        GRAY,
        False,
        path,
        2
    )

    # Draw path points
    for point in path:
        pygame.draw.circle(
            screen,
            GRAY,
            point,
            5
        )

    # Calculate normalized time
    t = tween_time / tween_duration

    # Repeat animation
    if t > 1:
        tween_time = 0
        t = 0

    # Get position
    position = get_spline_position(path, t)

    # Draw sprite
    pygame.draw.circle(
        screen,
        BLUE,
        (int(position[0]), int(position[1])),
        25
    )

    draw_text("MODE 1: TWEENING", 20, 20)
    draw_text(
        "Linear interpolation + Ease In/Out",
        20,
        50,
        20
    )
    draw_text(
        "Press 1 = Tweening | 2 = Morphing | 3 = Dynamics",
        20,
        570,
        18
    )

    tween_time += 1 / FPS


def draw_morphing():
    global morph_time

    screen.fill(BLACK)

    # Normalized time
    t = morph_time / morph_duration

    # Repeat
    if t > 1:
        morph_time = 0
        t = 0

    # Ease the morph
    smooth_t = ease_in_out(t)

    # Calculate intermediate polygon
    current_polygon = morph_polygon(
        triangle_4,
        rectangle,
        smooth_t
    )

    # Draw original triangle guide
    pygame.draw.polygon(
        screen,
        (70, 70, 70),
        triangle
    )

    # Draw morphing polygon
    pygame.draw.polygon(
        screen,
        GREEN,
        current_polygon
    )

    # Draw outline
    pygame.draw.polygon(
        screen,
        WHITE,
        current_polygon,
        3
    )

    # Draw vertices
    for point in current_polygon:
        pygame.draw.circle(
            screen,
            RED,
            (int(point[0]), int(point[1])),
            5
        )

    draw_text("MODE 2: POLYGON MORPHING", 20, 20)

    draw_text(
        "Triangle → Rectangle",
        20,
        50,
        20
    )

    draw_text(
        "Vertex interpolation with equal vertex count",
        20,
        75,
        18
    )

    draw_text(
        "Press 1 = Tweening | 2 = Morphing | 3 = Dynamics",
        20,
        570,
        18
    )

    morph_time += 1 / FPS


def draw_dynamics():
    global ball_x
    global ball_y
    global ball_vel_x
    global ball_vel_y

    screen.fill(BLACK)

    # --------------------------------------------------
    # KINEMATICS
    #
    # y(i+1) = y(i) + v(i) * dt
    # v(i+1) = v(i) + g * dt
    # --------------------------------------------------

    dt = 1

    ball_y = ball_y + ball_vel_y * dt
    ball_vel_y = ball_vel_y + gravity * dt

    ball_x = ball_x + ball_vel_x * dt

    # --------------------------------------------------
    # FLOOR COLLISION
    # --------------------------------------------------

    if ball_y + ball_radius >= floor_y:

        ball_y = floor_y - ball_radius

        # Restitution:
        # v_rebound = -e * v_impact

        ball_vel_y = -restitution * ball_vel_y

    # Keep ball inside horizontal screen
    if ball_x - ball_radius <= 0:
        ball_x = ball_radius
        ball_vel_x = -ball_vel_x

    if ball_x + ball_radius >= WIDTH:
        ball_x = WIDTH - ball_radius
        ball_vel_x = -ball_vel_x

    # Floor
    pygame.draw.line(
        screen,
        WHITE,
        (0, floor_y),
        (WIDTH, floor_y),
        3
    )

    # Ball
    pygame.draw.circle(
        screen,
        RED,
        (int(ball_x), int(ball_y)),
        ball_radius
    )

    # Ball highlight
    pygame.draw.circle(
        screen,
        YELLOW,
        (
            int(ball_x - 8),
            int(ball_y - 8)
        ),
        5
    )

    draw_text("MODE 3: BOUNCING DYNAMICS", 20, 20)

    draw_text(
        f"Gravity: {gravity}",
        20,
        50,
        20
    )

    draw_text(
        f"Restitution: {restitution}",
        20,
        75,
        20
    )

    draw_text(
        f"Vertical Velocity: {ball_vel_y:.2f}",
        20,
        100,
        20
    )

    draw_text(
        "Press 1 = Tweening | 2 = Morphing | 3 = Dynamics",
        20,
        570,
        18
    )


# --------------------------------------------------
# TASK 1.4: MAIN LOOP + KEY CONTROLS
# --------------------------------------------------

mode = 1

running = True

while running:

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Tweening
            if event.key == pygame.K_1:
                mode = 1
                tween_time = 0

            # Morphing
            elif event.key == pygame.K_2:
                mode = 2
                morph_time = 0

            # Dynamics
            elif event.key == pygame.K_3:
                mode = 3

                # Reset ball
                ball_x = 600
                ball_y = 100
                ball_vel_x = 2.0
                ball_vel_y = 0.0

            # ESC = quit
            elif event.key == pygame.K_ESCAPE:
                running = False

    # --------------------------------------------------
    # SELECT MODE
    # --------------------------------------------------

    if mode == 1:
        draw_tweening()

    elif mode == 2:
        draw_morphing()

    elif mode == 3:
        draw_dynamics()

    # --------------------------------------------------
    # UPDATE DISPLAY
    # --------------------------------------------------

    pygame.display.flip()

    # 60 FPS
    clock.tick(FPS)


pygame.quit()
sys.exit()
