from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

Pointer = tuple[int, int]

# Направления движения:
UP: Pointer = (0, -1)
DOWN: Pointer = (0, 1)
LEFT: Pointer = (-1, 0)
RIGHT: Pointer = (1, 0)

COLOR = tuple[int, int, int]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.

class GameObject:
    """Это родительский класс."""

    def __init__(self, body_color: COLOR = (0, 0, 0)):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Этот метод отрисовывает графику."""
        raise NotImplementedError()


class Apple(GameObject):
    """Это класс яблока. Когда змея ест яблоко - она растет."""

    def __init__(self, occupied_positions = None,
                 body_color: COLOR = APPLE_COLOR):
        super().__init__(body_color=body_color)
        if occupied_positions is None:
            occupied_positions = []
        self.position = self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions: list[Pointer]):
        """Это метод генерирует случайные координаты для яблока,
        избегая занятых позиций.
        """
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in occupied_positions:
                return new_position

    def draw(self):
        """Этот метод отрисовывает графику."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Это класс змеи. Мы за нее играем."""

    def __init__(self, body_color: COLOR = SNAKE_COLOR):
        super().__init__(body_color=body_color)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        """Этот метод отрисовывает графику."""
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        for position in self.positions[1:]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def update_direction(self):
        """Этот метод меняет направление движения змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Этот метод перемещает змею в соответствии с текущим направлением."""
        head_x, head_y = self.get_head_position()
        head_x = (head_x + (self.direction[0] * GRID_SIZE)) % SCREEN_WIDTH
        head_y = (head_y + (self.direction[1] * GRID_SIZE)) % SCREEN_HEIGHT
        self.positions.insert(0, (head_x, head_y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Этот отвечает за перезапуск игры в случии проигрыша."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def get_head_position(self):
        """
        Этот метод возвращает позицию головы змеи
        (первый элемент в списке positions).
        """
        return self.positions[0]


def handle_keys(game_object):
    """Эта функция отвечает за обработку нажатия клавиш пользователем."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Это основная функция игры. Здесь выполняются все основные действия."""
    pg.init()
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple = Apple(snake.positions)
        if (snake.positions[0][0] < 0 or snake.positions[0][0] >= SCREEN_WIDTH
                or snake.positions[0][1] < 0
                or snake.positions[0][1] >= SCREEN_HEIGHT):
            snake.reset()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        snake.move()
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
