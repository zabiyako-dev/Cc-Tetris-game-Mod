import pygame
import random
import sys

# --- Константы ---

pygame.init()
SCREEN_WIDTH = 300  # 10 блоков * 30 px
SCREEN_HEIGHT = 600  # 20 блоков * 30 px
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

COLORS = {
    'I': (64, 224, 208),   # Тёмно-бирюзовый
    'O': (218, 165, 32),   # Золотисто-жёлтый
    'T': (147, 112, 219),  # Темно-фиолетовый
    'S': (60, 179, 113),   # Морская волна
    'Z': (178, 34, 34),    # Тёмно-красный
    'J': (65, 105, 225),   # Королевский синий
    'L': (205, 133, 63),   # Персиково-коричневый
}
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SHAPES = {
    'S': [
        [(0, 1), (1, 1), (1, 0), (2, 0)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
    ],
    'Z': [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (2, 1), (1, 1), (1, 2)],
    ],
    'I': [
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
    ],
    'O': [
        [(0, 0), (1, 0), (0, 1), (1, 1)],
    ],
    'J': [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    'L': [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
    'T': [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
}

class Piece:
    def __init__(self, x, y, shape_key):
        self.x = x
        self.y = y
        self.shape_key = shape_key
        self.shape = SHAPES[shape_key]
        self.color = COLORS[shape_key]
        self.rotation = 0

    def image(self):
        return self.shape[self.rotation % len(self.shape)]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

def create_board():
    return [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def valid_space(piece, board):
    for x_off, y_off in piece.image():
        x = piece.x + x_off
        y = piece.y + y_off
        if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
            return False
        if y >= 0 and board[y][x] != BLACK:
            return False
    return True

def add_piece_to_board(board, piece):
    for x_off, y_off in piece.image():
        x = piece.x + x_off
        y = piece.y + y_off
        if y >= 0:
            board[y][x] = piece.color

def clear_rows(board):
    cleared = 0
    for i in reversed(range(len(board))):
        if BLACK not in board[i]:
            del board[i]
            board.insert(0, [BLACK for _ in range(BOARD_WIDTH)])
            cleared += 1
    return cleared

def draw_board(surface, board):
    surface.fill(BLACK)
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            color = board[y][x]
            if color != BLACK:
                pygame.draw.rect(surface, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                # Убрана серая сетка (обводка)

def draw_piece(surface, piece):
    for x_off, y_off in piece.image():
        x = piece.x + x_off
        y = piece.y + y_off
        if y >= 0:
            pygame.draw.rect(surface, piece.color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            # Убрана серая сетка (обводка)

def draw_window(screen, board, current_piece, paused, player_name, font, score):
    screen.fill(BLACK)
    draw_board(screen, board)
    draw_piece(screen, current_piece)

    # Отобразить имя игрока и статус паузы
    name_surface = font.render(f"Игрок: {player_name}", True, WHITE)
    screen.blit(name_surface, (SCREEN_WIDTH + 10, 10))

    pause_text = "ПАУЗА" if paused else ""
    pause_surface = font.render(pause_text, True, WHITE)
    screen.blit(pause_surface, (SCREEN_WIDTH + 10, 50))

    # Отобразить очки
    score_surface = font.render(f"Очки: {score}", True, WHITE)
    screen.blit(score_surface, (SCREEN_WIDTH + 10, 90))

    pygame.display.update()

def wait_for_name_input(screen):
    input_text = ""
    font = pygame.font.SysFont('Arial', 30)
    clock = pygame.time.Clock()

    prompt_text = "Введите имя игрока:"

    while True:
        screen.fill(BLACK)
        prompt = font.render(prompt_text, True, WHITE)
        input_surface = font.render(input_text, True, WHITE)
        screen.blit(prompt, (10, 150))
        screen.blit(input_surface, (10, 200))

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        return input_text.strip()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if event.unicode.isprintable():
                        input_text += event.unicode

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH + 150, SCREEN_HEIGHT))
    pygame.display.set_caption("Тетрис с управлением WASD и паузой")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 24)

    player_name = wait_for_name_input(screen)

    board = create_board()
    current_piece = Piece(BOARD_WIDTH // 2 - 2, 0, random.choice(list(SHAPES.keys())))
    fall_time = 0
    fall_speed = 0.5  # время в секундах между падениями на 1 клетку
    paused = False
    space_held = False
    score = 0  # Добавляем счётчик очков

    running = True
    while running:
        dt = clock.tick(60) / 1000  # секунды
        if not paused:
            fall_time += dt

        keys = pygame.key.get_pressed()
        space_held = keys[pygame.K_SPACE]

        current_fall_speed = 0.05 if space_held and not paused else fall_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                elif paused and event.key == pygame.K_SPACE:
                    running = False

                if not paused:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        current_piece.x -= 1
                        if not valid_space(current_piece, board):
                            current_piece.x += 1
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        current_piece.x += 1
                        if not valid_space(current_piece, board):
                            current_piece.x -= 1
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        current_piece.y += 1
                        if not valid_space(current_piece, board):
                            current_piece.y -= 1
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        current_piece.rotate()
                        if not valid_space(current_piece, board):
                            # вернуть назад
                            current_piece.rotation = (current_piece.rotation - 1) % len(SHAPES[current_piece.shape_key])

        if not paused and fall_time > current_fall_speed:
            current_piece.y += 1
            if not valid_space(current_piece, board):
                current_piece.y -= 1
                add_piece_to_board(board, current_piece)
                cleared = clear_rows(board)
                if cleared > 0:
                    score += cleared * 100  # Присваиваем 100 очков за каждую очищенную линию
                current_piece = Piece(BOARD_WIDTH // 2 - 2, 0, random.choice(list(SHAPES.keys())))
                if not valid_space(current_piece, board):
                    # Конец игры — выйти из цикла
                    running = False
            fall_time = 0

        draw_window(screen, board, current_piece, paused, player_name, font, score)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
