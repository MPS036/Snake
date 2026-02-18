import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Cube:
    def __init__(self, start, direction=(1, 0), color=(255, 0, 0)):
        self.pos = start
        self.x, self.y = direction
        self.color = color

    def move(self, x, y, rows):
        self.x = x
        self.y = y
        self.pos = ((self.pos[0] + self.x) % rows, (self.pos[1] + self.y) % rows)

    def draw(self, surface, cell_size, eyes=False):
        i, j = self.pos
        pygame.draw.rect(
            surface,
            self.color,
            (i * cell_size + 1, j * cell_size + 1, cell_size - 2, cell_size - 2),
        )
        if eyes:
            center = cell_size // 2
            radius = 3
            circle1 = (i * cell_size + center - radius, j * cell_size + 8)
            circle2 = (i * cell_size + cell_size - radius * 2, j * cell_size + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle1, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle2, radius)

class Snake:
    def __init__(self, color, pos, rows):
        self.color = color
        self.rows = rows
        self.head = Cube(pos, direction=(0, 1), color=color)
        self.body = [self.head]
        self.turns = {}
        self.x = 0
        self.y = 1

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x != 1:
            self.x, self.y = -1, 0
            self.turns[self.head.pos] = (self.x, self.y)
        elif keys[pygame.K_RIGHT] and self.x != -1:
            self.x, self.y = 1, 0
            self.turns[self.head.pos] = (self.x, self.y)
        elif keys[pygame.K_DOWN] and self.y != -1:
            self.x, self.y = 0, 1
            self.turns[self.head.pos] = (self.x, self.y)
        elif keys[pygame.K_UP] and self.y != 1:
            self.x, self.y = 0, -1
            self.turns[self.head.pos] = (self.x, self.y)

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        self.handle_input()

        for i, c in enumerate(self.body):
            p = c.pos
            if p in self.turns:
                dx, dy = self.turns[p]
                c.move(dx, dy, self.rows)
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.x, c.y, self.rows)

    def reset(self, pos):
        self.head = Cube(pos, direction=(0, 1), color=self.color)
        self.body = [self.head]
        self.turns = {}
        self.x = 0
        self.y = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.x, tail.y

        new_pos = ((tail.pos[0] - dx) % self.rows, (tail.pos[1] - dy) % self.rows)
        new_cube = Cube(new_pos, direction=(dx, dy), color=self.color)
        self.body.append(new_cube)

    def draw(self, surface, cell_size):
        for i, c in enumerate(self.body):
            c.draw(surface, cell_size, eyes=(i == 0))

def draw_grid(surface, width, rows):
    cell = width // rows
    for i in range(rows):
        x = i * cell
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(surface, (255, 255, 255), (0, x), (width, x))

def redraw_window(surface, width, rows, sn, snack):
    surface.fill((0, 0, 0))
    cell = width // rows
    sn.draw(surface, cell)
    snack.draw(surface, cell)
    draw_grid(surface, width, rows)
    pygame.display.update()

def random_snack(rows, snake):
    positions = {c.pos for c in snake.body}
    while True:
        pos = (random.randrange(rows), random.randrange(rows))
        if pos not in positions:
            return pos

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    root.destroy()

def main():
    width = 500
    rows = 20

    pygame.init()
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption("Snake")

    sn = Snake((255, 0, 0), (rows // 2, rows // 2), rows)
    snack = Cube(random_snack(rows, sn), color=(0, 255, 0))

    clock = pygame.time.Clock()

    while True:
        pygame.time.delay(50)
        clock.tick(10)

        sn.move()

        if sn.body[0].pos == snack.pos:
            sn.add_cube()
            snack = Cube(random_snack(rows, sn), color=(0, 255, 0))

        head_pos = sn.body[0].pos
        if head_pos in [c.pos for c in sn.body[1:]]:
            message_box("You Lost!", "Play again?")
            sn.reset((rows // 2, rows // 2))

        redraw_window(win, width, rows, sn, snack)

if __name__ == "__main__":
    main()
