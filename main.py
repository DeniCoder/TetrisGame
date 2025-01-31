import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 400, 700
BLOCK_SIZE = 30

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (0, 255, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (128, 0, 128)
]

# Формы фигур
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Тетрис")

# Шрифты
font = pygame.font.SysFont("comicsans", 30)
small_font = pygame.font.SysFont("comicsans", 20)

# Функция для отрисовки текста
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Функция для создания новой фигуры
def new_figure():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return {
        'shape': shape,
        'color': color,
        'x': WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2,
        'y': 0
    }

# Функция для проверки столкновений
def check_collision(board, figure):
    for y, row in enumerate(figure['shape']):
        for x, cell in enumerate(row):
            if cell:
                if (figure['y'] + y >= len(board) or
                    figure['x'] + x < 0 or
                    figure['x'] + x >= len(board[0]) or
                    board[figure['y'] + y][figure['x'] + x]):
                    return True
    return False

# Функция для добавления фигуры на доску
def add_figure_to_board(board, figure):
    for y, row in enumerate(figure['shape']):
        for x, cell in enumerate(row):
            if cell:
                board[figure['y'] + y][figure['x'] + x] = figure['color']

# Функция для удаления заполненных линий
def remove_completed_lines(board):
    lines_to_remove = [i for i, row in enumerate(board) if all(row)]
    for i in lines_to_remove:
        del board[i]
        board.insert(0, [None for _ in range(WIDTH // BLOCK_SIZE)])
    return len(lines_to_remove)

# Функция для отрисовки доски
def draw_board(surface, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Функция для отрисовки фигуры
def draw_figure(surface, figure):
    for y, row in enumerate(figure['shape']):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, figure['color'], ((figure['x'] + x) * BLOCK_SIZE, (figure['y'] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Основная функция игры
def main():
    # Создание доски
    board = [[None for _ in range(WIDTH // BLOCK_SIZE)] for _ in range(HEIGHT // BLOCK_SIZE)]

    # Создание первой фигуры
    figure = new_figure()

    # Счет
    score = 0

    # Скорость падения
    fall_speed = 0.3  # Увеличили скорость падения
    fall_time = 0

    # Инициализация часов для контроля FPS
    clock = pygame.time.Clock()

    # Основной цикл игры
    running = True
    while running:
        screen.fill(WHITE)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    figure['x'] -= 1
                    if check_collision(board, figure):
                        figure['x'] += 1
                if event.key == pygame.K_RIGHT:
                    figure['x'] += 1
                    if check_collision(board, figure):
                        figure['x'] -= 1
                if event.key == pygame.K_DOWN:
                    figure['y'] += 1
                    if check_collision(board, figure):
                        figure['y'] -= 1
                if event.key == pygame.K_UP:
                    # Поворот фигуры
                    rotated_figure = list(zip(*reversed(figure['shape'])))
                    if not check_collision(board, {'shape': rotated_figure, 'x': figure['x'], 'y': figure['y']}):
                        figure['shape'] = rotated_figure

        # Падение фигуры
        fall_time += clock.get_rawtime() / 100  # Используем clock.get_rawtime()
        if fall_time >= fall_speed:
            fall_time = 0
            figure['y'] += 1
            if check_collision(board, figure):
                figure['y'] -= 1
                add_figure_to_board(board, figure)
                lines_removed = remove_completed_lines(board)
                score += lines_removed * 100
                figure = new_figure()
                if check_collision(board, figure):
                    running = False

        # Отрисовка доски и фигуры
        draw_board(screen, board)
        draw_figure(screen, figure)

        # Отрисовка счета
        draw_text(f"Score: {score}", small_font, BLACK, screen, WIDTH // 2, 10)

        # Обновление экрана
        pygame.display.update()

        # Управление FPS
        clock.tick(30)  # Ограничиваем FPS до 30

    # Вывод итогового счета
    screen.fill(WHITE)
    draw_text(f"Game Over! Final Score: {score}", font, BLACK, screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.update()
    pygame.time.wait(3000)  # Пауза перед закрытием

# Функция для отображения стартового экрана
def start_screen():
    screen.fill(WHITE)
    draw_text("Тетрис", font, BLACK, screen, WIDTH // 2, HEIGHT // 4)
    draw_text("Управление:", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 80)
    draw_text("Влево: Клавиша Left", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text("Вправо: Клавиша Right", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 20)
    draw_text("Вниз: Клавиша Down", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 10)
    draw_text("Поворот: Клавиша Up", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 40)
    draw_text("Нажмите любую клавишу для старта", small_font, BLACK, screen, WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                waiting = False

# Запуск игры
start_screen()
main()
pygame.quit()