import pygame


class Treasure:
    def __init__(self, pos_x, pos_y, width, height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.treasure = pygame.transform.scale(
            pygame.image.load("./assets/crystals.png"), (self.width, self.height)
        )
        self.hitbox = pygame.Rect(
            self.pos_x,
            self.pos_y,
            self.width,
            self.height,
        )

    def draw(self, win):
        win.blit(self.treasure, (self.pos_x, self.pos_y))

        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def captured(self, zombie):
        if zombie.hitbox[0] in range(self.hitbox[0], self.hitbox[0] + self.hitbox[2]):
            return True

        if zombie.hitbox[0] + zombie.hitbox[2] in range(
            self.hitbox[0], self.hitbox[0] + self.hitbox[2]
        ):
            return True
