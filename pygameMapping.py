"""Animates a bouncing ball.

Author : Oliver Steele <oliver.steele@olin.edu>
Course : Olin Software Design Fall 2016
Date   : 2016-10-24
License: MIT LICENSE
"""
import csv
import pygame

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

"""
with open('country_centroids_primary.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        print(type(row))
        print('\t'.join(row))
"""


class Point(object):
        def __init__(self):
            self.radius = 10
            self.language = 1
            self.name = 1
            self.x = 320
            self.y = 240

        def reset(self):
            self.x = 320
            self.y = 240


class PointView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        model = self.model
        pygame.draw.circle(surface, BLUE, ((int(model.x)), int(model.y)), model.radius)


class PointController(object):
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

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def main():
    pygame.init()
    screen = pygame.display.set_mode((2000, 1075))

    # ball = Ball()
    point = Point()
    # models = [ball]
    models = [point]

    views = []
    # views.append(BallView(ball))
    views.append(PointView(point))
    # views.append(BallEnergyView(ball))
    BackGround = Background('/home/sam/Documents/softDes/InteractiveProgramming/InteractiveProgramming/map.png', [0,0])
    # controller = BounceController([ball])
    controller = PointController([point])

    running = True
    while running:
        for event in pygame.event.get():
            controller.handle_event(event)
            if event.type == pygame.QUIT:
                running = False

        for model in models:
            # model.step()
            model.reset()

        screen.fill(BLACK)
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
        for view in views:
            view.draw(screen)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
