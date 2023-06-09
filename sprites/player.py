import pygame


class Player:
    def __init__(self, pos_x, pos_y, width, height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.velocity = 3
        self.lives = 3
        self.max_lives = self.lives
        self.direction = "right"
        self.player_right = pygame.transform.scale(
            pygame.image.load("./assets/player.png"), (self.width, self.height)
        )
        self.player_left = pygame.transform.flip(self.player_right, True, False)
        self.hitbox = pygame.Rect(
            self.pos_x + 20,
            self.pos_y,
            self.width - 40,
            self.height,
        )

    def draw(self, win):
        if self.direction == "left":
            win.blit(self.player_left, (self.pos_x, self.pos_y))

        else:
            win.blit(self.player_right, (self.pos_x, self.pos_y))

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

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.direction = "left"
            self.pos_x -= self.velocity
            self.hitbox = pygame.Rect(
                self.pos_x + 20,
                self.pos_y,
                self.width - 40,
                self.height,
            )

        if keys[pygame.K_RIGHT]:
            self.direction = "right"
            self.pos_x += self.velocity
            self.hitbox = pygame.Rect(
                self.pos_x + 20,
                self.pos_y,
                self.width - 40,
                self.height,
            )

    def got_hit(self, zombie, spawned_zombies):
        if zombie.hitbox[0] in range(self.hitbox[0], self.hitbox[0] + self.hitbox[2]):
            if self.lives > 0:
                self.lives -= 1
            if zombie in spawned_zombies:
                spawned_zombies.remove(zombie)

        elif zombie.hitbox[0] + zombie.hitbox[2] in range(
            self.hitbox[0], self.hitbox[0] + self.hitbox[2]
        ):
            if self.lives > 0:
                self.lives -= 1
            if zombie in spawned_zombies:
                spawned_zombies.remove(zombie)

    def died(self):
        if self.lives <= 0:
            return True
