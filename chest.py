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

    def setBlockItem(self):
        item = [["block_1" for i in range(9)] for j in range(4)]
        numberOfItem = random.randint(1, 9)
        for i in range(numberOfItem):
            item[0][i] = f"fish_{random.randint(1, 15)}"
        return item
