import pygame
import random
import math
from setting import *

dic = {50: 'bush',
       161: 'grass',
       68: 'flower',
       101: 'path',
       102: 'path',
       103: 'path',
       115: 'stone',
       117: 'path',
       118: 'path',
       119: 'path',
       131: 'stone',
       133: 'path',
       134: 'path',
       135: 'path',
       193: 'patharoundwater',
       224: 'patharoundwater',
       225: 'patharoundwater',
       240: 'patharoundwater',
       242: 'patharoundwater',
       256: 'patharoundwater',
       257: 'patharoundwater',
       258: 'patharoundwater',
       261: 'bridge',
       274: 'water',
       273: 'wateroptional',
       290: 'lillypad',
       272: 'stoneunderwater',
       288: 'stoneunderwater'}


class Item(pygame.sprite.Sprite):
    def __init__(self, i, j, item):
        super().__init__()
        self.type = item.split("_")[0]
        self.id = item
        try:
            self.img = pygame.transform.scale(
                pygame.image.load(f'item/block/dummy (1).png'), (35, 35))
        except:
            self.img = pygame.transform.scale(
                pygame.image.load(f'item/block/dummy (1).jpg'), (35, 35))
        self.rect = self.img.get_rect()
        self.rect.x = j*46.5 + fov*50-675
        self.rect.y = i*48 + fov*50-375
        if i == 3:
            self.rect.y += 12


class UsableItem(Item):
    def __init__(self, i, j, item):
        super().__init__(i, j, item)
        self.durable = 100

    def repair(self):
        self.durable = 100

    def useDecreaseDurable(self):
        self.durable = self.durable - 1
        if self.durable == 0:
            self.broken()

    def broken(self):
        pass


class Block(Item):
    def __init__(self, i, j, item):
        super().__init__(i, j, item)
        try:
            self.img = pygame.transform.scale(pygame.image.load(
                f'item/block/dummy ({item.split("_")[-1]}).png'), (30, 30))
        except:
            self.img = pygame.transform.scale(pygame.image.load(
                f'item/block/dummy ({item.split("_")[-1]}).jpg'), (30, 30))
        self.img.set_colorkey("#FFFFFF")


class Fish(Item):
    namelist = [
        'Junonia',
        'Sand Dollar',
        'Starfish',
        'Atlantic Bass',
        'Clownfish',
        'Dab',
        'Sea Spider',
        'Blue Gill',
        'Guppy',
        'Fresh Snail',
        'Axolotl',
        'Banded Shark',
        'Golden Tench',
        'Moss Ball',
        'Plastic Bag',
    ]

    def __init__(self, i, j, item):
        super().__init__(i, j, item)
        self.name = self.namelist[int(item.split("_")[-1])-1]
        self.weight = round((random.random()+0.1)*100//10 + random.random(), 1)
        self.grade = round(5-round(math.log(random.randint(1, 81), 3), 0))
        if self.grade == 1:
            self.price = int(round(self.weight*1, 0))
        if self.grade == 2:
            self.price = int(round(self.weight*2, 0))
        if self.grade == 3:
            self.price = int(round(self.weight*5, 0))
        if self.grade == 4:
            self.price = int(round(self.weight*10, 0))
        if self.grade == 5:
            self.price = int(round(self.weight*50, 0))
        try:
            self.img = pygame.transform.scale(pygame.image.load(
                f'item/fish/dummy ({item.split("_")[-1]}).png'), (30, 30))
        except:
            self.img = pygame.transform.scale(pygame.image.load(
                f'item/fish/dummy ({item.split("_")[-1]}).jpg'), (30, 30))
        self.img.set_colorkey("black")


class Fishingrod(UsableItem):
    def __init__(self, i, j, item):
        super().__init__(i, j, item)
        try:
            self.img = pygame.transform.scale(pygame.image.load(
                f'item/fishingrod/dummy ({item.split("_")[-1]}).png'), (35, 35))
        except:
            self.img = pygame.transform.scale(pygame.image.load(
                f'item/fishingrod/dummy ({item.split("_")[-1]}).jpg'), (35, 35))
        self.img.set_colorkey("white")

    def use(self, tilearound, fishforfight, rodforfight, fishforfight_x, fishforfight_y, rodforfight_x, rodforfight_y, fishspeed, rodspeed, success, is_fishing):
        tilelist = [dic[i] if i in dic else "NULL" for i in tilearound]
        fail = 0
        if "patharoundwater" in tilelist or "stoneunderwater" in tilelist or 'water' in tilelist or \
                'wateroptional' in tilelist or 'lillypad' in tilelist:
            fishforfight_x += fishspeed
            fishforfight_x = max(50*fov//2-100, fishforfight_x)
            fishforfight_x = min(50*fov//2+150, fishforfight_x)

            rodforfight_x += rodspeed
            rodforfight_x = max(50*fov//2-100, rodforfight_x)
            rodforfight_x = min(50*fov//2+150, rodforfight_x)

            bluebar = pygame.transform.scale(
                pygame.image.load(f'photo/bluebar.png'), (300, 40))
            gameDisplay.blit(bluebar, (50*fov//2-100, 50*fov//2+75))
            fish = gameDisplay.blit(
                fishforfight, (fishforfight_x, fishforfight_y))
            rod = gameDisplay.blit(
                rodforfight,  (rodforfight_x, rodforfight_y))
            if fish.colliderect(rod):
                success += 1
                success = min(success, 600)
            else:
                success -= 1
                success = max(success, 0)
            if success == 0:
                is_fishing = False
                fail = 1
            if success == 600:
                is_fishing = False
            if is_fishing:
                font = pygame.font.Font('font/freesansbold.ttf', 20)
                text = font.render(
                    f'{success//6}%', True, "black", "grey")
                text.set_colorkey("grey")
                gameDisplay.blit(text,  (50*fov//2+210, 50*fov//2+80))

        return fishforfight_x, fishforfight_y, rodforfight_x, rodforfight_y, success, is_fishing, fail
