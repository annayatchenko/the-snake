"""
Игра 'Змейка'.

Запуск: python the_snake.py
Зависимость: pygame

Правила:
- Управляйте зеленой змейкой с помощью стрелок.
- Собирайте красные яблоки и избегайте жёлтых груш, уменьшающих змейку.
- Запрещён разворот на 180°.
- При столкновении змейки с собой, игра стартует заново.
"""

from random import choice, randint

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


class GameObject:
    """Базовый класс для игровых объектов. Определяет их позицию и цвет."""

    def __init__(self, position=None, body_color=None):
        """Инициализирует базовые атрибуты игрового объекта."""
        if position is None:
            self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки игровых объектов."""
        raise NotImplementedError(
            'Метод draw() должен быть переопределен в дочернем классе!'
        )


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self, occupied_spaces=None, body_color=APPLE_COLOR):
        """Инициализирует базовые атрибуты яблока."""
        super().__init__((0, 0), body_color)
        if occupied_spaces is None:
            occupied_spaces = []
        self.randomize_position(occupied_spaces)

    def randomize_position(self, occupied_spaces):
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            random_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            random_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (random_x, random_y)

            if new_position not in occupied_spaces:
                self.position = new_position
                break

    def draw(self, screen):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Pear(GameObject):
    """Класс, описывающий грушу."""

    def __init__(self, occupied_spaces=None, body_color=PEAR_COLOR):
        """Инициализирует базовые атрибуты груши."""
        super().__init__((0, 0), body_color)
        if occupied_spaces is None:
            occupied_spaces = []
        self.randomize_position(occupied_spaces)

    def randomize_position(self, occupied_spaces):
        """Устанавливает случайное положение груши на игровом поле."""
        while True:
            random_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            random_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (random_x, random_y)

            if new_position not in occupied_spaces:
                self.position = new_position
                break

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
        possible_directions = [UP, DOWN, LEFT, RIGHT]
        self.direction = choice(possible_directions)
        self.last = []

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, next_direction):
        """Обновляет направление после нажатия на кнопку."""
        if next_direction:
            self.direction = next_direction

    def move(self):
        """Обновляет позицию змейки, сдвигая голову и убирая хвост."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        # Вычисляем новые координаты головы с учетом прохода сквозь стены
        new_head = (
            (head_x + dir_x * GRID_SIZE) % (GRID_WIDTH * GRID_SIZE),
            (head_y + dir_y * GRID_SIZE) % (GRID_HEIGHT * GRID_SIZE)
        )

        # Добавляем новую голову в начало списка
        self.positions.insert(0, new_head)
        self.last = []

        # Если длина змейки не увеличилась (яблоко не съедено), убираем хвост
        while len(self.positions) > self.length:
            self.last.append(self.positions.pop())

    def draw(self, screen):
        """Отрисовывает голову змейки и затирает хвост."""
        # Отрисовка головы змейки
        head_rect = pygame.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента, если нужно
        for tail in self.last:
            last_rect = pygame.Rect(tail, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def pop_tail(self):
        """Мгновенно удаляет лишний хвост при уменьшении длины."""
        if self.positions:
            # Отрезаем сегмент и сохраняем в self.last
            self.last = self.positions.pop()


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для изменения направления змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit('Игра успешно завершена./The game is over.')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                return UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                return DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                return LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                return RIGHT


def reset_game(snake, apple, pear):
    """Возвращает игру к начальному состоянию после проигрыша."""
    snake.reset()
    screen.fill(BOARD_BACKGROUND_COLOR)
    # Генерируем новые случайные позиции для еды без наложений
    apple.randomize_position(snake.positions)
    occupied = snake.positions + [apple.position]
    pear.randomize_position(occupied)
    # Отрисовываем объекты заново на чистом поле
    apple.draw(screen)
    pear.draw(screen)


def main():
    """Основная функция, задающая игровой цикл."""
    pygame.init()
    screen.fill(BOARD_BACKGROUND_COLOR)

    snake = Snake()
    apple = Apple(occupied_spaces=snake.positions)
    current_occupied = snake.positions + [apple.position]
    pear = Pear(occupied_spaces=current_occupied)

    apple.draw(screen)
    pear.draw(screen)

    while True:
        clock.tick(SPEED)

        new_direction = handle_keys(snake)

        # Обновление состояний объектов
        snake.update_direction(new_direction)
        snake.move()

        # Проверка: съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            occupied = snake.positions + [pear.position]
            apple.randomize_position(occupied)
            apple.draw(screen)
        # Проверка: съела ли змейка грушу
        elif snake.get_head_position() == pear.position:
            snake.length -= 1
            # Если длина стала меньше 1 — перезапускаем игру
            if snake.length < 1:
                reset_game(snake, apple, pear)
            else:
                # Переразмещаем грушу относительно змейки и яблока
                occupied = snake.positions + [apple.position]
                pear.randomize_position(occupied)
                pear.draw(screen)
        # Проверка: столкнулась ли змейка сама со собой
        elif snake.get_head_position() in snake.positions[1:]:
            reset_game(snake, apple, pear)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
