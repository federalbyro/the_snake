from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 7.5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()
POISON_COLOR = (105, 0, 198)


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш для изменения направления движения змейки.

    :param game_object: Экземпляр класса Snake.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс для игровых объектов.

    Атрибуты:
        position (tuple): Позиция объекта на игровом поле.
        body_color (tuple): Цвет объекта.
    """

    def __init__(self, position, body_color=None):
        """Comment"""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Comment"""
        pass


class Apple(GameObject):
    """
    Класс, описывающий яблоко в игре.

    Наследуется от GameObject.
    """

    def __init__(self, body_color=APPLE_COLOR):
        """Comment"""
        super().__init__(position=None, body_color=body_color)
        self.randomize_position()

    def randomize_position(self):
        """Comment"""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Comment"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Poison(Apple):
    """Comment"""

    def __init__(self, body_color=POISON_COLOR):
        """Comment"""
        super().__init__(body_color=body_color)
        self.randomize_position()


class Stone(Apple):
    """Comment"""

    def __init__(self, body_color=(122, 127, 128)):
        """Comment"""
        super().__init__(body_color=body_color)
        self.randomize_position()


class Snake(GameObject):
    """Comment"""

    def __init__(self, body_color=SNAKE_COLOR):
        """Comment"""
        super().__init__(position=None, body_color=body_color)
        self.reset()

    def reset(self):
        """Comment"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Comment"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Comment"""
        self.update_direction()
        # Получаем текущую позицию головы
        current = self.positions[0]
        x, y = self.direction
        new_position = (
            (current[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
            (current[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT,
        )
        if new_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()

    def get_head_position(self):
        """Comment"""
        return self.positions[0]

    def draw(self):
        """Comment"""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def main():
    """Comment"""
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple()
    poison = Poison()
    stone = Stone()
    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        elif snake.get_head_position() == poison.position:
            if snake.length > 1:
                snake.length -= 1
                snake.positions.pop()
            else:
                snake.reset()
            poison.randomize_position()
        elif snake.get_head_position() == stone.position:
            snake.reset()
            stone.randomize_position()
        stone.draw()
        snake.draw()
        poison.draw()
        apple.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
