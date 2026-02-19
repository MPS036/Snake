class Cube:
    """
    Represents a single square (segment) of the snake or a snack.
    """

    def __init__(self, start, direction=(1, 0), color=(255, 0, 0)):
        """
        Initialize a cube.

        Args:
            start: Tuple (x, y) grid position.
            direction: Movement direction as (dx, dy).
            color: RGB color of the cube.
        """
        self.pos = start
        self.x, self.y = direction
        self.color = color

    def move(self, x: int, y: int, rows: int) -> None:
        """
        Move cube in a direction with wrap-around logic.

        Args:
            x: Horizontal direction (-1, 0, 1).
            y: Vertical direction (-1, 0, 1).
            rows: Grid size for wrap-around.
        """
        self.x = x
        self.y = y
        self.pos = ((self.pos[0] + self.x) % rows,
                    (self.pos[1] + self.y) % rows)

    def draw(self, surface, cell_size: int, eyes: bool = False) -> None:
        """
        Draw cube on the screen.

        Args:
            surface: Pygame surface.
            cell_size: Size of grid cell in pixels.
            eyes: Whether to draw eyes (used for snake head).
        """
        i, j = self.pos
        pygame.draw.rect(
            surface,
            self.color,
            (i * cell_size + 1,
             j * cell_size + 1,
             cell_size - 2,
             cell_size - 2),
        )

        if eyes:
            center = cell_size // 2
            radius = 3
            circle1 = (i * cell_size + center - radius, j * cell_size + 8)
            circle2 = (i * cell_size + cell_size - radius * 2, j * cell_size + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle1, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle2, radius)

class Snake:
    """
    Represents the snake entity.

    Handles:
    - Movement
    - Direction changes
    - Growth
    - Self-collision
    """

    def __init__(self, color, pos, rows):
        """
        Initialize the snake.

        Args:
            color: RGB color.
            pos: Starting position (x, y).
            rows: Grid size.
        """
        self.color = color
        self.rows = rows
        self.head = Cube(pos, direction=(0, 1), color=color)
        self.body = [self.head]
        self.turns = {}
        self.x = 0
        self.y = 1

    def handle_input(self) -> None:
        """
        Handle keyboard input and update direction.

        Prevents 180-degree turns.
        """
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

    def move(self) -> None:
        """
        Move the snake forward and process direction turns.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        self.handle_input()

        for i, cube in enumerate(self.body):
            p = cube.pos
            if p in self.turns:
                dx, dy = self.turns[p]
                cube.move(dx, dy, self.rows)
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                cube.move(cube.x, cube.y, self.rows)

    def reset(self, pos) -> None:
        """
        Reset snake to initial state after game over.

        Args:
            pos: Starting position.
        """
        self.head = Cube(pos, direction=(0, 1), color=self.color)
        self.body = [self.head]
        self.turns = {}
        self.x = 0
        self.y = 1

    def add_cube(self) -> None:
        """
        Add a new segment to the snake tail.
        """
        tail = self.body[-1]
        dx, dy = tail.x, tail.y

        new_pos = ((tail.pos[0] - dx) % self.rows,
                   (tail.pos[1] - dy) % self.rows)

        self.body.append(Cube(new_pos,
                              direction=(dx, dy),
                              color=self.color))

    def draw(self, surface, cell_size: int) -> None:
        """
        Draw the entire snake.
        """
        for i, cube in enumerate(self.body):
            cube.draw(surface, cell_size, eyes=(i == 0))

def draw_grid(surface, width: int, rows: int) -> None:
    """
    Draw grid lines on the playing field.
    """
    cell = width // rows
    for i in range(rows):
        x = i * cell
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(surface, (255, 255, 255), (0, x), (width, x))

def redraw_window(surface, width, rows, snake, snack) -> None:
    """
    Redraw all game elements on the screen.
    """
    surface.fill((0, 0, 0))
    cell = width // rows
    snake.draw(surface, cell)
    snack.draw(surface, cell)
    draw_grid(surface, width, rows)
    pygame.display.update()

def random_snack(rows: int, snake: Snake):
    """
    Generate a random position for snack
    that does not overlap the snake body.
    """
    positions = {cube.pos for cube in snake.body}
    while True:
        pos = (random.randrange(rows), random.randrange(rows))
        if pos not in positions:
            return pos

def message_box(subject: str, content: str) -> None:
    """
    Show a simple popup message using tkinter.
    """
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    root.destroy()

def main() -> None:
    """
    Initialize and run the main game loop.
    """
    width = 500
    rows = 20

    pygame.init()
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption("Snake")

    snake = Snake((255, 0, 0), (rows // 2, rows // 2), rows)
    snack = Cube(random_snack(rows, snake), color=(0, 255, 0))

    clock = pygame.time.Clock()

    while True:
        pygame.time.delay(50)
        clock.tick(10)

        snake.move()

        if snake.body[0].pos == snack.pos:
            snake.add_cube()
            snack = Cube(random_snack(rows, snake), color=(0, 255, 0))

        head_pos = snake.body[0].pos
        if head_pos in [c.pos for c in snake.body[1:]]:
            message_box("You Lost!", "Play again?")
            snake.reset((rows // 2, rows // 2))

        redraw_window(win, width, rows, snake, snack)

if __name__ == "__main__":
    main()
