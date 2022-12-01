import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, x=1, y=0, color = (255, 0, 0)):
        self.pos = start
        self.x = 1
        self.y = 0
        self.color = color

    def move(self, x, y):
        self.x = x
        self.y = y
        self.pos = (self.pos[0] + self.x, self.pos[1] + self.y)

    def draw(self, area, eyes = False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(area, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            center = dis // 2
            radius = 3
            circle_middle = (i * dis + center - radius, j * dis + 8)
            circle_middle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(area, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(area, (0, 0, 0), circle_middle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.x = 0
        self.y = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.x = -1
                    self.y = 0
                    self.turns[self.head.pos[:]] = [self.x, self.y]

                elif keys[pygame.K_RIGHT]:
                    self.x = 1
                    self.y = 0
                    self.turns[self.head.pos[:]] = [self.x, self.y]

                elif keys[pygame.K_DOWN]:
                    self.x = 0
                    self.y = 1
                    self.turns[self.head.pos[:]] = [self.x, self.y]

                elif keys[pygame.K_UP]:
                    self.x = 0
                    self.y = -1
                    self.turns[self.head.pos[:]] = [self.x, self.y]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.x == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.x == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.y == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.y == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.x, c.y)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.x = 0
        self.y = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.x, tail.y
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))
        self.body[-1].x = dx
        self.body[-1].y = dy

    def draw(self, area):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(area, True)
            else:
                c.draw(area)


def draw_field(w, rows, area):
    size = w // rows
    x = 0
    y = 0
    for i in range(rows):
        x = x + size
        y = y + size
        pygame.draw.line(area, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(area, (255, 255, 255), (0, y), (w, y))


def remake_window(area):
    global width, rows, sn, snack
    area.fill((0, 0, 0))
    sn.draw(area)
    snack.draw(area)
    draw_field(width, rows, area)
    pygame.display.update()


def random_snack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, sn, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    sn = snake((255, 0, 0), (10, 10))
    snack = cube(random_snack(rows, sn), color = (0, 255, 0))
    flag = True
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        sn.move()
        if sn.body[0].pos == snack.pos:
            sn.add_cube()
            snack = cube(random_snack(rows, sn), color = (0, 255, 0))
        for x in range(len(sn.body)):
            if sn.body[x].pos in list(map(lambda z: z.pos, sn.body[x+1:])):
                message_box("You Lost!", "Play again?")
                sn.reset((10, 10))
                break
        remake_window(win)
    pass


main()