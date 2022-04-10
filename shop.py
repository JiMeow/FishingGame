from item import Block, Item
from setting import *
from tile_map import Tile
import pygame


class Shop(Tile):
    def __init__(self, id):
        super().__init__(id)
        self.item = Block(0, 0, "block_1")
        self.item.rect.x = fov//2*50-25
        self.item.rect.y = fov//2*50

    def open(self):
        img = pygame.transform.scale(
            pygame.image.load('photo/checkdetailframe.jpg'), (50, 50))
        button = pygame.transform.scale(
            pygame.image.load('photo/coin.png'), (50, 50))
        button.set_colorkey("white")
        gameDisplay.blit(img, (fov//2*50-25, fov//2*50))
        gameDisplay.blit(button, (fov//2*50+75, fov//2*50))
        gameDisplay.blit(
            self.item.img, (self.item.rect.x+10, self.item.rect.y+10))

    def drawItemWhenClickShop(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.item.type != "block":
            gameDisplay.blit(self.item.img, (mouse_x-17.5, mouse_y-17.5))

    def swapItemShopInventory(self, idx, idy, inventory):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x in range(268, 684) and mouse_y in range(563, 763):
            after_x = (mouse_y-563)//50 % 4
            after_y = (mouse_x-268)//46 % 9
            self.item, inventory.itemlist[after_x][after_y] = \
                inventory.itemlist[after_x][after_y], self.item
            self.item.rect, inventory.itemlist[after_x][after_y].rect = \
                inventory.itemlist[after_x][after_y].rect, self.item.rect

    def swapItemInventoryShop(self, idx, idy, inventory):
        before_x, before_y = idx, idy
        if inventory.itemlist[before_x][before_y].type == "block":
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x in range(425, 475) and mouse_y in range(450, 500):
            inventory.itemlist[before_x][before_y], self.item = \
                self.item, inventory.itemlist[before_x][before_y]
            inventory.itemlist[before_x][before_y].rect, self.item.rect = \
                self.item.rect, inventory.itemlist[before_x][before_y].rect

    def sell(self):
        price = 0
        if self.item.type == "fish":
            price = self.item.price
            self.setItemBlock()
        return price

    def setItemBlock(self):
        self.item = Block(0, 0, "block_1")
        self.item.rect.x = fov//2*50-25
        self.item.rect.y = fov//2*50
