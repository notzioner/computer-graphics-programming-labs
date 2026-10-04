# 3D Coordinate Geometry & Spatial
# Bounding Volumes (AABB/Sphere)

import pygame
import math
import random

pygame.init()

# =========================
# WINDOW SETTINGS
# =========================

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Activity 3 - 3D Coordinate Geometry")

clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 28)
SMALL_FONT = pygame.font.Font(None, 22)

# =========================
# COLORS
# =========================

BLACK = (20, 20, 25)
WHITE = (240, 240, 240)
GRAY = (100, 100, 100)
RED = (220, 80, 80)
GREEN = (80, 220, 120)
BLUE = (80, 150, 240)
YELLOW = (240, 220, 80)


# =========================
# 3D POINT
# =========================

class Point3D:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance_to(self, other):
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )

    def subtract(self, other):
        return Point3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def dot(self, other):
        return (
            self.x * other.x +
            self.y * other.y +
            self.z * other.z
        )

    def cross(self, other):
        return Point3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )


# =========================
# SPHERE
# =========================

class Sphere3D:

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def contains_point(self, point):
        return self.center.distance_to(point) <= self.radius

    def intersects_sphere(self, other):

        dx = self.center.x - other.center.x
        dy = self.center.y - other.center.y
        dz = self.center.z - other.center.z

        distance_squared = (
            dx * dx +
            dy * dy +
            dz * dz
        )

        radius_sum = self.radius + other.radius

        return distance_squared <= radius_sum * radius_sum


# =========================
# AABB
# =========================

class AABB:

    def __init__(self, min_pt, max_pt):
        self.min_pt = min_pt
        self.max_pt = max_pt

    def intersects(self, other):

        return (
            self.min_pt.x <= other.max_pt.x and
            self.max_pt.x >= other.min_pt.x and

            self.min_pt.y <= other.max_pt.y and
            self.max_pt.y >= other.min_pt.y and

            self.min_pt.z <= other.max_pt.z and
            self.max_pt.z >= other.min_pt.z
        )


# =========================
# 3D OBJECT
# =========================

class Object3D:

    def __init__(self):

        self.center = Point3D(
            random.uniform(-200, 200),
            random.uniform(-150, 150),
            random.uniform(100, 500)
        )

        self.radius = random.uniform(10, 25)

        self.sphere = Sphere3D(
            self.center,
            self.radius
        )

        self.aabb = AABB(
            Point3D(
                self.center.x - self.radius,
                self.center.y - self.radius,
                self.center.z - self.radius
            ),
            Point3D(
                self.center.x + self.radius,
                self.center.y + self.radius,
                self.center.z + self.radius
            )
        )


# =========================
# CREATE 100 OBJECTS
# =========================

objects = []

for i in range(100):
    objects.append(Object3D())


# =========================
# 3D PROJECTION
# =========================

def project_point(point):

    camera_distance = 600

    scale = camera_distance / (
        camera_distance + point.z
    )

    x = int(
        WIDTH // 2 +
        point.x * scale
    )

    y = int(
        HEIGHT // 2 -
        point.y * scale
    )

    return x, y, scale


# =========================
# DRAW 3D AXES
# =========================

def draw_axes():

    origin = Point3D(0, 0, 0)

    x_axis = Point3D(150, 0, 0)
    y_axis = Point3D(0, 150, 0)
    z_axis = Point3D(0, 0, 150)

    origin_2d = project_point(origin)

    x_2d = project_point(x_axis)
    y_2d = project_point(y_axis)
    z_2d = project_point(z_axis)

    pygame.draw.line(
        screen,
        RED,
        origin_2d[:2],
        x_2d[:2],
        3
    )

    pygame.draw.line(
        screen,
        GREEN,
        origin_2d[:2],
        y_2d[:2],
        3
    )

    pygame.draw.line(
        screen,
        BLUE,
        origin_2d[:2],
        z_2d[:2],
        3
    )

    screen.blit(
        FONT.render("X", True, RED),
        x_2d[:2]
    )

    screen.blit(
        FONT.render("Y", True, GREEN),
        y_2d[:2]
    )

    screen.blit(
        FONT.render("Z", True, BLUE),
        z_2d[:2]
    )


# =========================
# DRAW OBJECT
# =========================

def draw_object(obj, collision):

    x, y, scale = project_point(
        obj.center
    )

    radius = max(
        2,
        int(obj.radius * scale)
    )

    if collision:
        color = YELLOW
    else:
        color = BLUE

    # Bounding sphere
    pygame.draw.circle(
        screen,
        color,
        (x, y),
        radius,
        1
    )

    # Center point
    pygame.draw.circle(
        screen,
        WHITE,
        (x, y),
        3
    )

    # AABB projection
    min_x, min_y, _ = project_point(
        obj.aabb.min_pt
    )

    max_x, max_y, _ = project_point(
        obj.aabb.max_pt
    )

    left = min(min_x, max_x)
    top = min(min_y, max_y)

    width = abs(max_x - min_x)
    height = abs(max_y - min_y)

    pygame.draw.rect(
        screen,
        GREEN if not collision else RED,
        (left, top, width, height),
        1
    )


# =========================
# TASK 3.2
# =========================

P = Point3D(2, -1, 7)
Q = Point3D(1, -3, 5)

example_distance = P.distance_to(Q)


# =========================
# TASK 3.3
# =========================

sphere_center = Point3D(-2, 3, -1)
sphere_radius = math.sqrt(8)


# =========================
# COLLISION CHECK
# =========================

def check_collisions():

    collisions = set()

    for i in range(len(objects)):

        for j in range(i + 1, len(objects)):

            sphere_a = objects[i].sphere
            sphere_b = objects[j].sphere

            box_a = objects[i].aabb
            box_b = objects[j].aabb

            # Broad-phase:
            # Sphere + AABB

            if sphere_a.intersects_sphere(sphere_b):

                if box_a.intersects(box_b):

                    collisions.add(i)
                    collisions.add(j)

    return collisions


# =========================
# MAIN LOOP
# =========================

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            # Regenerate objects
            if event.key == pygame.K_r:

                objects.clear()

                for i in range(100):
                    objects.append(Object3D())


    # =========================
    # UPDATE
    # =========================

    collision_objects = check_collisions()


    # =========================
    # RENDER
    # =========================

    screen.fill(BLACK)

    draw_axes()

    # Draw objects from farthest
    # to nearest

    objects_sorted = sorted(
        objects,
        key=lambda obj: obj.center.z,
        reverse=True
    )

    for i, obj in enumerate(objects):

        if obj in objects_sorted:

            collision = (
                objects.index(obj)
                in collision_objects
            )

            draw_object(
                obj,
                collision
            )


    # =========================
    # INFORMATION PANEL
    # =========================

    title = FONT.render(
        "3D Coordinate Geometry & Bounding Volumes",
        True,
        WHITE
    )

    screen.blit(
        title,
        (20, 20)
    )

    info1 = SMALL_FONT.render(
        f"Objects: {len(objects)}",
        True,
        WHITE
    )

    info2 = SMALL_FONT.render(
        f"Sphere/AABB Collisions: {len(collision_objects)} objects",
        True,
        WHITE
    )

    info3 = SMALL_FONT.render(
        f"Example 3 Distance: {example_distance:.1f}",
        True,
        WHITE
    )

    info4 = SMALL_FONT.render(
        f"Example 5 Radius: {sphere_radius:.3f}",
        True,
        WHITE
    )

    info5 = SMALL_FONT.render(
        "R - Regenerate Objects    ESC - Quit",
        True,
        WHITE
    )

    screen.blit(info1, (20, 55))
    screen.blit(info2, (20, 80))
    screen.blit(info3, (20, 105))
    screen.blit(info4, (20, 130))
    screen.blit(info5, (20, HEIGHT - 35))


    # =========================
    # LEGEND
    # =========================

    pygame.draw.circle(
        screen,
        BLUE,
        (850, 55),
        8
    )

    screen.blit(
        SMALL_FONT.render(
            "Normal Object",
            True,
            WHITE
        ),
        (865, 45)
    )

    pygame.draw.circle(
        screen,
        YELLOW,
        (850, 85),
        8
    )

    screen.blit(
        SMALL_FONT.render(
            "Collision",
            True,
            WHITE
        ),
        (865, 75)
    )


    # =========================
    # DISPLAY
    # =========================

    pygame.display.flip()

    clock.tick(60)


pygame.quit()
