"""Animates a bouncing ball.

Author : Oliver Steele <oliver.steele@olin.edu>
Course : Olin Software Design Fall 2016
Date   : 2016-10-24
License: MIT LICENSE
"""
import csv
import pygame
import pandas as pd
import numpy as np
import xlrd
import math

def processing_data():
    my_dic_first_language = pd.read_excel('data2.xlsx', index_col=0, parse_cols = "A:B").to_dict()
    my_dic_second_language = pd.read_excel('data2.xlsx', index_col=0, parse_cols = "A,C").to_dict()
    my_dic_third_language = pd.read_excel('data2.xlsx', index_col=0, parse_cols = "A,D").to_dict()

    a= my_dic_first_language['Dari Persian']
    b = my_dic_second_language['Pashtu']
    c = my_dic_third_language['Turkic']

    country = pd.read_excel(open('country_centroids_all2.xlsx', 'rb'), parse_cols = "A")
    position =  pd.read_excel('country_centroids_all2.xlsx', index_col=0, parse_cols = "A,D").to_dict()
    position2 = pd.read_excel('country_centroids_all2.xlsx', index_col=0, parse_cols = "A,E").to_dict()

    d =  position['LAT']
    h = position2['LONG']

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
    print(final_df.head())
    #print(list(final_df.rows.values))
    lang1 = list(final_df.iloc[0])
    lang2 = list(final_df.iloc[1])
    lang2 = list(final_df.iloc[2])
    lat = list(final_df.iloc[3])
    lon = list(final_df.iloc[4])
    return final_df

processing_data()


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
            self.radius = 5
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
    BackGround = Background('map.png', [0,0])
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
