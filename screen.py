import time
import pygame
import random
from setting import *
from player import Player
from tile_map import Tile, cut_picture
from chest import Chest

dic = {50: 'bush',
       161: 'grass',
       55: 'box',
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


class Screen():
    def __init__(self, tilelist) -> None:
        self.animate = 0
        self.tile = tilelist
        for k in range(3):
            for i in range(len(tilelist[k])):
                for j in range(len(tilelist[k][0])):
                    if tilelist[k][i][j] == 55:
                        tile = Chest(tilelist[k][i][j])
                    else:
                        tile = Tile(tilelist[k][i][j])
                    tile.rect.x = i*50
                    tile.rect.y = j*50
                    self.tile[k][i][j] = tile
        item = self.setBlockItem()
        self.player = Player(self.tile, item)

    def draw(self):
        self.player.walk()
        now_x = self.player.rect.x//50
        now_y = self.player.rect.y//50
        for i in range(now_x-fov//2-1, now_x+fov//2+2):
            for j in range(now_y-fov//2-1, now_y+fov//2+2):
                for layer in range(3):
                    if self.tile[layer][i][j].type == -1:
                        continue
                    if self.animate % 60 == 0:
                        if self.tile[layer][i][j].type == 273 or self.tile[layer][i][j].type == 274:
                            if random.randint(0, 100) < 2:
                                newtile = Tile(273)
                                newtile.rect.x = self.tile[layer][i][j].rect.x
                                newtile.rect.y = self.tile[layer][i][j].rect.y
                                self.tile[layer][i][j] = newtile
                            else:
                                newtile = Tile(274)
                                newtile.rect.x = self.tile[layer][i][j].rect.x
                                newtile.rect.y = self.tile[layer][i][j].rect.y
                                self.tile[layer][i][j] = newtile
                        if (self.tile[layer][i][j].type == 161 or self.tile[layer][i][j].type == 68) and layer == 0 and self.tile[layer+1][i][j].type == -1 and self.tile[layer+2][i][j].type == -1:
                            if random.randint(0, 100) < 10:
                                newtile = Tile(68)
                                newtile.rect.x = self.tile[layer][i][j].rect.x
                                newtile.rect.y = self.tile[layer][i][j].rect.y
                                self.tile[layer][i][j] = newtile
                            else:
                                newtile = Tile(161)
                                newtile.rect.x = self.tile[layer][i][j].rect.x
                                newtile.rect.y = self.tile[layer][i][j].rect.y
                                self.tile[layer][i][j] = newtile

                    gameDisplay.blit(self.tile[layer][i][j].img, ((
                        j-(now_y-fov//2))*50-self.player.rect.y % 50, (i-(now_x-fov//2))*50-self.player.rect.x % 50))

        # player back on house
        if self.tile[2][now_x+2][now_y+1].type != -1:
            self.player.draw()
            layer = 2
            while(self.tile[layer][now_x+2][now_y+1].type == -1):
                layer -= 1
            gameDisplay.blit(self.tile[layer][now_x+2][now_y+1].img, ((now_y+2-(now_y+1-fov//2))
                             * 50-self.player.rect.y % 50, (now_x+4-(now_x+2-fov//2))*50-self.player.rect.x % 50))
            layer = 2
            while(self.tile[layer][now_x+2][now_y+2].type == -1):
                layer -= 1
            gameDisplay.blit(self.tile[layer][now_x+2][now_y+2].img, ((now_y+3-(now_y+1-fov//2))
                             * 50-self.player.rect.y % 50, (now_x+4-(now_x+2-fov//2))*50-self.player.rect.x % 50))
            layer = 2
            while(self.tile[layer][now_x+2][now_y].type == -1):
                layer -= 1
            gameDisplay.blit(self.tile[layer][now_x+2][now_y].img, ((now_y+1-(now_y+1-fov//2))
                             * 50-self.player.rect.y % 50, (now_x+4-(now_x+2-fov//2))*50-self.player.rect.x % 50))
        else:
            self.player.draw()
        self.player.drawItem()
        if self.player.is_interact:
            self.player.interact()
        self.player.drawItemClickAndOnHand()
        if self.player.checkDetail:
            self.player.checkItemDetail()
        if self.player.is_useItem:
            self.player.drawUseItem()
        self.player.drawMoney()
        self.animate += 1

    def setBlockItem(self):
        item = [["block_1" for i in range(9)] for j in range(4)]
        return item
