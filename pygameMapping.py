"""Animates a bouncing ball.

Author : Oliver Steele <oliver.steele@olin.edu>
Course : Olin Software Design Fall 2016
Date   : 2016-10-24
License: MIT LICENSE
"""

import pygame

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


class Ball(object):
    def __init__(self):
        self.radius = 20
        self.reset()

    def step(self):
        self.y += self.dy
        self.dy += .08
        if self.y > 480 - self.radius and self.dy > 0:
            self.dy *= -1
        self.dy *= 0.99

    def reset(self):
        self.x = 320
        self.y = 240
        self.dy = 0

    def contains_pt(self, pt):
        return (self.x - pt[0]) ** 2 + (self.y - pt[1]) ** 2 < self.radius ** 2


class BallView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        model = self.model
        pygame.draw.circle(surface, BLUE, (model.x, int(model.y)), model.radius)


class BallEnergyView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        model = self.model
        ke = model.dy ** 2
        pe = (480 - model.y) ** 2
        pygame.draw.line(surface, BLUE, (10, 480), (10, 480 - int(ke * 20)), 20)
        pygame.draw.line(surface, BLUE, (40, 480), (40, 480 - int(pe / 10)), 20)


class BounceController(object):
    def __init__(self, models):
        self.models = models

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for model in self.models:
                if model.contains_pt(pygame.mouse.get_pos()):
                    model.reset()
                    break
        if event.type == pygame.KEYDOWN:
            for model in self.models:
                model.reset()


class Point(object):
        def __init__(self):
            self.radius = 20
            
            self.reset()

        def reset(self):
            self.x = 320
            self.y = 240


class PointView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        model = self.model
        pygame.draw.circle(surface, BLUE, (model.x, int(model.y)), model.radius)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def main():
    pygame.init()
    screen = pygame.display.set_mode((2000, 1075))

    ball = Ball()
    models = [ball]

    views = []
    views.append(BallView(ball))
    views.append(BallEnergyView(ball))
    BackGround = Background('/home/sam/Documents/softDes/InteractiveProgramming/InteractiveProgramming/map.png', [0,0])
    controller = BounceController([ball])

    running = True
    while running:
        for event in pygame.event.get():
            controller.handle_event(event)
            if event.type == pygame.QUIT:
                running = False

        for model in models:
            model.step()

        screen.fill(BLACK)
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
        for view in views:
            view.draw(screen)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
