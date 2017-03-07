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
WHITE = (255,255,255)

"""
with open('country_centroids_primary.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        print(type(row))
        print('\t'.join(row))
"""


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
        #print(model.x)
        pygame.draw.circle(surface, BLUE, ((int(model.x)), int(model.y)), model.radius)


class PointController(object):
    def __init__(self, models):
        self.models = models

    def handle_event(self, event):
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
                    # print('x')
                    # print(x)
                    # print(2000-x)
                    x = 2000-x
                    # print(model[i].x)
                    # print('y')
                    # print(y)
                    # print(model[i].y)
                    if x-350 < model[i].x <x+350:
                        #print('cat')
                        if  y-350 < model[i].y <y+350:
                            print('dog')
                            TextView.display(model[i])
                            #path1

class Rect(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        # self.rect.left, self.rect.top = location

class TextView(object):
    def __init__(self,model):
        self.model = model
        # self.y = 10
        # self.x = 20
        # self.color = fill(WHITE)
    """SAM YOUNG: TODO: So this is called from path1 (search path1) and it is supposed to create a label (honestly anything could work:)
    I got the standard font and created a surface object, but keep getting an error saying the first argyment is not a surface. If you get it working, want to also try
    creating a text box to put the label? But that doesn't matter as much. I dont know if you want to save the code in a different file so we dont get merge conflicts? I have shobot
    from 1:30 -3 but you can probably come hang out with me if you want outside cause no one will probs show up
    PSA: im saying pygame.Surface, but I think Surface has to be a legit suface. I wanted to call in the screen or recreate it within this class, but it was fuckity;
    We might want to go to a ninja!"""
    def display(self):
        pygame.font.init()
        default_font = pygame.font.get_default_font()
        font_renderer = pygame.font.Font(default_font, 12)
        label = font_renderer.render(self.name, 1, (0,0,0))
        # Rect = Rect('text.png', self.x, self.y)
        # pygame.Surface.blit(Rect.image, Rect.rect)
        #Rect=Rect('text.png')
        print(label)
        #TODO: Surface isnt legit?
        pygame.Surface.blit(label,(self.x,self.y))

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
    points = []
    for i in range(len(lon)):
        point = Point(lat[i],lon[i],real_countries[i],lang1[i],lang2[i],lang3[i])
        points.append(point)
    # models = [ball]
    models = points


    views = []

    # views.append(BallView(ball))
    for i in range(len(points)):
        views.append(PointView(points[i]))
    # views.append(BallEnergyView(ball))
    #print(views)
    BackGround = Background('map.png', [0,0])
    # controller = BounceController([ball])
    controller = PointController([points])

    running = True
    while running:
        for event in pygame.event.get():
            controller.handle_event(event)
            if event.type == pygame.QUIT:
                running = False

        # for point in models:
            # model.step()
            #print(type(point))
            # point.reset()

        screen.fill(BLACK)
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)

        for view in views:
            #print('dog')
            #print(view)
            view.draw(screen)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
