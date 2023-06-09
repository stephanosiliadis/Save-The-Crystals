import pygame
import sys, os

from sprites.player import Player
from sprites.zombie import Zombie
from sprites.bullet import Bullet
from sprites.treasure import Treasure


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pygame.init()
font = pygame.font.Font(None, 36)

# Game Constants:
RUN = True
CLOCK = pygame.time.Clock()
FPS = 60
ACCEPT_INPUT = True

# Dimensions:
WIDTH, HEIGHT = 1000, 450
PLAYER_WIDTH, PLAYER_HEIGHT = 150, 150
ZOMBIE_WIDTH, ZOMBIE_HEIGHT = 150, 150
BULLET_WIDTH, BULLET_HEIGHT = 25, 25
TREASURE_WIDTH, TREASURE_HEIGHT = PLAYER_WIDTH // 2, PLAYER_HEIGHT // 2

# Positions:
PLAYER_X, PLAYER_Y = WIDTH // 2 - PLAYER_WIDTH, HEIGHT - PLAYER_HEIGHT
ZOMBIE_Y = HEIGHT - ZOMBIE_HEIGHT
BULLET_Y = PLAYER_Y + BULLET_HEIGHT + 28
TREASURE_X, TREASURE_Y = WIDTH // 2 - TREASURE_WIDTH, HEIGHT - TREASURE_HEIGHT

# Colors:
WHITE = (255, 255, 255)

# Images:
ICON = pygame.image.load(resource_path("assets\\crystals.png"))
BACKGROUND = pygame.transform.scale(
    pygame.image.load(resource_path("assets\\background.jpg")), (WIDTH, HEIGHT)
)
BACKGROUND_WIN = pygame.transform.scale(
    pygame.image.load(resource_path("assets\\bg_win.jpg")), (WIDTH, HEIGHT)
)
BACKGROUND_LOSS = pygame.transform.scale(
    pygame.image.load(resource_path("assets\\bg_loss.jpg")), (WIDTH, HEIGHT)
)


# Other Constats:
MAX_ZOMBIES = [3, 5, 7]
SPAWNED_ZOMBIES = []

MAX_BULLETS = 7
BULLETS = []

INDEX = 0
STARTS_TICK = pygame.time.get_ticks()

# Window Settings:
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Save the Crystals - Play")
pygame.display.set_icon(ICON)


# Draw Function:
def draw(win):
    global BULLETS, SPAWNED_ZOMBIES
    win.blit(BACKGROUND, (0, 0))

    treasure.draw(win=win)
    player.draw(win=win)

    for zombie in SPAWNED_ZOMBIES:
        zombie.draw(win=win)
        zombie.move()

    for bullet in BULLETS:
        bullet.draw(win=win)
        bullet.move()

    # Draw timer
    seconds = (pygame.time.get_ticks() - STARTS_TICK) / 1000
    timer_text = font.render(f"Time: {int(seconds)}", True, (255, 255, 255))
    win.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))

    pygame.display.update()


# Reset Game:
def reset_game():
    global SPAWNED_ZOMBIES, BULLETS, INDEX, STARTS_TICK, player
    SPAWNED_ZOMBIES = []
    BULLETS = []
    INDEX = 0
    STARTS_TICK = pygame.time.get_ticks()
    player = Player(
        pos_x=PLAYER_X,
        pos_y=PLAYER_Y,
        width=PLAYER_WIDTH,
        height=PLAYER_HEIGHT,
    )


# Win / Loss Functions:
def end_game(win, result, reason_of_loss: str = None, time: int = None):
    global accept_input
    accept_input = False

    if result == "win":
        win.blit(BACKGROUND_WIN, (0, 0))
        win_text = font.render(
            "You managed to survive and save the power crystals! (Survived for 3 minutes)",
            True,
            (255, 255, 255),
        )
        win.blit(
            win_text,
            (
                WIDTH // 2 - win_text.get_width() // 2,
                HEIGHT // 2 - win_text.get_height() // 2,
            ),
        )

    else:
        win.blit(BACKGROUND_LOSS, (0, 0))
        loss_text = font.render(
            f"You lost - {reason_of_loss} (Survived for {round(time)} seconds)",
            True,
            (255, 255, 255),
        )
        win.blit(
            loss_text,
            (
                WIDTH // 2 - loss_text.get_width() // 2,
                HEIGHT // 2 - loss_text.get_height() // 2,
            ),
        )

    pygame.display.update()
    pygame.time.delay(3000)
    reset_game()
    accept_input = True


# Initialize objects:
player = Player(
    pos_x=PLAYER_X,
    pos_y=PLAYER_Y,
    width=PLAYER_WIDTH,
    height=PLAYER_HEIGHT,
)
treasure = Treasure(
    pos_x=TREASURE_X,
    pos_y=TREASURE_Y,
    width=TREASURE_WIDTH,
    height=TREASURE_HEIGHT,
)

# Game Loop:
while RUN:
    CLOCK.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

        # Check for bullet firing:
        if ACCEPT_INPUT and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(BULLETS) <= MAX_BULLETS:
                if player.direction == "left":
                    direction = "left"

                else:
                    direction = "right"
                bullet = Bullet(
                    pos_x=player.pos_x,
                    pos_y=BULLET_Y,
                    width=BULLET_WIDTH,
                    height=BULLET_HEIGHT,
                    direction=direction,
                )
                BULLETS.append(bullet)

    keys = pygame.key.get_pressed()
    player.move(keys=keys)

    # Spawn Zombies:
    SECONDS = (pygame.time.get_ticks() - STARTS_TICK) / 1000
    if SECONDS > 30 and INDEX == 0:
        INDEX = 1

    elif SECONDS > 60 and INDEX == 1:
        INDEX = 2

    if len(SPAWNED_ZOMBIES) <= MAX_ZOMBIES[INDEX]:
        zombie = Zombie(
            pos_y=ZOMBIE_Y,
            width=ZOMBIE_WIDTH,
            height=ZOMBIE_HEIGHT,
        )
        SPAWNED_ZOMBIES.append(zombie)

    # Check if the zombie hitted the player:
    for zombie in SPAWNED_ZOMBIES:
        player.got_hit(zombie=zombie, spawned_zombies=SPAWNED_ZOMBIES)

        # Check if the zombie captured the treasure:
        captured = treasure.captured(zombie=zombie)
        if captured:
            end_game(
                win=win,
                result="loss",
                reason_of_loss="The zombies captured the crystals!",
                time=SECONDS,
            )

    # Check if the bullet left the screen:
    for bullet in BULLETS:
        if (
            bullet.hitbox[0] <= 0
            or bullet.inverted_hitbox[0] + bullet.inverted_hitbox[2] >= WIDTH
        ):
            BULLETS.remove(bullet)

    for bullet in BULLETS:
        for zombie in SPAWNED_ZOMBIES:
            hit_zombie = zombie.got_hit(bullet=bullet)
            if hit_zombie:
                if bullet in BULLETS:
                    BULLETS.remove(bullet)  

                if zombie.lives == 0:
                    SPAWNED_ZOMBIES.remove(zombie)

    # Game over conditions:
    if player.died():
        end_game(
            win=win,
            result="loss",
            reason_of_loss="The zombies killed you!",
            time=SECONDS,
        )

    if SECONDS >= 180:
        end_game(win=win, result="win", reason_of_loss=None, time=None)

    draw(win=win)

pygame.quit()
sys.exit(0)
