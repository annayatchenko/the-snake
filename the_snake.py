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

# Цвет груши (плохой еды)
PEAR_COLOR = (255, 255, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка/The snake')

# Иконка игры:
icon = pygame.image.load('green python.jpeg')
pygame.display.set_icon(icon)

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс для игровых объектов.
    Определяет позицию и цвет бъекта.
    """

    def __init__(self, position=None, body_color=None):
        """Инициализирует базовые атрибуты игрового объекта."""
        if position is None:
            self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Метод для отрисовки игровых объектов.
        Должен переопределяться в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        """Инициализирует базовые атрибуты яблока."""
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        random_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        random_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (random_x, random_y)

    def draw(self, screen):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Pear(GameObject):
    """Класс, описывающий грушу."""

    def __init__(self):
        """Инициализирует базовые атрибуты груши."""
        super().__init__((0, 0), PEAR_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение груши на игровом поле."""
        random_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        random_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (random_x, random_y)

    def draw(self, screen):
        """Отрисовывает грушу на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self):
        """Инициализирует базовые атрибуты змейки."""
        super().__init__(None, SNAKE_COLOR)
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки, добавляя новую голову в начало списка
        и удаляя последний элемент, если длина змейки не увеличилась.
        """
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        # Вычисляем новые координаты головы с учетом прохода сквозь стены
        new_head = (
            (head_x + dir_x * GRID_SIZE) % (GRID_WIDTH * GRID_SIZE),
            (head_y + dir_y * GRID_SIZE) % (GRID_HEIGHT * GRID_SIZE)
        )

        # Добавляем новую голову в начало списка
        self.positions.insert(0, new_head)

        # Если длина змейки не увеличилась (яблоко не съедено), убираем хвост
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self, screen):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
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


def main():
    """Основная функция, задающая игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    screen.fill(BOARD_BACKGROUND_COLOR)

    apple = Apple()
    pear = Pear()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        # Обновление состояний объектов
        snake.update_direction()
        snake.move()

        # Проверка: съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Защита от появления яблока прямо внутри змейки
            while apple.position in snake.positions:
                apple.randomize_position()
        # Проверка: съела ли змейка грушу
        elif snake.get_head_position() == pear.position:
            snake.length -= 1
            # Если длина стала меньше 1 — перезапускаем игру
            if snake.length < 1:
                snake.reset()
                apple.randomize_position()
                pear.randomize_position()
                screen.fill(BOARD_BACKGROUND_COLOR)
            else:
                # Нам нужно удалить лишний сегмент с экрана прямо сейчас
                if len(snake.positions) > 0:
                    removed_tail = snake.positions.pop()
                    tail_rect = pygame.Rect(
                        removed_tail, (GRID_SIZE, GRID_SIZE)
                    )
                    pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, tail_rect)
            # Перемещаем грушу
            while True:
                pear.randomize_position()
                if (
                    pear.position not in snake.positions
                    and pear.position != apple.position
                ):
                    break
        # Проверка: столкнулась ли змейка сама со собой
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            # Полная очистка экрана при перезапуске
            screen.fill(BOARD_BACKGROUND_COLOR)
        # Отрисовка изменений на экране
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        pear.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
