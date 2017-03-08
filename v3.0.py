import csv
import pygame
import pandas as pd
import numpy as np
import xlrd
import math

#def processing_data():

my_dic_first_language = pd.read_excel('data2.xlsx', index_col=0, parse_cols = "A:B").to_dict()
my_dic_second_language = pd.read_excel('data2.xlsx', index_col=0, parse_cols = "A,C").to_dict()
my_dic_third_language = pd.read_excel('data2.xlsx', index_col=0, parse_cols = "A,D").to_dict()

a = my_dic_first_language['Dari Persian']
b = my_dic_second_language['Pashtu']
c = my_dic_third_language['Turkic']

country = pd.read_excel(open('pleasework.xlsx', 'rb'), parse_cols = "A")
position = pd.read_excel('pleasework.xlsx', index_col=0, parse_cols = "A,D").to_dict()
position2 = pd.read_excel('pleasework.xlsx', index_col=0, parse_cols = "A,E").to_dict()

d = position['LAT2']
h = position2['LONG2']

ps = pd.read_excel('data2.xlsx')
f = ps.iloc[:, 0].tolist()
cd = pd.read_excel('pleasework.xlsx')
e = cd.iloc[:, 0].tolist()

real_countries = []
for i in cd.iloc[:, 0].tolist():
    if i in ps.iloc[:, 0].tolist():
        real_countries.append(i)
for i in ps.iloc[:, 0].tolist():
    if i in cd.iloc[:, 0].tolist():
        real_countries.append(i)

new_first = {}
new_second = {}
new_third = {}
new_pos = {}
new_pos2 = {}


def common_dicts(dict1, dict2, lst):
    for k, v in dict1.items():
        for i in lst:
            if i == k:
                dict2[k] = v
    return dict2

new1= common_dicts(a,new_first,real_countries)
new2 = common_dicts(b,new_second,real_countries)
new3 = common_dicts(c,new_third,real_countries)
new4 = common_dicts(d,new_pos,real_countries)
new5 = common_dicts(h,new_pos2,real_countries)
dicts = [new1,new2,new3,new4,new5]

final_df =pd.DataFrame(dicts)
final_df.fillna(value='None',inplace = True)
lang1 = list(final_df.iloc[0])
lang2 = list(final_df.iloc[1])
lang3 = list(final_df.iloc[2])
lat = list(final_df.iloc[3])
lon = list(final_df.iloc[4])


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (204, 255, 255)
ORANGE = (244, 99, 99)


class Point(object):
        def __init__(self,lat,lon,name,lang1,lang2,lang3):
            self.radius = 5
            self.language = 1
            self.name = name
            self.x = lat
            self.y = lon
            self.lang1 = lang1
            self.lang2 = lang2
            self.lang3 = lang3

        def reset(self):
            self.x = lat
            self.y = lon


class PointView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        model = self.model
        pygame.draw.circle(surface, YELLOW, ((int(model.x)), int(model.y)), model.radius)


class texts(object):
    def __init__(self):
        self.name = ""
        self.x = -1000
        self.y = -1000
        text1 = pygame.font.Font("freesansbold.ttf", 60)
        self.TextSurf, self.TextRect = self.text_objects(self.name, text1)

    def text_objects(self, text, font):
        # print(text)
        textSurface = font.render(text, True, (255, 255, 255))
        return textSurface, textSurface.get_rect()

    def reset(self, text, x, y, screen):
        self.x = x
        self.y = y + 5
        text1 = pygame.font.Font("freesansbold.ttf", 24)
        self.TextSurf, self.TextRect = self.text_objects(text, text1)
        self.TextRect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.TextSurf, self.TextRect)


class infoTextView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        self.model.draw(surface)


class infoButton(object):
    def __init__(self):
        self.len = 60
        self.height = 30
        self.x = -20
        self.y = -20
        self.name = "No Country Selected"

        # resets based on mouse position.
    def reset(self, txt, x, y, screen):
        self.x = x
        self.y = y
        self.name = "No Country Selected"
        print(self.name)


class infoButtonView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), (self.model.x, self.model.y, self.model.len, self.model.height), 0)

class ButtonController(object):
    def __init__(self, model):
        self.model = model

    def handle_mouse_event(self, event, screen,models):
        if event.type == pygame.MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            print(models)
            for i in range(len(models)):
                if x-5 < models[i].x < x+5:
                    print('cat')
                    if y-5 < models[i].y < y+5:
                        print('dog')
                        pos = pygame.mouse.get_pos()
                        self.model.reset(models[i].name, pos[0], pos[1], screen)


class LangController(object):
    def __init__(self, model):
        self.model = model

    def handle_mouse_event(self, event, screen, models, lan):
        if event.type == pygame.MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            print(models)
            for i in range(len(models)):
                if x-5 < models[i].x < x+5:
                    print('cat')
                    if y-5 < models[i].y < y+5:
                        print('dog')
                        pos = pygame.mouse.get_pos()
                        if lan == 3:
                            self.model.reset(models[i].lang3, pos[0], pos[1] + 15, screen)
                        elif lan == 2:
                            print(lan)
                            self.model.reset(models[i].lang2, pos[0], pos[1] + 15, screen)
                        else:
                            print(lan)
                            self.model.reset(models[i].lang1, pos[0], pos[1] + 15, screen)



class Rect(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        # self.rect.left, self.rect.top = location

class TextView(object):
    def __init__(self,point):
        self.point = point
        # self.y = 10
        # self.x = 20
        # self.color = fill(WHITE)
"""
    def display(self,screen):
        # pygame.font.init()
        # default_font = pygame.font.get_default_font()
        # font_renderer = pygame.font.Font(default_font, 12)
        # label = font_renderer.render(self.name, 1, (0,0,0))
        # Rect = Rect('text.png', self.x, self.y)
        # pygame.Surface.blit(Rect.image, Rect.rect)
        #Rect=Rect('text.png')
        #print(label)
        #TODO: Surface isnt legit?
        print('cat')
        #screen = pygame.display.set_mode((2000, 1075))
        print('a')
        rect_surface = pygame.Surface((100, 100)) # create rectangular surface 100x500
        print(type(rect_surface))
        screen.blit(rect_surface, (self.point.x, self.point.y)) # draw rectangular surface on your screen
        #pygame.display.update()
        rect_surface.fill(BLUE) # fill surface with color (different that screen color)
        font = pygame.font.SysFont("monospace", 15) # set up font style
        label = font.render(self.point.name, 1, WHITE) # render font with color (different than rect_surface)
        rect_surface.blit(label, (5, 5)) # draw font object on rect_surface (should look like text box on screren)
        pygame.display.update()
"""

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def main():
    pygame.init()
    screen = pygame.display.set_mode((1470, 735))
    button = infoButton()
    infot = texts()
    lang = texts()
    points = []
    for i in range(len(lon)):
        point = Point(lat[i],lon[i],real_countries[i],lang1[i],lang2[i],lang3[i])
        points.append(point)
    models = points
    views = []
    for i in range(len(points)):
        views.append(PointView(points[i]))

    views.append(infoButtonView(button))
    views.append(infoTextView(infot))
    views.append(infoTextView(lang))
    BackGround = Background('world-map.jpg', [0,0])
    button_controller = ButtonController(button)
    button_controller2 = ButtonController(infot)
    lang_controller = LangController(lang)
    text1 = texts()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    lan = 1
                elif event.key == pygame.K_2:
                    lan = 2
                elif event.key == pygame.K_3:
                    lan = 3
                else:
                    lan = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_controller.handle_mouse_event(event, screen, models)
                button_controller2.handle_mouse_event(event, screen, models)
                lang_controller.handle_mouse_event(event, screen, models, lan)

            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
        views.append(text1)
        text1.reset("Languages of the World",1470/2 - 300, 20, screen)
        for view in views:
            view.draw(screen)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
