# Activity 4: 3D Projection Engine: Orthographic,
# Oblique & Perspective

import pygame
import math

pygame.init()

# =========================
# WINDOW SETTINGS
# =========================

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Activity 4 - 3D Projection Engine")

clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 30)
SMALL_FONT = pygame.font.Font(None, 24)


# =========================
# COLORS
# =========================

BLACK = (20, 20, 25)
WHITE = (240, 240, 240)
RED = (230, 80, 80)
GREEN = (80, 220, 120)
BLUE = (80, 150, 240)
YELLOW = (240, 220, 80)
GRAY = (100, 100, 100)


# =========================
# 3D CUBE VERTICES
# =========================

cube_vertices = [
    [-100, -100, -100],
    [100, -100, -100],
    [100, 100, -100],
    [-100, 100, -100],

    [-100, -100, 100],
    [100, -100, 100],
    [100, 100, 100],
    [-100, 100, 100]
]


# =========================
# CUBE EDGES
# =========================

cube_edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),

    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),

    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
]


# =========================
# ROTATION AROUND X
# =========================

def rotate_x(x, y, z, angle):

    rad = math.radians(angle)

    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    new_y = y * cos_a - z * sin_a
    new_z = y * sin_a + z * cos_a

    return x, new_y, new_z


# =========================
# ROTATION AROUND Y
# =========================

def rotate_y(x, y, z, angle):

    rad = math.radians(angle)

    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    new_x = x * cos_a + z * sin_a
    new_z = -x * sin_a + z * cos_a

    return new_x, y, new_z


# =========================
# ROTATION AROUND Z
# =========================

def rotate_z(x, y, z, angle):

    rad = math.radians(angle)

    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    new_x = x * cos_a - y * sin_a
    new_y = x * sin_a + y * cos_a

    return new_x, new_y, z


# =========================
# APPLY ALL ROTATIONS
# =========================

def rotate_point(vertex, angle_x, angle_y, angle_z):

    x, y, z = vertex

    # Rotate around X
    x, y, z = rotate_x(
        x, y, z, angle_x
    )

    # Rotate around Y
    x, y, z = rotate_y(
        x, y, z, angle_y
    )

    # Rotate around Z
    x, y, z = rotate_z(
        x, y, z, angle_z
    )

    return x, y, z


# =========================
# ORTHOGRAPHIC PROJECTION
# =========================

def project_orthographic(x, y, z):

    xp = x
    yp = y

    return (
        int(xp + WIDTH // 2),
        int(yp + HEIGHT // 2)
    )


# =========================
# CAVALIER PROJECTION
# =========================

def project_cavalier(x, y, z):

    # Cavalier:
    # alpha = 45 degrees
    # L1 = 1.0

    alpha = math.radians(45)

    L1 = 1.0

    xp = x + z * L1 * math.cos(alpha)
    yp = y + z * L1 * math.sin(alpha)

    return (
        int(xp + WIDTH // 2),
        int(yp + HEIGHT // 2)
    )


# =========================
# CABINET PROJECTION
# =========================

def project_cabinet(x, y, z):

    # Cabinet:
    # alpha = 63.4 degrees
    # L1 = 0.5

    alpha = math.radians(63.4)

    L1 = 0.5

    xp = x + z * L1 * math.cos(alpha)
    yp = y + z * L1 * math.sin(alpha)

    return (
        int(xp + WIDTH // 2),
        int(yp + HEIGHT // 2)
    )


# =========================
# PERSPECTIVE PROJECTION
# =========================

def project_perspective(x, y, z):

    D = 400

    distance = z + D

    # Prevent division by zero
    if distance == 0:
        distance = 0.001

    xp = (x * D) / distance
    yp = (y * D) / distance

    return (
        int(xp + WIDTH // 2),
        int(yp + HEIGHT // 2)
    )


# =========================
# SELECT PROJECTION
# =========================

def project_point(x, y, z, mode):

    if mode == "Orthographic":
        return project_orthographic(
            x, y, z
        )

    elif mode == "Cavalier":
        return project_cavalier(
            x, y, z
        )

    elif mode == "Cabinet":
        return project_cabinet(
            x, y, z
        )

    elif mode == "Perspective":
        return project_perspective(
            x, y, z
        )


# =========================
# DRAW AXES
# =========================

def draw_axes(mode, angle_x, angle_y, angle_z):

    origin = rotate_point(
        [0, 0, 0],
        angle_x,
        angle_y,
        angle_z
    )

    x_axis = rotate_point(
        [180, 0, 0],
        angle_x,
        angle_y,
        angle_z
    )

    y_axis = rotate_point(
        [0, 180, 0],
        angle_x,
        angle_y,
        angle_z
    )

    z_axis = rotate_point(
        [0, 0, 180],
        angle_x,
        angle_y,
        angle_z
    )

    origin_2d = project_point(
        *origin,
        mode
    )

    x_2d = project_point(
        *x_axis,
        mode
    )

    y_2d = project_point(
        *y_axis,
        mode
    )

    z_2d = project_point(
        *z_axis,
        mode
    )

    # X axis
    pygame.draw.line(
        screen,
        RED,
        origin_2d,
        x_2d,
        2
    )

    # Y axis
    pygame.draw.line(
        screen,
        GREEN,
        origin_2d,
        y_2d,
        2
    )

    # Z axis
    pygame.draw.line(
        screen,
        BLUE,
        origin_2d,
        z_2d,
        2
    )

    screen.blit(
        SMALL_FONT.render(
            "X",
            True,
            RED
        ),
        x_2d
    )

    screen.blit(
        SMALL_FONT.render(
            "Y",
            True,
            GREEN
        ),
        y_2d
    )

    screen.blit(
        SMALL_FONT.render(
            "Z",
            True,
            BLUE
        ),
        z_2d
    )


# =========================
# DRAW CUBE
# =========================

def draw_cube(mode, angle_x, angle_y, angle_z):

    projected_vertices = []

    # Rotate and project every vertex
    for vertex in cube_vertices:

        rotated = rotate_point(
            vertex,
            angle_x,
            angle_y,
            angle_z
        )

        x, y, z = rotated

        projected = project_point(
            x,
            y,
            z,
            mode
        )

        projected_vertices.append(
            projected
        )

    # Draw edges
    for edge in cube_edges:

        start = projected_vertices[
            edge[0]
        ]

        end = projected_vertices[
            edge[1]
        ]

        pygame.draw.line(
            screen,
            WHITE,
            start,
            end,
            3
        )

    # Draw vertices
    for point in projected_vertices:

        pygame.draw.circle(
            screen,
            YELLOW,
            point,
            5
        )


# =========================
# VANISHING POINT
# =========================

def draw_vanishing_point():

    if mode == "Perspective":

        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        pygame.draw.circle(
            screen,
            RED,
            (center_x, center_y),
            6
        )

        screen.blit(
            SMALL_FONT.render(
                "Vanishing Point",
                True,
                RED
            ),
            (
                center_x + 10,
                center_y - 10
            )
        )


# =========================
# VARIABLES
# =========================

mode = "Orthographic"

angle_x = 0
angle_y = 0
angle_z = 0

running = True


# =========================
# MAIN GAME LOOP
# =========================

while running:

    # =====================
    # EVENTS
    # =====================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Projection modes
            if event.key == pygame.K_1:
                mode = "Orthographic"

            elif event.key == pygame.K_2:
                mode = "Cavalier"

            elif event.key == pygame.K_3:
                mode = "Cabinet"

            elif event.key == pygame.K_4:
                mode = "Perspective"

            # Reset
            elif event.key == pygame.K_r:
                angle_x = 0
                angle_y = 0
                angle_z = 0

            # Quit
            elif event.key == pygame.K_ESCAPE:
                running = False


    # =====================
    # KEYBOARD ROTATION
    # =====================

    keys = pygame.key.get_pressed()

    rotation_speed = 2

    # X rotation
    if keys[pygame.K_UP]:
        angle_x -= rotation_speed

    if keys[pygame.K_DOWN]:
        angle_x += rotation_speed

    # Y rotation
    if keys[pygame.K_LEFT]:
        angle_y -= rotation_speed

    if keys[pygame.K_RIGHT]:
        angle_y += rotation_speed

    # Z rotation
    if keys[pygame.K_q]:
        angle_z -= rotation_speed

    if keys[pygame.K_e]:
        angle_z += rotation_speed


    # =====================
    # DRAW
    # =====================

    screen.fill(BLACK)

    # Title
    title = FONT.render(
        "3D Projection Engine",
        True,
        WHITE
    )

    screen.blit(
        title,
        (20, 20)
    )

    # Draw axes
    draw_axes(
        mode,
        angle_x,
        angle_y,
        angle_z
    )

    # Draw cube
    draw_cube(
        mode,
        angle_x,
        angle_y,
        angle_z
    )

    # Vanishing point
    draw_vanishing_point()


    # =====================
    # INFORMATION
    # =====================

    mode_text = FONT.render(
        f"Projection: {mode}",
        True,
        YELLOW
    )

    screen.blit(
        mode_text,
        (20, 60)
    )

    rotation_text = SMALL_FONT.render(
        f"Rotation X: {angle_x:.0f}  "
        f"Y: {angle_y:.0f}  "
        f"Z: {angle_z:.0f}",
        True,
        WHITE
    )

    screen.blit(
        rotation_text,
        (20, 95)
    )


    # =====================
    # CONTROLS
    # =====================

    controls = [
        "1 - Orthographic",
        "2 - Cavalier Oblique",
        "3 - Cabinet Oblique",
        "4 - Perspective",
        "Arrow Keys - Rotate X/Y",
        "Q / E - Rotate Z",
        "R - Reset Rotation",
        "ESC - Quit"
    ]

    y_position = 150

    for text in controls:

        surface = SMALL_FONT.render(
            text,
            True,
            WHITE
        )

        screen.blit(
            surface,
            (20, y_position)
        )

        y_position += 25


    # =====================
    # DISPLAY
    # =====================

    pygame.display.flip()

    clock.tick(60)


pygame.quit()
