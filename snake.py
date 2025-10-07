import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1000, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)

COLORS = [
    ("Green", (50, 220, 50)),
    ("Blue", (70, 130, 255)),
    ("Orange", (255, 140, 40)),
    ("Purple", (170, 80, 255)),
    ("Red", (240, 60, 60)),
    ("Pink", (255, 105, 180)),
]

snake = [(5, 5)]
direction = (1, 0)

def place_food():
    return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

food = place_food()

def draw():
    screen.fill(BLACK)

    for x, y in snake:
        pygame.draw.rect(screen, snake_color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    fx, fy = food
    pygame.draw.rect(screen, COLORS[4][1], (fx * GRID_SIZE, fy * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.display.update()

def handle_keys():
    global direction
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP] and direction != (0, 1):
        direction = (0, -1)
    elif keys[pygame.K_DOWN] and direction != (0, -1):
        direction = (0, 1)
    elif keys[pygame.K_LEFT] and direction != (1, 0):
        direction = (-1, 0)
    elif keys[pygame.K_RIGHT] and direction != (-1, 0):
        direction = (1, 0)

def move_snake():
    head_x, head_y = snake[-1]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    snake.append(new_head)

    global food
    if new_head == food:
        food = place_food()
    else:
        snake.pop(0)

def check_collision():
    head_x, head_y = snake[-1]

    if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
        return True

    if (head_x, head_y) in snake[:-1]:
        return True
    return False


def show_menu():
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)
    
    menu = True
    difficulties = [("Easy", 10), ("Medium", 15), ("Hard", 20)]
    selected = 0
    while menu:
        screen.fill(BLACK)
        title = font.render("Classical Snake Game", True, COLORS[0][1])
        prompt = small_font.render("Choose Difficulty", True, COLORS[4][1])
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))
        
        for i, (name, _) in enumerate(difficulties):
            color = COLORS[0][1] if i ==selected else COLORS[4][1]
            diff_surface = small_font.render(name, True, color)
            x = WIDTH // 2 - diff_surface.get_width() // 2 + (i - 1) * 200
            y = HEIGHT // 2 + 50
            screen.blit(diff_surface, (x, y))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(difficulties)
                elif event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(difficulties)
                elif event.key == pygame.K_RETURN:
                    menu = False


    menu = True
    color_selected = 0
    while menu:
        screen.fill(BLACK)
        title = font.render("Classical Snake Game", True, COLORS[0][1])
        prompt = small_font.render("Choose Snake Color", True, COLORS[4][1])
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))

        for i, (name, _) in enumerate(COLORS):
            color = COLORS[0][1] if i == color_selected else COLORS[4][1]
            diff_surface = small_font.render(name, True, color)
            x = WIDTH // 2 - diff_surface.get_width() // 2 + (i - len(COLORS)//2) * 150
            y = HEIGHT // 2 + 50
            screen.blit(diff_surface, (x, y))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    color_selected = (color_selected - 1) % len(COLORS)
                elif event.key == pygame.K_RIGHT:
                    color_selected = (color_selected + 1) % len(COLORS)
                elif event.key == pygame.K_RETURN:
                    menu = False

        snake_color = COLORS[color_selected][1]

    return difficulties[selected][1], snake_color 

speed, snake_color = show_menu()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_keys()
    move_snake()
    if check_collision():
        running = False

    draw()
    clock.tick(speed)

print("Game Over! Score:", len(snake) - 1)
pygame.quit()
