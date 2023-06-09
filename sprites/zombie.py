import pygame
import random


class Zombie:
    def __init__(self, pos_y, width, height):
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.attrs = [
            [1, 2],
            [3, 3],
            [5, 4],
        ]
        self.velocity = random.choice(self.attrs[0])
        self.lives = random.choice(self.attrs[1])
        self.max_lives = self.lives
        self.direction = random.choice(["left", "right"])
        self.zombie_right = pygame.transform.scale(
            pygame.image.load("./assets/zombie.png"), (self.width, self.height)
        )
        self.zombie_left = pygame.transform.flip(self.zombie_right, True, False)

        if self.direction == "left":
            self.pos_x = 1000

        else:
            self.pos_x = -self.width

        self.hitbox = pygame.Rect(
            self.pos_x + 33,
            self.pos_y,
            self.width - 65,
            self.height,
        )

    def draw(self, win):
        if self.direction == "left":
            win.blit(self.zombie_left, (self.pos_x, self.pos_y))

        else:
            win.blit(self.zombie_right, (self.pos_x, self.pos_y))

        # Draw health bar background
        health_bar_width = self.hitbox[2]
        health_bar_height = 10
        health_bar_x = self.hitbox[0]
        health_bar_y = self.pos_y - health_bar_height - 5
        pygame.draw.rect(
            win,
            (255, 0, 0),
            (health_bar_x, health_bar_y, health_bar_width, health_bar_height),
        )

        # Draw health bar
        health_bar_width = int((self.lives / self.max_lives) * self.hitbox[2])
        pygame.draw.rect(
            win,
            (0, 255, 0),
            (health_bar_x, health_bar_y, health_bar_width, health_bar_height),
        )

        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.direction == "left":
            self.pos_x -= self.velocity
            self.hitbox = pygame.Rect(
                self.pos_x + 33,
                self.pos_y,
                self.width - 65,
                self.height,
            )

        else:
            self.pos_x += self.velocity
            self.hitbox = pygame.Rect(
                self.pos_x + 33,
                self.pos_y,
                self.width - 65,
                self.height,
            )

    def got_hit(self, bullet):
        if bullet.direction == "left":
            if bullet.hitbox[0] in range(
                self.hitbox[0], self.hitbox[0] + self.hitbox[2]
            ):
                if self.lives > 0:
                    self.lives -= 1
                    return True

        elif bullet.direction == "right":
            if bullet.inverted_hitbox[0] in range(
                self.hitbox[0], self.hitbox[0] + self.hitbox[2]
            ):
                if self.lives > 0:
                    self.lives -= 1
                    return True

        return False
