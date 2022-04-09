from sre_constants import SUCCESS
import pygame
import random

from pytest import fail
from item import Fish, Fishingrod, UsableItem
from setting import *
from inventory import Inventory


class Player(pygame.sprite.Sprite):
    def __init__(self, tile, itemlist):
        super().__init__()
        self.tile = tile
        self.animate = 0
        # player
        self.player = pygame.transform.scale(
            pygame.image.load('photo/player.png'), (100, 100))
        self.playerright = pygame.transform.scale(
            pygame.image.load('photo/playerright.png'), (100, 100))
        self.playerleft = pygame.transform.scale(
            pygame.image.load('photo/playerleft.png'), (100, 100))
        self.playerupleft = pygame.transform.scale(
            pygame.image.load('photo/playerupleft.png'), (100, 100))
        self.playerupright = pygame.transform.scale(
            pygame.image.load('photo/playerupright.png'), (100, 100))
        self.rect = self.playerright.get_rect()
        self.rect.x = display_width//2-500
        self.rect.y = display_height//2-500
        self.hitbox = pygame.Rect(self.rect.x+60, self.rect.y+50, 1, 1)
        self.walk_x = 0
        self.walk_y = 0
        # item
        self.is_openinventory = False
        self.is_drawItemInventory = False
        self.is_drawItemSlot = False
        self.is_useItem = False
        self.star = pygame.transform.scale(
            pygame.image.load('photo/star.png'), (15, 15))
        self.star.set_colorkey("#FFFFFF")
        self.itemlist = itemlist
        self.setItemInventory()
        self.inventory = Inventory(itemlist)
        self.itemslot = itemlist[-1:]
        self.selectSlot = 0
        self.selectInventory = [3, 0]
        self.checkDetail = False
        # activity
        self.activity = False
        # fishing
        self.fishingrodforfight = pygame.transform.scale(
            pygame.image.load(f'item/fishingrod/dummy (1).jpg'), (40, 40))
        self.fishingrodforfight.set_colorkey("white")
        self.fishforfight = pygame.transform.scale(
            pygame.image.load(f'photo/fishforfight.jpg'), (40, 40))
        self.fishforfight.set_colorkey("white")
        self.is_fishing = False
        self.rodforfight_rect = self.fishingrodforfight.get_rect()
        self.rodforfight_rect.x, self.rodforfight_rect.y = 50*fov//2+20, 50*fov//2+75
        self.fishforfight_rect = self.fishforfight.get_rect()
        self.fishforfight_rect.x, self.fishforfight_rect.y = 50*fov//2+20, 50*fov//2+75
        self.fishdirect = random.randint(0, 1)*2-1
        self.fishspeed = random.randint(0, 6)*self.fishdirect
        self.rodspeed = -1
        self.success = 120
        # money
        self.money = 0

    def walkable(self, x, y):
        if self.tile[2][x][y].type == -1:
            return True
        return False

    def playerCollision(self):
        ans = 0
        for layer in range(3):
            for i in range(len(self.tile[layer])):
                for j in range(len(self.tile[layer][0])):
                    if self.tile[layer][i][j].rect.colliderect(self.hitbox):
                        if self.walkable(i, j):
                            return False
        return True

    def walk(self):
        before_x = self.rect.x
        before_y = self.rect.y
        if self.walk_x != 0 and self.walk_y != 0:
            self.walk_x = walk_speed/1.414 if self.walk_x > 0 else -walk_speed/1.414
            self.walk_y = walk_speed/1.414 if self.walk_y > 0 else -walk_speed/1.414
        self.rect.x += self.walk_x
        self.rect.y += self.walk_y
        self.hitbox = pygame.Rect(self.rect.x+60, self.rect.y+50, 1, 1)
        if self.playerCollision():
            self.rect.x = before_x
            self.rect.y = before_y
            self.hitbox = pygame.Rect(self.rect.x+60, self.rect.y+50, 1, 1)

    def draw(self):
        if self.walk_x == 0 and self.walk_y == 0:
            gameDisplay.blit(self.player, (fov//2*50, fov//2*50))
        elif self.walk_y == 0:
            if self.walk_x >= 0:
                gameDisplay.blit(self.playerupright, (fov//2*50, fov//2*50))
            elif self.walk_x < 0:
                gameDisplay.blit(self.player, (fov//2*50, fov//2*50))
        elif self.walk_x < 0:
            if self.walk_y > 0:
                gameDisplay.blit(self.playerright, (fov//2*50, fov//2*50))
            elif self.walk_y < 0:
                gameDisplay.blit(self.playerleft, (fov//2*50, fov//2*50))
        else:
            if self.walk_y > 0:
                gameDisplay.blit(self.playerright, (fov//2*50, fov//2*50))
            elif self.walk_y < 0:
                gameDisplay.blit(self.playerleft, (fov//2*50, fov//2*50))
            else:
                gameDisplay.blit(self.player, (fov//2*50, fov//2*50))
        self.animate += 1

    def openItemslot(self):
        self.itemslot_img = pygame.transform.scale(
            pygame.image.load('photo/itemslot.jpg'), (420, 60))
        gameDisplay.blit(self.itemslot_img, ((fov*50-420)//2, fov*50-100))
        for i in range(len(self.itemslot)):
            for j in range(len(self.itemslot[0])):
                if self.itemslot[0][j].id.split('_')[0] != "block":
                    if j == self.selectSlot:
                        gameDisplay.blit(
                            self.star, ((fov*50-420)//2+13+43.5*self.selectSlot, fov*50-97))
                    gameDisplay.blit(self.inventory.itemlist[3][j].img, ((
                        fov*50-410)//2+16+43.5*j, fov*50-89))
                else:
                    if j == self.selectSlot:
                        gameDisplay.blit(
                            self.star, ((fov*50-420)//2+13+43.5*self.selectSlot, fov*50-97))

    def openInventory(self):
        self.inventory_img = pygame.transform.scale(
            pygame.image.load('photo/inventory.png'), (420, 210))
        gameDisplay.blit(self.inventory_img, ((fov*50-420)//2, fov*50-385))
        for i in range(len(self.inventory.itemlist)):
            for j in range(len(self.inventory.itemlist[0])):
                if self.inventory.itemlist[i][j].id.split('_')[0] != "block":
                    if i == self.selectInventory[0] and j == self.selectInventory[1]:
                        gameDisplay.blit(
                            self.star,  (self.inventory.itemlist[i][j].rect.x-7, self.inventory.itemlist[i][j].rect.y-7))
                    gameDisplay.blit(self.inventory.itemlist[i][j].img, (
                        self.inventory.itemlist[i][j].rect.x, self.inventory.itemlist[i][j].rect.y))
                else:
                    gameDisplay.blit(self.inventory.itemlist[i][j].img, (
                        self.inventory.itemlist[i][j].rect.x, self.inventory.itemlist[i][j].rect.y))
                    if i == self.selectInventory[0] and j == self.selectInventory[1]:
                        gameDisplay.blit(
                            self.star,  (self.inventory.itemlist[i][j].rect.x-7, self.inventory.itemlist[i][j].rect.y-7))

    def drawItemInventory(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.inventory.itemlist[self.selectInventory[0]][self.selectInventory[1]].id.split('_')[0] != "block":
            gameDisplay.blit(self.inventory.itemlist[self.selectInventory[0]]
                             [self.selectInventory[1]].img, (mouse_x-17.5, mouse_y-17.5))

    def drawItemSlot(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.inventory.itemlist[3][self.selectSlot].id.split('_')[0] != "block":
            gameDisplay.blit(
                self.inventory.itemlist[3][self.selectSlot].img, (mouse_x-17.5, mouse_y-17.5))

    def swapItemInventory(self):
        before_x, before_y = self.selectInventory[0], self.selectInventory[1]
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x in range(268, 684) and mouse_y in range(563, 763):
            after_x = (mouse_y-563)//50 % 4
            after_y = (mouse_x-268)//46 % 9
            self.inventory.itemlist[before_x][before_y], self.inventory.itemlist[after_x][
                after_y] = self.inventory.itemlist[after_x][after_y], self.inventory.itemlist[before_x][before_y]
            self.inventory.itemlist[before_x][before_y].rect, self.inventory.itemlist[after_x][
                after_y].rect = self.inventory.itemlist[after_x][after_y].rect, self.inventory.itemlist[before_x][before_y].rect
            self.selectInventory = [after_x, after_y]
            if self.selectInventory[0] == 3:
                self.selectSlot = after_y
        else:
            return

    def swapItemSlot(self):
        before = self.selectSlot
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y in range(860, 895) and mouse_x in range(282, 675):
            after = (mouse_x-282)//44 % 9
            self.inventory.itemlist[3][before].type, self.inventory.itemlist[3][
                after].type = self.inventory.itemlist[3][after].type, self.inventory.itemlist[3][before].type
            self.inventory.itemlist[3][before].img, self.inventory.itemlist[3][
                after].img = self.inventory.itemlist[3][after].img, self.inventory.itemlist[3][before].img
            self.selectSlot = after
            if self.selectInventory[0] == 3:
                self.selectInventory = [3, after]
        else:
            return

    def drawItemOnHand(self):
        if self.walk_x == 0 and self.walk_y == 0 or self.walk_x < 0 and self.walk_y == 0:
            if self.inventory.itemlist[3][self.selectSlot].id.split('_')[0] != "block":
                img = pygame.transform.scale(
                    self.inventory.itemlist[3][self.selectSlot].img, (50, 50))
                if self.inventory.itemlist[3][self.selectSlot].id.split('_')[0] == "fishingrod":
                    img = pygame.transform.scale(
                        self.inventory.itemlist[3][self.selectSlot].img, (60, 60))
                if self.inventory.itemlist[3][self.selectSlot].id.split('_')[0] == "fish":
                    img = pygame.transform.scale(
                        self.inventory.itemlist[3][self.selectSlot].img, (40, 40))
                img.set_colorkey("white")
                if self.inventory.itemlist[3][self.selectSlot].id[:5] == "fish_":
                    img.set_colorkey("black")
                gameDisplay.blit(img, (fov//2*50+60, fov//2*50+27))

    def setItemInventory(self):
        self.itemlist[3][0] = "fish_1"
        self.itemlist[3][1] = "fish_2"
        self.itemlist[3][2] = "fishingrod_1"
        for i in range(3):
            for j in range(9):
                if i*9+j < 15:
                    self.itemlist[i][j] = f"fish_{i*9+j+1}"

    def drawItem(self):
        if self.is_openinventory:
            # draw inventory
            self.openInventory()
            if self.is_drawItemInventory:
                # draw item in inventory on mouse
                self.drawItemInventory()
        else:
            # draw item slot
            self.openItemslot()
            if self.is_drawItemSlot:
                # draw item in slot on mouse
                self.drawItemSlot()
        self.drawItemOnHand()

    def checkItemDetail(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        select_x = 0
        select_y = 0
        if mouse_y in range(860, 895) and mouse_x in range(282, 675):
            select_x = 3
            select_y = (mouse_x-282)//44 % 9
        elif self.is_openinventory:
            if mouse_x in range(268, 684) and mouse_y in range(563, 763):
                select_x = (mouse_y-563)//50 % 4
                select_y = (mouse_x-268)//46 % 9
            else:
                return
        else:
            return
        type = self.inventory.itemlist[select_x][select_y].id.split('_')[0]
        if type == "fish":
            font = pygame.font.Font('font/freesansbold.ttf', 15)
            item = self.inventory.itemlist[select_x][select_y]
            name = font.render(f' {item.name}', True, "black", "grey")
            weight = font.render(f': {item.weight}', True, "black", "grey")
            price = font.render(f': {item.price}', True, "black", "grey")
            grade = font.render(f': {item.grade}', True, "black", "grey")
            weight.set_colorkey("grey")
            price.set_colorkey("grey")
            grade.set_colorkey("grey")
            name.set_colorkey("grey")
            frame = pygame.transform.scale(pygame.image.load(
                f'photo/checkdetailframe.jpg'), (140, 140))
            # frame.set_colorkey("white")
            coin = pygame.transform.scale(
                pygame.image.load(f'photo/coin.png'), (20, 20))
            coin.set_colorkey("white")
            anvil = pygame.transform.scale(
                pygame.image.load(f'photo/anvil.png'), (20, 20))
            anvil.set_colorkey("white")
            star = pygame.transform.scale(
                pygame.image.load(f'photo/star.png'), (25, 25))
            star.set_colorkey("white")
            gameDisplay.blit(frame, (mouse_x, mouse_y))
            gameDisplay.blit(name, (mouse_x+15, mouse_y+18))
            gameDisplay.blit(anvil, (mouse_x+18, mouse_y+48))
            gameDisplay.blit(weight, (mouse_x+42, mouse_y+50))
            gameDisplay.blit(coin, (mouse_x+17, mouse_y+74))
            gameDisplay.blit(price, (mouse_x+42, mouse_y+75))
            gameDisplay.blit(star, (mouse_x+15, mouse_y+95))
            gameDisplay.blit(grade, (mouse_x+42, mouse_y+100))

    def useItem(self):
        item = self.inventory.itemlist[3][self.selectSlot]
        pos_x = self.hitbox.x//50
        pos_y = self.hitbox.y//50
        tilearound = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0):
                    tilearound += [self.tile[2][pos_x+i][pos_y+j].type]
        if isinstance(item, UsableItem):
            if item.type == "fishingrod" and self.walk_x == 0 and self.walk_y == 0:
                self.activity = True
                if self.animate % 15 == 0:
                    self.fishdirect = random.randint(0, 1)*2-1
                    self.fishspeed = random.randint(1, 2)*self.fishdirect
                self.is_fishing = True
                self.fishforfight_rect.x, self.fishforfight_rect.y, self.rodforfight_rect.x, self.rodforfight_rect.y, self.success, self.is_fishing, fail\
                    = item.use(tilearound, self.fishforfight, self.fishingrodforfight, self.fishforfight_rect.x, self.fishforfight_rect.y, self.rodforfight_rect.x, self.rodforfight_rect.y, self.fishspeed, self.rodspeed, self.success, self.is_fishing)
                if not self.is_fishing:
                    # give random fish to player
                    if not fail:
                        self.giveRandomFish()
                    self.resetFishing()
                    self.is_useItem = False
            else:
                self.resetFishing()
                self.is_fishing = False

    def drawUseItem(self):
        if self.is_useItem:
            self.useItem()

    def resetFishing(self):
        self.rodforfight_rect = self.fishingrodforfight.get_rect()
        self.rodforfight_rect.x, self.rodforfight_rect.y = 50*fov//2+20, 50*fov//2+75
        self.fishforfight_rect = self.fishforfight.get_rect()
        self.fishforfight_rect.x, self.fishforfight_rect.y = 50*fov//2+20, 50*fov//2+75
        self.fishdirect = random.randint(0, 1)*2-1
        self.fishspeed = random.randint(0, 6)*self.fishdirect
        self.rodspeed = -1
        self.success = 120

    def giveRandomFish(self):
        giveAt = (-1, -1)
        for i in range(3, -1, -1):
            if giveAt != (-1, -1):
                break
            for j in range(len(self.inventory.itemlist[i])):
                if self.inventory.itemlist[i][j].type == "block":
                    giveAt = (i, j)
                    break
        if giveAt == (-1, -1):
            print("Inventory_Full")
        else:
            self.inventory.itemlist[giveAt[0]][giveAt[1]] = Fish(
                giveAt[0], giveAt[1], "fish_"+str(random.randint(1, 15)))

    def drawMoney(self):
        start_x = 10
        start_y = 10
        font = pygame.font.Font('font/freesansbold.ttf', 15)
        # money = font.render(f': {self.money}', True, "black", "grey")
        money = font.render(f': {self.money:05}', True, "black", "grey")
        money.set_colorkey("grey")
        frame = pygame.transform.scale(pygame.image.load(
            f'photo/checkdetailframe.jpg'), (95, 35))
        coin = pygame.transform.scale(
            pygame.image.load(f'photo/coin.png'), (20, 20))
        coin.set_colorkey("white")
        gameDisplay.blit(frame, (start_x, start_y))
        # gameDisplay.blit(name, (mouse_x+15, mouse_y+18))
        gameDisplay.blit(coin, (start_x+9, start_y+8))
        gameDisplay.blit(money, (start_x+30, start_y+9))