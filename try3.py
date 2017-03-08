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

a= my_dic_first_language['Dari Persian']
b = my_dic_second_language['Pashtu']
c = my_dic_third_language['Turkic']

country = pd.read_excel(open('country_centroids_all2.xlsx', 'rb'), parse_cols = "A")
position =  pd.read_excel('country_centroids_all2.xlsx', index_col=0, parse_cols = "A,G").to_dict()
position2 = pd.read_excel('country_centroids_all2.xlsx', index_col=0, parse_cols = "A,F").to_dict()

d =  position['LAT2']
h = position2['LONG2']

ps = pd.read_excel('data2.xlsx')
f=ps.iloc[:,0].tolist()
cd = pd.read_excel('country_centroids_all2.xlsx')
e=cd.iloc[:,0].tolist()

real_countries = []
for i in cd.iloc[:,0].tolist():
    if i in ps.iloc[:,0].tolist():
        real_countries.append(i)
for i in ps.iloc[:,0].tolist():
    if i in cd.iloc[:,0].tolist():
        real_countries.append(i)

new_first = {}
new_second = {}
new_third = {}
new_pos = {}
new_pos2 = {}

def common_dicts(dict1,dict2,lst):
    for k,v in dict1.items():
        for i in lst:
            if i == k:
                dict2[k]=v
    return dict2

new1= common_dicts(a,new_first,real_countries)
new2 = common_dicts(b,new_second,real_countries)
new3 = common_dicts(c,new_third,real_countries)
new4 = common_dicts(d,new_pos,real_countries)
new5 = common_dicts(h,new_pos2,real_countries)
dicts = [new1,new2,new3,new4,new5]

final_df =pd.DataFrame(dicts)
#print(final_df.head())
#print(list(final_df.rows.values))
lang1 = list(final_df.iloc[0])
lang2 = list(final_df.iloc[1])
lang3 = list(final_df.iloc[2])
lat = list(final_df.iloc[3])
lon = list(final_df.iloc[4])
#print(lon)
#print(real_countries)
    #return final_df

#processing_data()


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

"""
with open('country_centroids_primary.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        print(type(row))
        print('\t'.join(row))
"""


class Point(object):
        def __init__(self,lat,lon,name,lang1,lang2,lang3):
            self.radius = 10
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
        #print(model.x)
        pygame.draw.circle(surface, BLUE, ((int(model.x)), int(model.y)), model.radius)


class PointController(object):
    def __init__(self, models):
        self.models = models

    def handle_event(self, event, screen):
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     for model in self.models:
        #         if model.contains_pt(pygame.mouse.get_pos()):
        #             model.reset()
        #             break
        if event.type == pygame.KEYDOWN:
            for model in self.models:
                model.reset()
        if event.type == pygame.MOUSEBUTTONDOWN:
            (x,y) = pygame.mouse.get_pos()
            for model in self.models:
                for i in range(len(self.models)):
                    print('x')
                    print(x)
                    #print(2000-x)
                    x = 2000-x
                    print(model[i].x)
                    print('y')
                    print(y)
                    print(model[i].y)
                    if x-350 < model[i].x <x+350:
                        #print('cat')
                        if  y-350 < model[i].y <y+350:
                            print('dog')
                            TextView(model[i]).display(screen)
            #path1


class texts(object):
    def __init__(self):
        text = "Hello"

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0, 0, 0))
        return textSurface, textSurface.get_rect()

    def reset(self, text, screen):
        text1 = pygame.font.Font("freesansbold.ttf", 16)
        TextSurf, TextRect = self.text_objects(text, text1)
        TextRect.center = (200, 200)
        screen.blit(TextSurf, TextRect)


class infoButton(object):
    def __init__(self):
        self.len = 20
        self.height = 20
        self.x = 20
        self.y = 20
        self.infotxt = "No Country Selected"
        # self.txt = texts()

        # resets based on mouse position.
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.infotext = "No Country Selected"


class infoButtonView(object):
    def __init__(self, model):
        self.model = models

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 200), (self.model.x, self.model.y, self.model.len, self.model.height), 0)


class ButtonController(object):
    def __init__(self, model):
        self.model = model

    def handle_mouse_event(self, event, screen):
        pos = pygame.mouse.get_pos()
        self.model.reset(pos[0], pos[1])
        # self.model.txt.rest(x, y, self.model.infotxt, screen)


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
    """SAM YOUNG: TODO: So this is called from path1 (search path1) and it is supposed to create a label (honestly anything could work:)
    I got the standard font and created a surface object, but keep getting an error saying the first argyment is not a surface. If you get it working, want to also try
    creating a text box to put the label? But that doesn't matter as much. I dont know if you want to save the code in a different file so we dont get merge conflicts? I have shobot
    from 1:30 -3 but you can probably come hang out with me if you want outside cause no one will probs show up
    PSA: im saying pygame.Surface, but I think Surface has to be a legit suface. I wanted to call in the screen or recreate it within this class, but it was fuckity;
    We might want to go to a ninja!"""

    def display(self,screen):

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
        # pygame.Surface.blit(label,(self.x,self.y))

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
    points = []
    for i in range(len(lon)):
        point = Point(lat[i],lon[i],real_countries[i],lang1[i],lang2[i],lang3[i])
        points.append(point)
    models = points
    views = []
    for i in range(len(points)):
        views.append(PointView(points[i]))

    models.append(button)
    views.append(infoButtonView(button))
    BackGround = Background('world-map.jpg', [0,0])
    controller = PointController([points])
    button_controller = ButtonController(button)
    text1 = texts()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                controller.handle_event(event, screen)
                button_controller.handle_mouse_event(event, screen)
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
        for view in views:

            view.draw(screen)
        text1.reset("hi", screen)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
