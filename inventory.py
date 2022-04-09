import pygame
import random
from item import *
from setting import *

class Inventory():
    def __init__(self,itemlist):
        self.itemlist = itemlist
        for i in range(len(self.itemlist)):
            for j in range(len(self.itemlist[0])):
                name = self.itemlist[i][j].split("_")[0]
                name2 = name[0].upper()+name[1:]
                item = eval(name2)(i,j,self.itemlist[i][j])
                itemlist[i][j] = item
                self.itemlist[i][j] = item