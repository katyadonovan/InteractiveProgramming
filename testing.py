import os

import pygame

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"


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

    def reset(self, x=320, y=320):
        self.x = 320
        self.y = 240
        self.dy = 0

    def contains_pt(self, pt):
        return (self.x - pt[0]) ** 2 + (self.y - pt[1]) ** 2 < self.radius ** 2


class infoButton(object):
    def __init__(self):
        self.len = 20
        self.height = 20
        self.x = 20
        self.y = 20

    def reset(self, x, y):
        self.x = x
        self.y = y


class BallView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        pygame.draw.circle(surface, BLUE, (self.model.x, int(self.model.y)), self.model.radius)


class BallKEnergyView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        ke = self.model.dy ** 2
        pygame.draw.line(surface, BLUE, (10, 480), (10, 480 - int(ke * 20)), 20)


class infoButtonView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        pygame.draw.rect(surface, (60, 60, 100), (self.model.x, self.model.y, self.model.len, self.model.height), 0)


class BallPEnergyView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        pe = (480 - self.model.y) ** 2
        pygame.draw.line(surface, BLUE, (40, 480), (40, 480 - int(pe / 10)), 20)


class ButtonController(object):
    def __init__(self, model):
        self.model = model

    def handle_mouse_event(self, event):
        pos = pygame.mouse.get_pos()
        self.model.reset(pos[0], pos[1])


class BallController(object):
    def __init__(self, model):
        self.model = model

    def handle_mouse_event(self, event):
        pos = pygame.mouse.get_pos()
        print(type(pos))
        self.model.reset()


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    ball = Ball()
    ball_controller = BallController(ball)

    info = infoButton()
    views = [
        BallView(ball),
        BallPEnergyView(ball),
        BallKEnergyView(ball), infoButtonView(info)
    ]
    button_controller = ButtonController(info)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                ball_controller.handle_mouse_event(event)
                button_controller.handle_mouse_event(event)
            if event.type == pygame.QUIT:
                running = False

        ball.step()

        screen.fill(BLACK)

        for view in views:
            view.draw(screen)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
