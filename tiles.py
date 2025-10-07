import pygame
import random

pygame.init()

GRID_SIZE = 60
GRID_WIDTH = 13
GRID_HEIGHT = 10
WIDTH, HEIGHT = GRID_SIZE * GRID_WIDTH, GRID_SIZE * GRID_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

COLORS = [
    (255, 102, 153),  # Bright Pastel Red
    (102, 255, 178),  # Bright Pastel Green
    (102, 204, 255),  # Bright Pastel Blue
    (255, 255, 102),  # Bright Pastel Yellow
    (255, 102, 255),  # Bright Pastel Magenta
    (255, 178, 102),  # Bright Pastel Orange
    (204, 153, 255),  # Bright Pastel Purple
    (153, 255, 255),  # Bright Pastel Cyan
    (255, 153, 204),  # Bright Pastel Pink
    (204, 255, 153),  # Bright Pastel Lime
]

grid = [[random.randint(0, len(COLORS)-1) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
selected = []
score = 0
fade_tiles = []

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile = grid[y][x]
            rect = pygame.Rect(x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE)
            fade = next((f for f in fade_tiles if f[0] == x and f[1] == y), None)
            if fade:
                color = COLORS[tile] if tile is not None else (50, 50, 50)
                s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                s.fill((*color, fade[2]))
                screen.blit(s, rect)
            else:
                color = COLORS[tile] if tile is not None else (50, 50, 50)
                pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0,0,0), rect, 1)
            if (x, y) in selected:
                pygame.draw.rect(screen, (255,255,255), rect, 3)

def handle_click(pos):
    global selected, score, fade_tiles
    x, y = pos[0] // GRID_SIZE, pos[1] // GRID_SIZE
    if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
        return
    if grid[y][x] is None:
        return
    if (x, y) in selected:
        selected.remove((x, y))
        return
    selected.append((x, y))
    if len(selected) == 2:
        x1, y1 = selected[0]
        x2, y2 = selected[1]
        if grid[y1][x1] == grid[y2][x2]:
            fade_tiles.append((x1, y1, 255))
            fade_tiles.append((x2, y2, 255))
            score += 10
        selected = []

def refill_grid():
    for x in range(GRID_WIDTH):
        col = [grid[y][x] for y in range(GRID_HEIGHT)]
        col = [c for c in col if c is not None]
        missing = GRID_HEIGHT - len(col)
        col = [None]*missing + col
        for y in range(GRID_HEIGHT):
            grid[y][x] = col[y]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] is None:
                grid[y][x] = random.randint(0, len(COLORS)-1)

def draw_score():
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, (80,80,80))
    screen.blit(text, (10, HEIGHT-40))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())
    screen.fill((0,0,0))
    draw_grid()
    draw_score()

    if fade_tiles:
        for i in range(len(fade_tiles)-1, -1, -1):
            x, y, alpha = fade_tiles[i]
            alpha -= 25
            if alpha <= 0:
                grid[y][x] = None
                fade_tiles.pop(i)
            else:
                fade_tiles[i] = (x, y, alpha)

    pygame.display.flip()
    clock.tick(60)
