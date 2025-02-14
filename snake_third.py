from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 640
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
POISON_COLOR = (105, 0, 198)

FPS = 10

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


class GameObj:
    def __init__(self, body_color):
        self.body_color = body_color
        self.position = None
        self.rand_pos()

    def rand_pos(self):
        """Устанавливает случайную позицию объекта."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Отрисовывает объект на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def interact(self, snake):
        """
        Метод взаимодействия объекта со змейкой.
        Должен быть переопределён в наследниках.
        """
        pass


class Apple(GameObj):
    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)

    def interact(self, snake):
        """При столкновении с яблоком змейке добавляется один сегмент."""
        snake.length += 1
        self.rand_pos()


class Poison(GameObj):
    def __init__(self, body_color=POISON_COLOR):
        super().__init__(body_color)

    def interact(self, snake):
        """
        При столкновении с ядом уменьшается длина змейки на один,
        либо змея перезапускается, если её длина равна 1.
        """
        if snake.length > 1:
            snake.length -= 1
            snake.positions.pop()
        else:
            snake.reset()
        self.rand_pos()


class Stone(GameObj):
    def __init__(self, body_color=(122, 127, 128)):
        super().__init__(body_color)

    def interact(self, snake):
        """При столкновении со стеной змейка погибает (перезапуск)."""
        snake.reset()
        self.rand_pos()


class PlayerControl:
    def __init__(self, body_color):
        self.body_color = body_color

    def move(self):
        """Логика перемещения. Должна быть реализована в наследнике."""
        pass

    def draw(self):
        """Отрисовка игрока. Должна быть реализована в наследнике."""
        pass

    def handle_input(self, event):
        """Обработка ввода игрока. Может быть расширена в наследнике."""
        pass


class Snake(PlayerControl):
    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()

    def reset(self):
        """Сбрасывает состояние змейки."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            # Запрещаем разворот назад
            if ((self.next_direction[0] * -1, self.next_direction[1] * -1)
                    != self.direction):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку по экрану."""
        self.update_direction()
        current = self.positions[0]
        dx, dy = self.direction
        new_position = ((current[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
                        (current[1] + dy * GRID_SIZE) % SCREEN_HEIGHT)
        if new_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
            else:
                self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def draw(self):
        """Отрисовывает змейку на экране."""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        for pos in self.positions[1:]:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def handle_input(self, event):
        """Обрабатывает нажатия клавиш для управления направлением змейки."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != DOWN:
                self.next_direction = UP
            elif event.key == pygame.K_DOWN and self.direction != UP:
                self.next_direction = DOWN
            elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                self.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                self.next_direction = RIGHT


class Game:
    """
    Класс,который будет инкапсулировать саму игру.
    Здесь внедряются зависимости: змейка и список объектов,
    с которыми она может взаимодействовать.
    """
    def __init__(self, snake, game_objects):
        self.snake = snake #вот тут высокоуровневый модуль Game не будет зависеть на прямую от PC
        self.game_objects = game_objects
        self.running = True

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.snake.handle_input(event)

    def update(self):
        self.snake.move()
        head_pos = self.snake.get_head_position()
        for obj in self.game_objects:
            if head_pos == obj.position:
                obj.interact(self.snake)

    def draw(self):
        screen.fill(BOARD_BACKGROUND_COLOR)
        for obj in self.game_objects:
            obj.draw()
        self.snake.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            clock.tick(FPS)
            self.process_events()
            self.update()
            self.draw()
        pygame.quit()


def main():
    snake = Snake()
    game_objects = [Apple(), Poison(), Stone()]

    game = Game(snake, game_objects)
    game.run()


if __name__ == "__main__":
    main()
    
'''Вместо того, чтобы функция main сама содержала весь игровой цикл 
и знала детали его реализации, мы выделили класс Game. 
который зависит от абстракций (объекты, реализующие методы draw и interact),
 а конкретные реализации передаются извне.'''

#Абстракция не должна зависеть от деталей, детали должны зависеть от абстракций.
#Классы должны зависеть от абстракций, а не от конкретных реализаций.
