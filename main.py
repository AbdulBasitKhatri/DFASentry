import pygame
import math
import random

# ==================== INIT ====================
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DFA Sentinel")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# ==================== COLORS ====================
WHITE = (255, 255, 255)
BLUE  = (50, 120, 255)     # Player
RED   = (255, 70, 70)      # Sentry
GOLD  = (255, 200, 0)      # Treasure
BLACK = (0, 0, 0)
GREEN = (60, 200, 60)

# ==================== DFA ====================
DFA = {
    "Patrol": {"f": "Patrol", "n": "Chase", "t": "Catch"},
    "Chase":  {"f": "Patrol", "n": "Chase", "t": "Catch"},
    "Catch":  {"f": "Catch",  "n": "Catch", "t": "Catch"}
}

state = "Patrol"

# ==================== ENTITIES ====================
player = pygame.Rect(100, 100, 30, 30)
sentry = pygame.Rect(400, 300, 40, 40)
treasure = pygame.Rect(600, 350, 30, 30)

PLAYER_SPEED = 5
SENTRY_SPEED = 4

NEAR_DISTANCE = 200
PATROL_RADIUS = 80
patrol_angle = 0.0
returning_to_patrol = False
score = 0
game_over = False
player_won = False

# ==================== FUNCTIONS ====================
def distance(a, b):
    return math.hypot(a.centerx - b.centerx, a.centery - b.centery)

def get_symbol():
    if player.colliderect(sentry):
        return "t"
    elif distance(player, sentry) <= NEAR_DISTANCE:
        return "n"
    else:
        return "f"

def move_towards(rect, target_rect, speed):
    dx = target_rect.centerx - rect.centerx
    dy = target_rect.centery - rect.centery
    dist = math.hypot(dx, dy)
    if dist > 0:
        rect.x += int(speed * dx / dist)
        rect.y += int(speed * dy / dist)

def patrol_around_treasure():
    global patrol_angle, returning_to_patrol

    target_x = treasure.centerx + PATROL_RADIUS * math.cos(patrol_angle)
    target_y = treasure.centery + PATROL_RADIUS * math.sin(patrol_angle)
    target = pygame.Rect(target_x, target_y, 1, 1)

    # Smooth return before orbiting
    if returning_to_patrol:
        move_towards(sentry, target, SENTRY_SPEED)
        if distance(sentry, target) < 5:
            returning_to_patrol = False
    else:
        patrol_angle += 0.03
        sentry.centerx = int(target_x)
        sentry.centery = int(target_y)

def sentry_behavior():
    if state == "Patrol":
        patrol_around_treasure()
    elif state == "Chase":
        move_towards(sentry, player, SENTRY_SPEED)

def reset_game():
    global state, game_over, player_won, returning_to_patrol, patrol_angle, score

    # Reset DFA
    state = "Patrol"

    # Reset flags
    game_over = False
    player_won = False
    returning_to_patrol = False
    patrol_angle = 0.0
    score = 0
    # Reset positions
    player.topleft = (100, 100)
    randomize_treasure()
    sentry.center = (treasure.centerx + PATROL_RADIUS, treasure.centery)

def randomize_treasure():
    margin = 80
    treasure.x = random.randint(margin, WIDTH - margin)
    treasure.y = random.randint(margin, HEIGHT - margin)

randomize_treasure()

# ==================== GAME LOOP ====================
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Restart game on R key
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                reset_game()

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player.y -= PLAYER_SPEED
        if keys[pygame.K_s]: player.y += PLAYER_SPEED
        if keys[pygame.K_a]: player.x -= PLAYER_SPEED
        if keys[pygame.K_d]: player.x += PLAYER_SPEED

        # DFA Update
        symbol = get_symbol()
        next_state = DFA[state][symbol]

        # Detect Chase -> Patrol transition
        if state == "Chase" and next_state == "Patrol":
            returning_to_patrol = True

        state = next_state

        # Sentry movement
        if state != "Catch":
            sentry_behavior()

        # End conditions
        if state == "Catch":
            game_over = True

        if player.colliderect(treasure):
            score += 1
            randomize_treasure()

    # ==================== DRAW ====================
    pygame.draw.rect(screen, GOLD, treasure)
    pygame.draw.rect(screen, BLUE if state != "Catch" else BLACK, player)
    pygame.draw.rect(screen, RED, sentry)

    screen.blit(font.render(f"State: {state}", True, BLACK), (10, 10))
    screen.blit(font.render(f"Symbol: {get_symbol()}", True, BLACK), (10, 40))
    screen.blit(font.render(f"Score: {score}", True, GOLD), (140, 10))

    if game_over:
        if player_won:
            msg = "YOU STOLE THE TREASURE!"
            color = GREEN
            screen.blit(font.render(msg, True, color),((WIDTH / 3.5), HEIGHT // 2))
        else:
            msg = "PLAYER CAUGHT (ACCEPTING STATE)"
            color = RED
            screen.blit(font.render(msg, True, color),((WIDTH // 4), HEIGHT // 2))

        screen.blit(font.render("Press R to Restart", True, BLACK),(WIDTH // 2 - 120, HEIGHT // 2 + 40))

    pygame.display.flip()

pygame.quit()
