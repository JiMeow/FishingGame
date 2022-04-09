import pygame
import random

dic = {50: 'bush',
       161: 'grass',
       68: 'flower',
       101: 'path',
       102: 'path',
       103: 'path',
       117: 'path',
       118: 'path',
       119: 'path',
       133: 'path',
       134: 'path',
       135: 'path',
       224: 'patharoundwater',
       242: 'patharoundwater',
       256: 'patharoundwater',
       257: 'patharoundwater',
       258: 'patharoundwater',
       261: 'bridge',
       274: 'water',
       273: 'wateroptional'}


class Tile():
    def __init__(self, id) -> None:
        self.type = id
        self.img = pygame.transform.scale(photo[id], (50, 50))
        self.img.set_colorkey((0, 0, 0))
        self.rect = self.img.get_rect()


def cut_picture(path):
    surface = pygame.image.load(path)
    tile_num_x = surface.get_size()[0] // 16
    tile_num_y = surface.get_size()[1] // 16
    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * 16
            y = row * 16
            new_surface = pygame.Surface((16, 16))
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, 16, 16))
            cut_tiles.append(new_surface)

    return cut_tiles


def readmap():
    result = []
    for i in range(3):
        ans = []
        with open(f"map/map2_Tile Layer {i+1}.csv", "r") as f:
            r = f.read().strip().split('\n')
            for i in range(len(r)):
                r[i] = r[i].strip().split(',')
                for j in range(len(r[i])):
                    r[i][j] = int(r[i][j])
                ans.append(r[i])
        result.append(ans)
    return result


photo = cut_picture("Map/atlas_16x.png")
