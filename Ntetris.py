import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 300, 600
CELL_SIZE = 30
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

COLORS = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 255, 255),
    (128, 0, 128)
]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

screen = pygame.display.set_mode((WIDTH + 100, HEIGHT))
pygame.display.set_caption("Тетрис")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.randint(1, len(COLORS) - 1)
        self.rotation = 0

    def image(self):
        return self.shape[self.rotation % len(self.shape)]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

def create_new_piece():
    shape = random.choice(SHAPES)
    x = COLS // 2 - len(shape[0]) // 2
    return Piece(x, 0, shape)

def valid_position(grid, piece):
    for i, row in enumerate(piece.image()):
        for j, cell in enumerate(row):
            if cell:
                x = piece.x + j
                y = piece.y + i
                if x < 0 or x >= COLS or y >= ROWS:
                    return False
                if y >= 0 and grid[y][x]:
                    return False
    return True

def lock_piece(grid, piece):
    for i, row in enumerate(piece.image()):
        for j, cell in enumerate(row):
            if cell:
                x = piece.x + j
                y = piece.y + i
                if y >= 0:
                    grid[y][x] = piece.color

def clear_lines(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_grid)
    while len(new_grid) < ROWS:
        new_grid.insert(0, [0 for _ in range(COLS)])
    return new_grid, lines_cleared

def draw_text(text, x, y, color=(255,255,255)):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def main():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    current_piece = create_new_piece()
    next_piece = create_new_piece()
    fall_time = 0
    fall_speed = 500
    level = 1
    score = 0
    lines_cleared_total = 0
    game_over = False
    lines_to_next_level = 10
    line_animation = []
    pause = False
    down_pressed = False

    while True:
        dt = clock.tick(60)
        if not pause and not game_over:
            fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if not game_over:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not valid_position(grid, current_piece):
                            current_piece.x += 1
                    elif event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not valid_position(grid, current_piece):
                            current_piece.x -= 1
                    elif event.key == pygame.K_DOWN:
                        down_pressed = True
                        current_piece.y += 1
                        if not valid_position(grid, current_piece):
                            current_piece.y -= 1
                    elif event.key == pygame.K_UP:
                        original_rotation = current_piece.rotation
                        current_piece.rotate()
                        if not valid_position(grid, current_piece):
                            for _ in range(3):
                                current_piece.rotate()
                    elif event.key == pygame.K_SPACE:
                        pause = not pause
                    elif event.key == pygame.K_r:
                        grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                        current_piece = create_new_piece()
                        next_piece = create_new_piece()
                        fall_time = 0
                        level = 1
                        score = 0
                        lines_cleared_total = 0
                        game_over = False
                        lines_to_next_level = 10
                        line_animation.clear()
                elif event.key == pygame.K_r:
                    # Перезапуск после окончания игры
                    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                    current_piece = create_new_piece()
                    next_piece = create_new_piece()
                    fall_time = 0
                    level = 1
                    score = 0
                    lines_cleared_total = 0
                    game_over = False
                    lines_to_next_level = 10
                    line_animation.clear()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    down_pressed = False

        if not pause and not game_over:
            # Ускоренное падение при удержании DOWN
            if down_pressed:
                fall_speed_current = 50
            else:
                fall_speed_current = fall_speed

            if fall_time > fall_speed_current:
                fall_time = 0
                current_piece.y += 1
                if not valid_position(grid, current_piece):
                    current_piece.y -= 1
                    lock_piece(grid, current_piece)
                    grid, lines_cleared = clear_lines(grid)
                    lines_cleared_total += lines_cleared
                    score += lines_cleared * 100
                    if lines_cleared > 0:
                        line_animation.extend([(y, 0) for y in range(ROWS - lines_cleared, ROWS)])
                    current_piece = next_piece
                    next_piece = create_new_piece()
                    if not valid_position(grid, current_piece):
                        game_over = True

            if lines_cleared_total >= lines_to_next_level:
                level += 1
                lines_to_next_level += 10
                fall_speed = max(100, fall_speed - 50)

        # Анимация линий
        if line_animation:
            for i in range(len(line_animation)):
                y, alpha = line_animation[i]
                if alpha < 255:
                    alpha += 15
                    line_animation[i] = (y, alpha)
            line_animation = [item for item in line_animation if item[1] < 255]

        # Отрисовка
        screen.fill(COLORS[0])

        # Поле
        for y in range(ROWS):
            for x in range(COLS):
                if grid[y][x]:
                    pygame.draw.rect(screen, COLORS[grid[y][x]],
                                     (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Текущая фигура
        for i, row in enumerate(current_piece.image()):
            for j, cell in enumerate(row):
                if cell:
                    x = (current_piece.x + j) * CELL_SIZE
                    y = (current_piece.y + i) * CELL_SIZE
                    pygame.draw.rect(screen, COLORS[current_piece.color],
                                     (x, y, CELL_SIZE, CELL_SIZE))
        # Следующая фигура
        for i, row in enumerate(next_piece.shape[0]):
            for j, cell in enumerate(row):
                if cell:
                    x = WIDTH + 10 + j * CELL_SIZE
                    y = 50 + i * CELL_SIZE
                    pygame.draw.rect(screen, COLORS[next_piece.color],
                                     (x, y, CELL_SIZE, CELL_SIZE))
        draw_text("Следующая", WIDTH + 10, 20)
        # Очки и уровень
        draw_text(f"Очки: {score}", WIDTH + 10, 200)
        draw_text(f"Уровень: {level}", WIDTH + 10, 240)

        # Анимация линий
        for y, alpha in line_animation:
            overlay = pygame.Surface((WIDTH, CELL_SIZE))
            overlay.set_alpha(alpha)
            overlay.fill((255, 255, 255))
            screen.blit(overlay, (0, y * CELL_SIZE))

        # Текст
        if game_over:
            draw_text("Игра окончена! R - перезапуск", 20, HEIGHT // 2, color=(255,0,0))
        elif pause:
            draw_text("Пауза (Esc - выйти, R - перезапуск)", 20, HEIGHT // 2, color=(255,255,0))

        pygame.display.flip()

if __name__ == "__main__":
    main()