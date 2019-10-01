import math
import pygame
from Vec2d import Vec2d
pygame.init()

done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
mouseX = 0
mouseY = 0
drawing = []

ratio = 10
numbers = 80

size = ratio * numbers
screen = pygame.display.set_mode([size*2, size])
pygame.display.set_caption("Path Following")
clock = pygame.time.Clock()


def show_drawing():
    pygame.draw.circle(screen, BLUE,  [drawing[0].x, drawing[0].y], 10)
    for i in range(drawing.__len__()-1):
        pygame.draw.line(screen, WHITE, [drawing[i].x, drawing[i].y], [drawing[i+1].x, drawing[i+1].y])


def set_target():
    while drawing[0].distance(vehicle.pos) < ld:
        if len(drawing) == 1:
            break
        drawing.pop(0)


class Vehicle:
    def __init__(self, x, y):
        self.pos = Vec2d(x, y)
        self.vel = 3
        self.acc = 0
        self.theta = 0
        self.delta = 0
        self.alpha = 0
        self.length = 100
        self.kaapa = 0
        self.desired = 0.1
        self.ld = 0

    def update(self):
        if self.delta > 1:
            self.delta = 1
        elif self.delta < -1:
            self.delta = -1
        self.vel += self.acc
        self.pos.x += self.vel * math.cos(-self.theta)
        self.pos.y += self.vel * math.sin(-self.theta)
        self.theta += self.vel * (math.tan(self.delta) / self.length)

    def seek_2(self, point):
        self.ld = self.pos.distance(point)
        self.alpha = (drawing[0].sub_vect(Vec2d(self.pos.x - self.length * math.cos(-self.theta), self.pos.y - self.length * math.sin(-self.theta)))).angle() - self.theta
        self.kaapa = (2 * math.sin(self.alpha)) / self.ld
        if math.atan2(self.kaapa * self.length, 1) - self.delta > 0.02:
            self.delta += 0.03
        elif self.delta - math.atan2(self.kaapa * self.length, 1) > 0.02:
            self.delta -= 0.03

    def show_vehicle(self):
        pygame.draw.polygon(screen, GREEN, rect(self.pos.x + (self.length/2) * math.cos(-self.theta),
                                                self.pos.y + (self.length/2) * math.sin(-self.theta),
                                                -self.theta, self.length, 10))
        pygame.draw.polygon(screen, RED, rect(self.pos.x + self.length * math.cos(-self.theta),
                                              self.pos.y + self.length * math.sin(-self.theta),
                                              -self.delta - self.theta, 40, 17))
        pygame.draw.polygon(screen, RED, rect(self.pos.x, self.pos.y,  -self.theta, 40, 17))


def rect(x, y, angle, w, h):
    return [translate(x, y, angle, -w/2,  h/2),
            translate(x, y, angle,  w/2,  h/2),
            translate(x, y, angle,  w/2, -h/2),
            translate(x, y, angle, -w/2, -h/2)]


def translate(x, y, angle, px, py):
    x1 = x + px * math.cos(angle) - py * math.sin(angle)
    y1 = y + px * math.sin(angle) + py * math.cos(angle)
    return [x1, y1]


vehicle = Vehicle(100, size-100)
ld = 150

while not done:

    clock.tick(80)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if pygame.mouse.get_pressed()[0]:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        if not len(drawing):
            drawing.append(Vec2d(mouseX, mouseY))
        if not drawing[-1].x == mouseX and not drawing[-1].y == mouseY:
            drawing.append(Vec2d(mouseX, mouseY))

    if len(drawing):
        show_drawing()
        set_target()
        vehicle.seek_2(drawing[0])

    vehicle.update()
    vehicle.show_vehicle()
    pygame.display.flip()

pygame.quit()
