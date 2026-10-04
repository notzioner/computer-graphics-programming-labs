# Activity 5: Hardware Graphics Pipeline & Shading
# with PyOpenGL

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# =========================
# INITIALIZE PYGAME
# =========================

pygame.init()

display = (1000, 700)

pygame.display.set_mode(
    display,
    DOUBLEBUF | OPENGL
)

pygame.display.set_caption(
    "Activity 5 - Hardware Graphics Pipeline"
)


# =========================
# OPENGL SETUP
# =========================

gluPerspective(
    45,
    display[0] / display[1],
    0.1,
    50.0
)

glTranslatef(
    0.0,
    0.0,
    -8.0
)


# Enable depth buffering
glEnable(GL_DEPTH_TEST)

# Enable transparency
glEnable(GL_BLEND)

glBlendFunc(
    GL_SRC_ALPHA,
    GL_ONE_MINUS_SRC_ALPHA
)

# Smooth shading
glShadeModel(GL_SMOOTH)


# =========================
# CUBE VERTICES
# =========================

vertices = [
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),

    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
]


# =========================
# CUBE COLORS
# =========================

colors = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),

    (1, 0, 1),
    (0, 1, 1),
    (1, 1, 1),
    (0.5, 0.5, 0.5)
]


# =========================
# CUBE SURFACES
# =========================

surfaces = [
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
]


# =========================
# DRAW COLORED CUBE
# =========================

def draw_colored_cube():

    glBegin(GL_QUADS)

    for surface in surfaces:

        for vertex_index in surface:

            glColor3fv(
                colors[vertex_index]
            )

            glVertex3fv(
                vertices[vertex_index]
            )

    glEnd()


# =========================
# DRAW CUBE WITH ALPHA
# =========================

def draw_transparent_cube():

    glBegin(GL_QUADS)

    for surface in surfaces:

        for vertex_index in surface:

            color = colors[vertex_index]

            glColor4f(
                color[0],
                color[1],
                color[2],
                0.35
            )

            glVertex3fv(
                vertices[vertex_index]
            )

    glEnd()


# =========================
# DRAW ARTICULATED ARM
# =========================

def draw_articulated_arm():

    # ---------------------
    # Upper arm
    # ---------------------

    glPushMatrix()

    glTranslatef(
        -3.0,
        0.0,
        0.0
    )

    glRotatef(
        arm_angle,
        0,
        0,
        1
    )

    glScalef(
        0.7,
        2.0,
        0.7
    )

    glColor3f(
        0.2,
        0.8,
        1.0
    )

    draw_colored_cube()

    glPopMatrix()


    # ---------------------
    # Lower arm
    # ---------------------

    glPushMatrix()

    glTranslatef(
        -3.0,
        -2.0,
        0.0
    )

    glRotatef(
        -arm_angle * 1.5,
        0,
        0,
        1
    )

    glTranslatef(
        0.0,
        -1.2,
        0.0
    )

    glScalef(
        0.6,
        1.5,
        0.6
    )

    glColor3f(
        1.0,
        0.6,
        0.2
    )

    draw_colored_cube()

    glPopMatrix()


    # ---------------------
    # Hand
    # ---------------------

    glPushMatrix()

    glTranslatef(
        -3.0,
        -4.0,
        0.0
    )

    glRotatef(
        arm_angle,
        0,
        0,
        1
    )

    glScalef(
        0.8,
        0.8,
        0.8
    )

    glColor3f(
        1.0,
        0.8,
        0.2
    )

    draw_colored_cube()

    glPopMatrix()


# =========================
# ROTATION VARIABLES
# =========================

cube_rotation = 0.0

arm_angle = 0.0


# =========================
# MOVEMENT VARIABLES
# =========================

scene_x = 0.0
scene_y = 0.0
scene_z = 0.0

scene_rot_x = 0.0
scene_rot_y = 0.0

movement_speed = 0.05
rotation_speed = 1.5


running = True

clock = pygame.time.Clock()


# =========================
# MAIN LOOP
# =========================

while running:

    # =====================
    # EVENTS
    # =====================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            # Reset controls
            if event.key == pygame.K_r:

                scene_x = 0.0
                scene_y = 0.0
                scene_z = 0.0

                scene_rot_x = 0.0
                scene_rot_y = 0.0


    # =====================
    # CONTROLS
    # =====================

    keys = pygame.key.get_pressed()


    # Move left / right
    if keys[pygame.K_a]:
        scene_x -= movement_speed

    if keys[pygame.K_d]:
        scene_x += movement_speed


    # Move up / down
    if keys[pygame.K_q]:
        scene_y += movement_speed

    if keys[pygame.K_e]:
        scene_y -= movement_speed


    # Move forward / backward
    if keys[pygame.K_w]:
        scene_z += movement_speed

    if keys[pygame.K_s]:
        scene_z -= movement_speed


    # Rotate left / right
    if keys[pygame.K_LEFT]:
        scene_rot_y -= rotation_speed

    if keys[pygame.K_RIGHT]:
        scene_rot_y += rotation_speed


    # Rotate up / down
    if keys[pygame.K_UP]:
        scene_rot_x -= rotation_speed

    if keys[pygame.K_DOWN]:
        scene_rot_x += rotation_speed


    # =====================
    # UPDATE
    # =====================

    cube_rotation += 1.0

    arm_angle += 1.5

    # Keep angles manageable
    if cube_rotation >= 360:
        cube_rotation = 0

    if arm_angle >= 360:
        arm_angle = 0


    # =====================
    # CLEAR BUFFERS
    # =====================

    glClear(
        GL_COLOR_BUFFER_BIT |
        GL_DEPTH_BUFFER_BIT
    )


    # =====================
    # APPLY CONTROLS
    # =====================

    glPushMatrix()

    glTranslatef(
        scene_x,
        scene_y,
        scene_z
    )

    glRotatef(
        scene_rot_x,
        1,
        0,
        0
    )

    glRotatef(
        scene_rot_y,
        0,
        1,
        0
    )


    # =====================
    # MAIN ROTATING CUBE
    # =====================

    glPushMatrix()

    glTranslatef(
        1.0,
        0.5,
        0.0
    )

    glRotatef(
        cube_rotation,
        1,
        1,
        0
    )

    glScalef(
        1.3,
        1.3,
        1.3
    )

    draw_colored_cube()

    glPopMatrix()


    # =====================
    # ARTICULATED ARM
    # =====================

    draw_articulated_arm()


    # =====================
    # TRANSPARENT CUBE 1
    # =====================

    glPushMatrix()

    glTranslatef(
        3.0,
        -1.5,
        -1.5
    )

    glRotatef(
        cube_rotation,
        0,
        1,
        0
    )

    draw_transparent_cube()

    glPopMatrix()


    # =====================
    # TRANSPARENT CUBE 2
    # =====================

    glPushMatrix()

    glTranslatef(
        3.5,
        -1.5,
        0.5
    )

    glRotatef(
        -cube_rotation,
        1,
        0,
        0
    )

    draw_transparent_cube()

    glPopMatrix()


    # End scene movement
    glPopMatrix()


    # =====================
    # DISPLAY
    # =====================

    pygame.display.flip()

    clock.tick(60)
pygame.quit()
