import pygame


class Bullet:
    def __init__(self, pos_x, pos_y, width, height, direction):
        self.pos_x = pos_x
        self.inverted_x = self.pos_x + 110
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.direction = direction
        self.velocity = 4
        self.hitbox = pygame.Rect(
            self.pos_x,
            self.pos_y + 7,
            self.width,
            self.height - 15,
        )
        self.inverted_hitbox = pygame.Rect(
            self.inverted_x,
            self.pos_y + 7,
            self.width,
            self.height - 15,
        )
        self.bullet = pygame.transform.scale(
            pygame.image.load("./assets/bullet.png"), (self.width, self.height)
        )
        self.bullet_left = pygame.transform.rotate(self.bullet, 90)
        self.bullet_right = pygame.transform.flip(self.bullet_left, True, False)

    def draw(self, win):
        if self.direction == "left":
            win.blit(self.bullet_left, (self.pos_x, self.pos_y))
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

        else:
            win.blit(self.bullet_right, (self.inverted_x, self.pos_y))
            # pygame.draw.rect(win, (255, 0, 0), self.inverted_hitbox, 2)

    def move(self):
        if self.direction == "left":
            self.pos_x -= self.velocity
            self.hitbox = pygame.Rect(
                self.pos_x,
                self.pos_y + 7,
                self.width,
                self.height - 15,
            )

        else:
            self.inverted_x += self.velocity
            self.inverted_hitbox = pygame.Rect(
                self.inverted_x,
                self.pos_y + 7,
                self.width,
                self.height - 15,
            )
