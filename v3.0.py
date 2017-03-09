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

country = pd.read_excel(open('bleh.xlsx', 'rb'), parse_cols = "A")
position = pd.read_excel('bleh.xlsx', index_col=0, parse_cols = "A,D").to_dict()
position2 = pd.read_excel('bleh.xlsx', index_col=0, parse_cols = "A,E").to_dict()

d = position['LAT2']
h = position2['LONG2']

ps = pd.read_excel('data2.xlsx')
f = ps.iloc[:, 0].tolist()
cd = pd.read_excel('bleh.xlsx')
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
LANG1 = (25,105,152)
LANG2 = (117,26,162)
LANG3 = (26,162,94)
TITLE = (0,0,0)
COUNTRY = (255,255,255)

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
        pygame.draw.circle(surface, LIGHTBLUE, ((int(model.x)), int(model.y)), model.radius)


class texts(object):
    def __init__(self):
        self.name = ""
        self.x = -1000
        self.y = -1000
        self.color = BLACK
        text1 = pygame.font.Font("freesansbold.ttf", 60)
        self.TextSurf, self.TextRect = self.text_objects(self.name, text1, self.color)

    def text_objects(self, text, font,color):
        textSurface = font.render(text, True,color)
        return textSurface, textSurface.get_rect()

    def reset(self, text, x, y, screen,size,color):
        self.x = x + 5
        self.y = y + 5
        text1 = pygame.font.Font("freesansbold.ttf", size)
        self.TextSurf, self.TextRect = self.text_objects(text, text1, color)
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
        self.len = 140
        self.height = 60
        self.x = -200
        self.y = -200
        self.name = "No Country Selected"

        # resets based on mouse position.
    def reset(self, txt, x, y, screen,size,color):
        self.x = x
        self.y = y
        self.name = "No Country Selected"


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
            for i in range(len(models)):
                if x-5 < models[i].x < x+5:
                    if y-5 < models[i].y < y+5:
                        pos = pygame.mouse.get_pos()
                        self.model.reset(models[i].name, pos[0], pos[1], screen, 20, COUNTRY)


class LangController(object):
    def __init__(self, model):
        self.model = model

    def handle_mouse_event(self, event, screen, models, lan):
        if event.type == pygame.MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            for i in range(len(models)):
                if x-5 < models[i].x < x+5:
                    if y-5 < models[i].y < y+5:
                        pos = pygame.mouse.get_pos()
                        if lan == 3:
                            self.model.reset(models[i].lang3, pos[0], pos[1] + 25, screen,20,LANG3)
                        elif lan == 2:
                            self.model.reset(models[i].lang2, pos[0], pos[1] + 25, screen,20,LANG2)
                        else:
                            self.model.reset(models[i].lang1, pos[0], pos[1] + 25, screen,20,LANG1)



class Rect(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()

class TextView(object):
    def __init__(self,point):
        self.point = point

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
    button1 = infoButton()
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
    text2 = texts()
    text3 = texts()
    text4 = texts()
    views.append(text1)
    views.append(text2)
    views.append(text3)
    views.append(infoButtonView(button1))
    views.append(text4)
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
        text1.reset("Languages of the World",1470/2 - 220, 20, screen, 40, BLACK)
        text2.reset("Most Spoken Language: Blue", 40, 735-130, screen, 20, LANG1)
        text3.reset("Second Most Spoken Language: Purple", 40, 735- 100,  screen, 20, LANG2)
        text4.reset("Third Most Spoken Language: Green", 40, 735- 70, screen, 20, LANG3)

        for view in views:
            view.draw(screen)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
