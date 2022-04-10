from item import *
from inventory import *
from tile_map import *


class Chest(Tile):
    def __init__(self, id):
        super().__init__(id)
        itemlist = self.setBlockItem()
        self.inventory = Inventory(itemlist)

    def open(self):
        inventory_img = pygame.transform.scale(
            pygame.image.load('photo/inventory.png'), (420, 210))
        # gameDisplay.blit(inventory_img, ((fov*50-420)//2, fov*50-385))
        gameDisplay.blit(inventory_img, ((fov*50-420)//2, fov*50-685))
        for i in range(len(self.inventory.itemlist)):
            for j in range(len(self.inventory.itemlist[0])):
                gameDisplay.blit(self.inventory.itemlist[i][j].img, (
                    self.inventory.itemlist[i][j].rect.x, self.inventory.itemlist[i][j].rect.y-300))

    def drawItemWhenClickChest(self, idx, idy):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.inventory.itemlist[idx][idy].id.split('_')[0] != "block":
            gameDisplay.blit(self.inventory.itemlist[idx]
                             [idy].img, (mouse_x-17.5, mouse_y-17.5))

    def draw(self, i, j):
        idx, idy = i, j
        if [idx, idy] != [-1, -1]:
            # print("draw")
            self.drawItemWhenClickChest(i, j)

    def setBlockItem(self):
        item = [["block_1" for i in range(9)] for j in range(4)]
        numberOfItem = random.randint(1, 9)
        for i in range(numberOfItem):
            item[0][i] = f"fish_{random.randint(1, 15)}"
        return item

    def checkItemDetail(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x in range(265, 684) and mouse_y in range(265, 475):
            select_x = (mouse_y-265)//50 % 4
            select_y = (mouse_x-265)//46 % 9
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

    def swapItemChest(self, idx, idy, inventory):
        before_x, before_y = idx, idy
        if self.inventory.itemlist[before_x][before_y].type == "block":
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x in range(265, 684) and mouse_y in range(265, 475):
            after_x = (mouse_y-265)//50 % 4
            after_y = (mouse_x-265)//46 % 9
            self.inventory.itemlist[before_x][before_y], self.inventory.itemlist[after_x][
                after_y] = self.inventory.itemlist[after_x][after_y], self.inventory.itemlist[before_x][before_y]
            self.inventory.itemlist[before_x][before_y].rect, self.inventory.itemlist[after_x][
                after_y].rect = self.inventory.itemlist[after_x][after_y].rect, self.inventory.itemlist[before_x][before_y].rect

    def swapItemChestInventory(self, idx, idy, inventory):
        before_x, before_y = idx, idy
        if self.inventory.itemlist[before_x][before_y].type == "block":
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x in range(268, 684) and mouse_y in range(563, 763):
            after_x = (mouse_y-563)//50 % 4
            after_y = (mouse_x-268)//46 % 9
            self.inventory.itemlist[before_x][before_y], inventory.itemlist[after_x][
                after_y] = inventory.itemlist[after_x][after_y], self.inventory.itemlist[before_x][before_y]
            self.inventory.itemlist[before_x][before_y].rect, inventory.itemlist[after_x][
                after_y].rect = inventory.itemlist[after_x][after_y].rect, self.inventory.itemlist[before_x][before_y].rect

    def swapItemInventoryChest(self, idx, idy, inventory):
        before_x, before_y = idx, idy
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if inventory.itemlist[before_x][before_y].type == "block":
            return
        if mouse_x in range(265, 684) and mouse_y in range(265, 475):
            after_x = (mouse_y-265)//50 % 4
            after_y = (mouse_x-265)//46 % 9
            inventory.itemlist[before_x][before_y], self.inventory.itemlist[after_x][
                after_y] = self.inventory.itemlist[after_x][after_y], inventory.itemlist[before_x][before_y]
            inventory.itemlist[before_x][before_y].rect, self.inventory.itemlist[after_x][
                after_y].rect = self.inventory.itemlist[after_x][after_y].rect, inventory.itemlist[before_x][before_y].rect
